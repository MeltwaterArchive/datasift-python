from behave import *
from datasift import Client

client = Client("<name>", "<api_key>")

use_step_matcher('parse')


@given("CSDL to validate like '{csdl_val}'")
def step_impl(context, csdl_val):
    setattr(context, 'csdl_val', csdl_val)


@when('I call the validate endpoint')
def step_impl(context):
    assert(client.is_valid(context.csdl_val))


@then('I should get a validation with a dpu cost')
def step_impl(context):
    response = client.validate(context.csdl_val)
    assert(response['dpu'] > 0)


@given("CSDL to compile like '{csdl_com}'")
def step_impl(context, csdl_com):
    setattr(context, 'csdl_com', csdl_com)


@when('I call the compile endpoint')
def step_impl(context):
    assert(client.is_valid(context.csdl_com))
    setattr(context, 'response', client.compile(context.csdl_com))


@then('I should get a compilation with a hash')
def step_impl(context):
    response = context.response
    assert(response['hash'])


@when('I call the usage endpoint')
def step_impl(context):
    setattr(context, 'usage', client.usage())


@then('I should get back account usage')
def step_impl(context):
    assert(context.usage['end'])


@given("a hash like '{dpu_hash}'")
def step_impl(context, dpu_hash):
    setattr(context, 'dpu_hash', dpu_hash)


@when('I call the dpu endpoint')
def step_impl(context):
    response = client.dpu(context.dpu_hash)
    setattr(context, 'response', response)


@then('I should get a dpu cost')
def step_impl(context):
    assert(context.response['dpu'] > 0)


@given("A facebook page like {page_id}")
def step_impl(context, page_id):
    setattr(context, 'page_id', page_id)


@when('I call the source create endpoint')
def step_impl(context):
    parameters = {
        "likes": True,
        "posts_by_others": True,
        "comments": True,
        "page_likes": True
    }

    resources = [
        {
            "parameters": {
                "url": "http://www.facebook.com/" + context.page_id,
                "title": context.page_id,
                "id": context.page_id
            }
        }
    ]

    auth = [
        {
            "parameters": {
                "value": "<token_id>"
            }
        }
    ]
    response = client.managed_sources.create('facebook_page', 'test', resources, auth, parameters)
    setattr(context, 'response', response)


@then('I should get a valid source back')
def step_impl(context):
    assert(context.response['id'])


@then('I should be able to start the source I just created')
def step_impl(context):
    resp = client.managed_sources.start(context.response['id'])
    assert(resp['status'] == 'active')


@then('I should be able to stop the source I just started')
def step_impl(context):
    resp = client.managed_sources.stop(context.response['id'])
    assert(resp['status'] == 'paused')


@then('I should be able to delete the source I just created')
def step_impl(context):
    resp = client.managed_sources.delete(context.response['id'])
    assert(resp.status_code == 204)


@then('I should be able to get the source I just created')
def step_impl(context):
    resp = client.managed_sources.get()
    assert(context.response['id'] in [source['id'] for source in resp['sources']])


@then('I should be able to update the source I just created with a new page "applemusic"')
def step_impl(context):
    parameters = {
        "likes": True,
        "posts_by_others": True,
        "comments": True,
        "page_likes": True
    }

    resources = [
        {
            "parameters": {
                "url": context.response['resources'][0]['parameters']['url'],
                "title": context.response['resources'][0]['parameters']['title'],
                "id": context.response['resources'][0]['parameters']['id']
            },
            "resource_id": context.response['id']
        },
        {
            "parameters": {
                "url": "http://www.facebook.com/applemusic",
                "title": "applemusic",
                "id": "applemusic"
            }
        }
    ]

    auth = [
        {
            "parameters": {
                "value": "<token_id>"
            }
        }
    ]
    response = client.managed_sources.update(context.response['id'], 'facebook_page', 'test', resources, auth, parameters)
    assert(response.status_code == 202)
    setattr(context, 'response', response)


@then('I should be able to get the source and it should have the two pages I added')
def step_impl(context):
    resp = client.managed_sources.get()
    assert(len(resp['sources']) == 2)


@then('I should be able to add a new authentication token to the source I just created')
def step_impl(context):
    auth_id = [
        {
            "parameters": {
                "value": "<auth_id>"
            }
        }
    ]
    resp = client.managed_sources.auth.add(context.response['id'], auth_id)
    assert(resp.status_code == 200)


@then(u'I should be able to remove an authentication token from the source I just created')
def step_impl(context):
    auth_ids = ["<auth_id>"]
    resp = client.managed_sources.auth.remove(context.response['id'], auth_ids)
    assert(resp.status_code == 200)
