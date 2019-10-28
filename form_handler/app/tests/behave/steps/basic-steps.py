from behave import given, then, when
from unittest import mock
from src import form_server as server


@given(u'an instance of the server application')
def step_impl(context):
    assert context.server is not None


@given(u'a mock db interface')
def step_impl(context):
    pgw_mock = mock.MagicMock()
    pgw_mock.__enter__.return_value = mock.Mock()
    server.pgware = pgw_mock


@when(u'I send an empty head query')
def step_impl(context):
    context.response = context.server.get('/')
    print(context.response.__dict__)


@then(u'I receive a response indicating it worked')
def step_impl(context):
    assert context.response.status_code == 200


@then(u'it contains "{text}"')
def step_impl(context, text):
    # response is bin string
    assert context.response.data == text.encode('ascii')
