import os
import pickledb
import yaml
import json
import pgware
import csv
import logging
import send_mail
import sys
from flask import (
    Flask,
    request,
    Response,
    redirect,
    jsonify,
    abort,
    g
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('DEBUG'))
logger.addHandler(logging.StreamHandler())

"""
TODO:
    - validate input
    - send mail forwarding subscription information
"""


def cfg_get(config=''):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    defpath = f'{current_dir}/config.default.yaml'
    optpath = f'{current_dir}/{config}'
    def_config_file = open(defpath, 'r')
    opt_config_file = open(optpath, 'r') if os.path.exists(optpath) else None
    def_config = yaml.safe_load(def_config_file)
    config = {} if not opt_config_file else yaml.safe_load(opt_config_file)
    return {**def_config, **config}

def handler_defs_get():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f'{current_dir}/definitions.yaml', 'r') as def_file:
        handlers = yaml.safe_load(def_file)
    return handlers

def data2hash(data):
    print(data.values())
    key_info = ''.join(data.values())
    return str(hash(key_info))


def get_local_store(app):
    if 'pickledb' not in g:
        g.pickledb = pickledb.load(
            app.config['pickle_db'],
            app.config['pickle_persist'],
            False
        )

    return g.pickledb


def save_local_store(app):
    g.pickledb.dump()


def get_db(app):
    if 'pgw' not in g:
        g.pgw = pgware.build(
            client='psycopg2',
            auto_json=False,
            **app.config['postgresql']
        )
    return g.pgw.get_connection()

def get_assets(formtype, dbconn):
    result = dbconn.execute(f'SELECT key, value FROM asset WHERE description = \'mail_{formtype}\'')
    results = result.fetchall()
    data = {k: v for k, v in results}
    return(data)


def gather(fields, request, is_post, is_get, is_json):
    if is_get:
        data = {k : request.args.get(k) for k in fields}
    elif is_json:
        data = request.get_json()
        del data['verstopt']
    else:
        data = {k : request.form.get(k) for k in fields}
    return data

def handle_request(request, app, definition):
    # Prepare parsing, gather data
    is_post = request.method == 'POST'
    is_get = request.method == 'GET'
    is_json = request.content_type == 'application/json'
    if is_get:
        check = request.args.get('verstopt')
    elif is_post:
        check = request.form.get('verstopt')
    elif is_json:
        d = request.get_json()
        check = d['verstopt']

    if check != definition['hidden_check']:
        logger.info('Security check failed')
        abort(400)

    data = gather(definition['fields'], request, is_post, is_get, is_json)
    for k, v in data.items():
        if not v:
            logger.warning('Failed to gather key "%s"', k)
            abort(400)

    # Check for duplicate submit
    submission_key = data2hash(data)
    logging.info('Submission key is "%s"', submission_key)
    store = get_local_store(app)
    if store.get(submission_key) is not False:  # Data already received
        logging.info('Duplicate submission, ignoring')
        if definition['redirect'] and is_post and not is_json:
            return redirect(definition['redirect_url'], code=302)
        return Response(
            json.dumps({'error': 'data already submitted'}),
            status=409,
            mimetype='application/json'
        )

    logging.info('New submission accepted')
    store.set(submission_key, 'true')
    save_local_store(app)

    # Write to database
    if definition['persist_to_db']:
        try:
            with get_db(app) as dbconn:
                dbconn.execute(definition['sql'], data)
        except Exception as e:
            logger.exception(e)
            logger.warning('Database lost, continue')

    # Log to csv
    if definition['persist_to_csv']:
        with open(app.config['csv_file'][definition['name']], 'a', newline='') as csvf:
            columns = definition['fields'] + ['ip', 'form_type']
            wr = csv.DictWriter(csvf, columns)
            wr.writerow({
                'ip': request.remote_addr,
                'form_type': definition['name'],
                **data})

    print(json.dumps(data, indent=2))
    try:
        with get_db(app) as dbconn:
            assets = get_assets(definition['name'], dbconn)

        if definition['send_mail']:
            send_mail.send_mail(definition['name'], data, assets)

        if definition['notify_mail']:
            send_mail.notify_mail(definition['name'], data)

    except Exception as exc:
        logger.exception(exc)
        logger.warning('Failed to send mail %s, recovering', data)

    # redirect with 302, even if 303 is more (too ?) specific
    if is_post and not is_json:
        return redirect(definition['redirect'], code=302)

    return jsonify(data)


# ################################################################ FLASK ROUTES
# #############################################################################
def create_app():
    app = Flask(__name__)
    app.config = {**app.config, **cfg_get('./config.yaml')}
    app.handlers = handler_defs_get()

    @app.route('/')
    def hello():
        return 'form server'

    @app.route('/inscription', methods=['GET', 'POST'])
    def inscription():
        definition = app.handlers['landing_page']
        return handle_request(request, app, definition)

    @app.route('/jdb_psh', methods=['GET', 'POST'])
    def jdb_psh():
        definition = app.handlers['jdb_psh']
        return handle_request(request, app, definition)

    @app.route('/jdb_entreprise', methods=['GET', 'POST'])
    def jdb_entreprise():
        definition = app.handlers['jdb_entreprise']
        return handle_request(request, app, definition)

    return app


#         ## legacy
#         ####################################
#         if is_get:
#             if request.args.get('verstopt') != 'vrst':
#             data = {
#                 'nom': request.args.get('nom'),
#                 'prenom': request.args.get('prenom'),
#                 'email': request.args.get('email'),
#                 'form_type': 'landing_page'
#             }
#         elif is_json:
#             data = request.get_json()
#             data['form_type'] = 'landing_page'
#             if data.get('verstop') != 'vrst':
#                 logger.info('Security check failed')
#                 abort(400)
#             del data['verstopt']
#         else:
#             data = {
#                 'nom': request.form.get('nom'),
#                 'prenom': request.form.get('prenom'),
#                 'email': request.form.get('email'),
#                 'form_type': 'landing_page'
#             }
#             if request.form.get('verstopt') != 'vrst':
#                 logger.info('Security check failed')
#                 abort(400)
# 
#         # Validate data
#         handler.
#         if not data['nom']:
#             logger.warning('Missing field NOM')
#             abort(400)
#         if not data['prenom']:
#             logger.warning('Missing field PRENOM')
#             abort(400)
#         if not data['email']:
#             logger.warning('Missing field EMAIL')
#             abort(400)
# 
#         # Check if not already received
#         submission_key = data2hash(data)
#         logging.info('Submission key is "%s"', submission_key)
#         store = get_local_store(app)
#         if store.get(submission_key) is not False:  # Data already received
#             logging.info('Duplicate submission, ignoring')
#             if is_post and not is_json:
#                 return redirect("https://andi.beta.gouv.fr/merci", code=302)
#             return Response(
#                 json.dumps({'error': 'data already submitted'}),
#                 status=409,
#                 mimetype='application/json'
#             )
#         logging.info('New submission accepted')
#         store.set(submission_key, 'true')
#         save_local_store(app)
# 
#         # Write to database
#         try:
#             with get_db(app) as dbconn:
#                 write_user(data, dbconn)
#         except Exception as e:
#             logger.exception(e)
#             logger.warning('Database lost, continueing')
# 
#         # Log to csv
#         with open(app.config['csv_file'], 'a', newline='') as csvf:
#             columns = ['nom', 'prenom', 'email', 'ip', 'form_type']
#             wr = csv.DictWriter(csvf, columns)
#             wr.writerow({'ip': request.remote_addr, **data})
# 
#         # Send "received" mail
#         print(json.dumps(data, indent=2))
#         with get_db(app) as dbconn:
#             assets = get_assets(data['form_type'], dbconn)
# 
#         if send_mail.send_mail(data['form_type'], data, assets):
#             send_mail.notify_mail(data['form_type'], data)
#         else:
#             logger.warning('Failed to send mail %s', data)
# 
#         # redirect with 302, even if 303 is more (too ?) specific
#         if is_post and not is_json:
#             return redirect("https://andi.beta.gouv.fr/merci", code=302)
# 
#         return jsonify(data)
#     return app


if __name__ == '__main__':
    create_app().run()
