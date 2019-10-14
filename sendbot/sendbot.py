#!/usr/bin/env python3
import logging
import click
from airtable import Airtable
import os
import datetime
from datetime import datetime as dt
import psycopg2
import time
import re
from send_mail import send_mail, notify_mail

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('INFO'))
logger.addHandler(logging.StreamHandler())

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


# ################################################################### MAIN FLOW
# #############################################################################
@click.group()
@click.pass_context
@click.option('--notify-mail', help='mail adress to notify to', default=None)
@click.option('--debug', is_flag=True, default=False)
@click.option('--dry-run', is_flag=True, default=False)
@click.option('--test-mail', help='Mail adress to send mails to', default=None)
def main(ctx, notify_mail, debug, dry_run, test_mail):
    if debug:
        logger.setLevel(logging.getLevelName('DEBUG'))
        logger.debug('Debugging enabled')
    ctx.obj['dry_run'] = dry_run
    ctx.obj['test_mail'] = test_mail
    ctx.obj['notif_mail'] = notify_mail

    if ctx.obj['dry_run']:
        logger.debug('Dry Run enabled')

    for x in ['AIRTABLE_KEY', 'AIRTABLE_BASE_KEY', 'PG_DSN', 'MG_BOX', 'MG_KEY']:
        if x not in os.environ:
            raise RuntimeError(f'Missing env variable "{x}"')
        ctx.obj[x.lower()] = os.environ[x]

    table_def = [
        ('Immersion', 'immersions', MAPPINGS_IMMERSION),
        ('Fiches PSH', 'people', MAPPINGS_PEOPLE),
        ('Entreprises / Employeurs', 'companies', MAPPINGS_ENTREPRISE),
    ]

    for table, key, mapping in table_def:
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


@main.command()
@click.pass_context
def daily_jdb_psh(ctx):
    # Clean list
    records = [x for x in ctx.obj['immersions'].values() if x['start_date']]
    for rec in records:
        rec['start_date_dt'] = dt.strptime(rec['start_date'], '%Y-%m-%d')
        rec['end_date_dt'] = dt.strptime(rec['end_date'], '%Y-%m-%d') + datetime.timedelta(0, 23 * 3600 + 59 * 60 + 59)
        rec['person'] = rec['person'][0]
        rec['company'] = rec['companies'][0]

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


if __name__ == '__main__':
    main(obj={})  # pylint:disable=no-value-for-parameter, unexpected-keyword-arg
