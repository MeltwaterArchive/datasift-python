from __future__ import print_function
import time
from datasift import Client
import json

user_name = "your username"
api_key = "your API key"
datasift = Client(user_name, api_key, False)


print("Create an identity for a customer")
identity = datasift.account.identity.create('Customer name')
print(identity)

print("Update the identity")
datasift.account.identity.update(identity['id'], 'Updated Customer name')

print("Get the updated identity")
print(datasift.account.identity.get(identity['id']))

print("Create a Datasift token for this identity using a token from the third party service")
token = datasift.account.identity.token.create(identity['id'], 'Facebook', '<Facebook Token>')
print(token)

print("Create a client for the token so API calls can be made for this customer")
customer_client = Client(user_name, token['token'])

print("Get all PYLON recordings for this customer")
print(customer_client.pylon.get())

print("Create a limit for this identity and service")
datasift.account.identity.limit.create(self, identity['id'], 'Facebook', 1000)

print("Get the newly created limit")
print(datasift.account.identity.limit.get(identity['id'], 'Facebook'))

print("Delete the identity")
datasift.account.identity.delete(identity['id'])

