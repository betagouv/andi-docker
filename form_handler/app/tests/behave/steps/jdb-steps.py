from behave import given, when

PSH_SUBMIT_PATH = '/jdb_psh'
PSH_HIDDEN_CHECK = 'iuhs'

ENTREPRISE_SUBMIT_PATH = '/jdb_entreprise'
ENTREPRISE_HIDDEN_CHECK = 'zloe'


@given(u'valid jdb {jdb_type} data')
def step_impl(context, jdb_type):
    if jdb_type == 'psh':
        context.sub_data = {
            'andi_id': 'SOME_ANDI_ID',
            'date': '19/18/2019',
            'desc_activities': 'Contenu de test',
            'used_it_tools': 'oui',
            'desc_events_ok': 'Contenu de test',
            'desc_events_nook': 'Contenu de test',
        }
    elif jdb_type == 'entreprise':
        context.sub_data = {
            'andi_id': 'SOME_ANDI_ID',
            'date': '19/18/2019',
            'used_it_tools': 'oui',
            'desc_facts': 'Contenu de test',
            'desc_difficulties': 'Contenu de test',
        }
    else:
        raise RuntimeError


@when(u'I submit a complete jdb {jdb_type} by POST in JSON format')
def step_impl(context, jdb_type):
    if jdb_type == 'psh':
        path, check = PSH_SUBMIT_PATH, PSH_HIDDEN_CHECK
    elif jdb_type == 'entreprise':
        path, check = ENTREPRISE_SUBMIT_PATH, ENTREPRISE_HIDDEN_CHECK
    else:
        raise RuntimeError

    context.response = context.server.post(
        path,
        json={'verstopt': check, **context.sub_data}
    )
