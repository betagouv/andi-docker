import pickledb
from behave import given, then, when

from src import form_server as server

SUBMIT_PATH = '/inscription'
HIDDEN_CHECK = 'vrst'


@given(u'valid subscription data')
def step_impl(context):
    context.sub_data = {
        'nom': 'martin',
        'prenom': 'ricky',
        'email': 'martin.ricky@example.com',
    }


@when(u'I submit a complete subscription by POST')
def step_impl(context):
    context.response = context.server.post(
        SUBMIT_PATH,
        data={'verstopt': HIDDEN_CHECK, **context.sub_data}
    )


@when(u'I submit a complete subscription by POST in JSON format')
def step_impl(context):
    context.response = context.server.post(
        SUBMIT_PATH,
        json={'verstopt': HIDDEN_CHECK, **context.sub_data}
    )


@when(u'I submit a complete subscription by GET')
def step_impl(context):
    context.response = context.server.get(
        SUBMIT_PATH,
        query_string={'verstopt': HIDDEN_CHECK, **context.sub_data}
    )


@then(u'I receive a response redirecting me to "{page}"')
def step_impl(context, page):
    assert context.response.status_code == 302
    assert page.encode('ascii') in context.response.data


@then(u'the response is in JSON')
def step_impl(context):
    assert context.response.content_type == 'application/json'


@then(u'it contains the same data that was being sent')
def step_impl(context):
    print(f'Sent data: {context.sub_data}')
    print(f'Received data: {context.response.get_json()}')
    assert context.sub_data == context.response.get_json()


@then(u'I can check the information has been received')
def step_impl(context):
    store = pickledb.load(context.pickle_file, False)
    # remove hidden key for correct key generation
    key = server.data2hash(context.sub_data)
    assert store.get(key) is not False


@then(u'the response code indicates a failure')
def step_impl(context):
    assert context.response.status_code == 409


@then(u'the error message says "{message}"')
def step_impl(context, message):
    msg = context.response.get_json()
    assert msg['error'] == message


@when(u'I add a new field "{field}" with value "{field_value}" to the data')
def step_impl(context, field, field_value):
    context.sub_data[field] = field_value


@then(u'the SQL query contains the data from "{field}"')
def step_impl(context, field):
    check = context.sub_data[field]
    calls = context.pgw_mock.mock_calls
    name, args, kwargs = calls[3]
    sql = args[0]
    data = args[1]
    print(sql)
    print(data)
    assert data[field] == context.sub_data[field]
