import requests
import sys
from dotenv import load_dotenv
import os

def control_ac(on = False):

    # load credentials
    load_dotenv()

    # new session
    s = requests.Session()

    # login
    payload = {"user":{"email": os.environ.get('email'), "password": os.environ.get('password'), "application": {"app_id": "", "app_secret": ""}}}
    response_login = s.post('https://connectstat.carrier.com/api/users/sign_in', json=payload)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'auth_token ' + response_login.json()['access_token']
    }

    # 3: turn on
    # 0: turn off
    if on:
        action_value = 3
    else:
        action_value = 0

    # send request to server
    s.post(
        'https://connectstat.carrier.com/api-devices-field/apiv1/dsns/' + os.environ.get('device_id') + '/properties/UsrMd1/datapoints',
        headers=headers,
        json={"datapoint": {"value": action_value}}
    )

    # close session
    s.close()

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        # turn off ac
        control_ac()
        
    elif sys.argv[1] == 'on':
        # turn on ac
        control_ac(on=True)
