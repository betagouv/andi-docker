import logging
import os
import pprint
import re
import copy

# import json
import mistune
import requests
from liquid import Liquid

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('DEBUG'))
logger.addHandler(logging.StreamHandler())

MASK_INSCRIPTION_TEXT = """
{{mail_text}}
"""


MASK_NOTIFICATION = """
Notification d'envoi de mail de type "{{mail_type}}":

{{data}}
"""

MAILGUN_KEY = os.environ['MG_KEY']
MAILGUN_SANDBOX = os.environ['MG_BOX']


def notify_mail(mail_type, data, subject=False, to='andi@beta.gouv.fr'):
    text = Liquid(MASK_NOTIFICATION).render(
        mail_type=mail_type,
        data=pprint.pformat(data, indent=4)
    )
    if not subject:
        subject = f'Formulaire reçu type "{mail_type}"'
    send(
        recipient=to,
        subject=subject,
        text=text
    )


def get_template(mail_type):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = f'{current_dir}/templates/{mail_type}.html'
    with open(path, 'r') as f:
        data = f.read()
    return data


def send_mail(mail_type, data, assets_in):
    assets = copy.copy(assets_in)
    logger.debug("Preparing to send mail %s", mail_type)
    for key, value in assets.items():
        assets[key] = Liquid(value).render(**data)

    mail_text = mistune.markdown(assets['texte'], escape=False)
    content_text = cleanhtml(Liquid(MASK_INSCRIPTION_TEXT).render(mail_text=mail_text))
    content_html = Liquid(get_template(mail_type)).render(mail_text=mail_text, mail_subject=assets['sujet'])

    result = send(
        recipient=data['email'],
        subject=assets.get('sujet', 'Courrier andi.beta.gouv.fr'),
        text=content_text,
        html=content_html
    )

    if result:
        logger.debug("Mail '%s' sent", mail_type)
        return True

    logger.warning("Failed to send mail %s", mail_type)
    return False


def send(recipient, subject, text, html=None):
    request_url = f'https://api.eu.mailgun.net/v3/{MAILGUN_SANDBOX}/messages'
    data = {
        'from': 'ANDi no-reply <no-reply@mailgun.bilo.be>',
        'to': recipient,
        'subject': subject,
        'text': text,
        'html': html,
        'h:Reply-To': 'ANDi <andi@beta.gouv.fr>'
    }

    # if not html:
    #     del data['html']

    request = requests.post(
        request_url,
        auth=('api', MAILGUN_KEY),
        data=data
    )
    return request.status_code == 200


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
