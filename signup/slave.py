import sys
import time
import zmq
import requests
import json
import re

def signup(email, questions):

    csrf_url = 'http://mooc-signup-test.herokuapp.com'
    resp = requests.get(csrf_url)
    match = re.search(u".*csrfmiddlewaretoken'\ value='(?P<token>[a-z,A-Z,0-9]+)'", resp.text)
    csrf_token = match.groups('token')[0]

    signup_url = 'http://mooc-signup-test.herokuapp.com/signup'
    signup_data = {
        'csrfmiddlewaretoken': csrf_token,
        'email': email,
    }
    signup_data.update(questions)

    resp = requests.post(signup_url, data=signup_data, cookies=resp.cookies)
    if resp.status_code != 200:
        print(resp.text)

master_address = sys.argv[1]

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://{0}:5557".format(master_address))

# Socket to sync with master
sync = context.socket(zmq.PUSH)
sync.connect("tcp://{0}:5558".format(master_address))
sync.send('Reporting for duty')

# Process tasks forever
while True:
    print("ready for work")
    s = receiver.recv()
    signup(**json.loads(s))
    print(s)

