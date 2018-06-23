import json
import requests
from django.conf import settings

try:
    handle_resolver = settings.HANDsdLE['resolver']
except (KeyError, AttributeError):
    handle_resolver = "http://hdl.handle.net"

try:
    handle_user = settings.HANDLE['user']
except (KeyError, AttributeError):
    handle_user = None

try:
    handle_pw = settings.HANDLE['pw']
except (KeyError, AttributeError):
    handle_pw = None

try:
    handle_url = settings.HANDLE['url']
except (KeyError, AttributeError):
    handle_url = None
try:
    handle_app_base_url = settings.HANDLE['app_base_url']
except (KeyError, AttributeError):
    handle_app_base_url = None


def create_handle(handle_url, handle_user, handle_pw, parsed_data):
    """ registered a handle-id for the url passed in as 'parsed_data """
    payload = json.dumps(
        [
            {
                "type": handle_url,
                "parsed_data": parsed_data
            }
        ]
    )

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
    }

    auth = (handle_user, handle_pw)
    try:
        response = requests.request("POST", handle_url, data=payload, headers=headers, auth=auth)
    except:
        print('something went wrong trying to send the request')
        return None

    if response.status_code == 201:
        print('created')
        return response.json()
    else:
        print(response.status_code)
        return None
