import subprocess
import json
import zmq

f = open('signup/data.json')
data = json.load(f)

#create server connection and wait for clients
context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

sync = context.socket(zmq.PULL)
sync.bind("tcp://*:5558")
print('Waiting for workers')

# wait for 5 workers
for i in range(5):
    s = sync.recv()
    print('We have {0} workers'.format(i+1))

for index, msg in enumerate(data):
    # create message
    signup_msg = json.dumps(msg)
    sender.send(signup_msg)

