#!/usr/bin/env python3
import logging
import time
import click
import os
from airtable import Airtable
import os
import requests
import datetime
from datetime import datetime as dt
import psycopg2
import time
import re
from send_mail import send_mail, notify_mail

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('INFO'))
logger.addHandler(logging.StreamHandler())

TABLE_NAMES = {
    'immersions': 'Immersion',
    'people': 'Profils selectionnés',
    'companies': 'Employeurs identifiés'
}

MAPPINGS_IMMERSION = [
    ('ID Immersion', 'id'),
    ('PSH', 'person'),
    ('Employeur accueillant', 'companies'),
    ('Date d\u00e9marrage', 'start_date'),
    ('Date fin', 'end_date'),
    ('Lien JDB - PSH', 'psh_jdb_link'),
    ('Lien JDB - EMPLOYEUR', 'entreprise_jdb_link'),
    ('Etape', 'stage'),
]

MAPPINGS_PEOPLE = [
    ('ANDi iD', 'andi_id'),
    ('Name', 'name'),
    ('Email', 'mail'),
]

MAPPINGS_ENTREPRISE = [
    ('Name', 'name')
]


def map_record(record, mapping):
    return {to: record.get(fr) for (fr, to) in mapping}


def get_all(airtable, mapping):
    all_records = {}
    pages = airtable.get_iter(maxRecords=50)
    for page in pages:
        for record in page:
            try:
                all_records[record['id']] = map_record(record['fields'], mapping)
            except Exception as exc:
                logger.exception(exc)

    return all_records


def get_assets(mail_def, dbconn):
    with dbconn.cursor() as cur:
        cur.execute(f'SELECT key, value FROM asset WHERE description = \'mail_{mail_def}\'')
        results = cur.fetchall()
    data = {k: v for k, v in results}
    return(data)


def notify_slack(msg):
    hook_path = os.environ['SLACK_HOOK']
    hook_url = f'https://hooks.slack.com/services/{hook_path}'
    block = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': msg
        },
    }
    for i in range(0, 10):
        try:
            resp = requests.post(
                hook_url,
                json={'blocks': [block]},
            )
            ok_to_proceed = resp.status_code == 200
        except Exception:
            ok_to_proceed = False

        if ok_to_proceed:
            return
        elif i >= 10:
            logger.warning('Failed to notify slack: %s / %s', resp.text, resp.status_code)
            return

        time.sleep(i)


def CatchAllExceptions(cls, handler):

    class Cls(cls):

        _original_args = None

        def make_context(self, info_name, args, parent=None, **extra):
            # grab the original command line arguments
            self._original_args = ' '.join(args)

            try:
                return super(Cls, self).make_context(
                    info_name, args, parent=parent, **extra)
            except Exception as exc:
                # call the handler
                handler(self, info_name, exc)

        def invoke(self, ctx):
            try:
                return super(Cls, self).invoke(ctx)
            except Exception as exc:
                # call the handler
                handler(self, ctx.info_name, exc)

    return Cls


def report_exception(cmd, info_name, exc):
    logger.exception(exc)
    if 'SLACK_HOOK' in os.environ:
        notify_slack(f':bangbang: @chaîne @Pieterjan Echec envoi mailing: *{str(exc)}*')
    else:
        logger.warning('Could not notify Slack')


# ################################################################### MAIN FLOW
# #############################################################################
@click.group(cls=CatchAllExceptions(click.Group, handler=report_exception))
@click.pass_context
@click.option('--notify-mail', help='mail adress to notify to', default=None)
@click.option('--notify-slack', is_flag=True, default=False)
@click.option('--debug', is_flag=True, default=False)
@click.option('--dry-run', is_flag=True, default=False)
@click.option('--test-mail', help='Mail adress to send mails to', default=None)
def main(ctx, notify_mail, notify_slack, debug, dry_run, test_mail):
    if debug:
        logger.setLevel(logging.getLevelName('DEBUG'))
        logger.debug('Debugging enabled')
    ctx.obj['dry_run'] = dry_run
    ctx.obj['test_mail'] = test_mail
    ctx.obj['notif_mail'] = notify_mail
    ctx.obj['notify_slack'] = notify_slack
    if notify_slack:
        if 'SLACK_HOOK' not in os.environ:
            raise RuntimeError('Missing slack token')

    if ctx.obj['dry_run']:
        logger.debug('Dry Run enabled')

    for x in ['AIRTABLE_KEY', 'AIRTABLE_BASE_KEY', 'PG_DSN', 'MG_BOX', 'MG_KEY']:
        if x not in os.environ:
            raise RuntimeError(f'Missing env variable "{x}"')
        ctx.obj[x.lower()] = os.environ[x]

    table_def = [
        ('immersions', MAPPINGS_IMMERSION),
        ('people', MAPPINGS_PEOPLE),
        ('companies', MAPPINGS_ENTREPRISE),
    ]

    for key, mapping in table_def:
        table = TABLE_NAMES.get(key)
        if table is None:
            logger.critical('Could not access table "%s": check name', key)
            raise RuntimeError('Wrong table definitions')
        logger.info('Preparing to query airtable "%s"', table)
        temp_table = Airtable(ctx.obj['airtable_base_key'], table, api_key=ctx.obj['airtable_key'])
        ctx.obj[key] = get_all(temp_table, mapping)
        i = 0
        if debug:
            for k, v in ctx.obj[key].items():
                i += 1
                if i > 3:
                    break
        # Avoid triggering airtable throttling
        time.sleep(.5)

    ctx.obj['dbconn'] = psycopg2.connect(ctx.obj['pg_dsn'])


@main.command(cls=CatchAllExceptions(click.Command, handler=report_exception))
@click.pass_context
def daily_jdb_psh(ctx):
    # Clean list
    records = [x for x in ctx.obj['immersions'].values() if x['start_date'] and x['end_date']]
    for rec in records:
        try:
            rec['start_date_dt'] = dt.strptime(rec['start_date'], '%Y-%m-%d')
            rec['end_date_dt'] = dt.strptime(rec['end_date'], '%Y-%m-%d') + datetime.timedelta(0, 23 * 3600 + 59 * 60 + 59)
            rec['person'] = rec['person'][0]
            rec['company'] = rec['companies'][0]
        except Exception as exc:
            logger.critical('Encountered error with record %s', rec)
            logger.exception(exc)
            raise

    # Filter
    now = dt.now()
    send_list = []
    for rec in records:
        if rec['start_date_dt'] < now and rec['end_date_dt'] > now:
            if rec['stage'] != 'Immersion en cours':
                logger.warning('Immersion %s can\'t be activated: wrong stage (%s)', rec['id'], rec['stage'])
            else:
                logger.info('Immersion %s ( %s ) is active', rec['id'], rec['stage'])
                send_list.append(rec)

    mail_assets = get_assets('jdb_psh', ctx.obj['dbconn'])

    for rec in send_list:
        logger.debug('Checking auto-mail for %s', rec['person'])
        person_rec = ctx.obj['people'][rec['person']]
        raw_name = person_rec['name']
        name = re.sub(r'\b[A-Z\'\-]+\b', '', raw_name).strip()

        company = ctx.obj['companies'][rec['company']]['name']

        if ctx.obj['dry_run']:
            mail = None
        elif ctx.obj['test_mail']:
            mail = ctx.obj['test_mail']
        else:
            mail = person_rec['mail']

        mail_data = {
            'prenom': name,
            'jdb_url': rec['psh_jdb_link'],
            'entreprise': company,
            'email': mail
        }

        logger.debug('Sending mail to %s', mail_data['prenom'])
        if ctx.obj['dry_run']:
            logger.debug('** DRY-RUN: Not sending anything **')
            continue

        send_mail('jdb_psh', mail_data, mail_assets)
        if ctx.obj['notif_mail'] is not None:
            notify_mail(
                mail_type='jdb_psh',
                data=mail_data,
                subject=f'Rappel JDB PSH Sent: {person_rec["mail"]}',
                to=ctx.obj['notif_mail']
            )
        if ctx.obj['notify_slack'] is not None:
            msg_str = f':pouce: Rappel JDB PSH envoyé à {person_rec["mail"]}'
            notify_slack(msg_str)


if __name__ == '__main__':
    main(obj={})  # pylint:disable=no-value-for-parameter, unexpected-keyword-arg
