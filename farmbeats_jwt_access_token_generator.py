import requests
import json
import msal

# Your service principal App ID
CLIENT_ID = "7cd01835-e347-4811-9894-d233b75d2fa7"
# Your service principal password
CLIENT_SECRET = "YTFiYzE3NzUtMjRkYy00ODQyLThjOTktZWFlMDhkMGJmNjMz="
# Tenant ID for your Azure subscription
TENANT_ID = "d78aee32-8f91-4f9e-90ea-fb72965d9d7c"

AUTHORITY_HOST = 'https://login.microsoftonline.com'
AUTHORITY = AUTHORITY_HOST + '/' + TENANT_ID

ENDPOINT = "https://imiotcoe-farmbeats-api.azurewebsites.net"
SCOPE = ENDPOINT + "/.default"

context = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = context.acquire_token_for_client(SCOPE)
# We should get an access token here
access_token = token_response.get('access_token')
print(access_token)
