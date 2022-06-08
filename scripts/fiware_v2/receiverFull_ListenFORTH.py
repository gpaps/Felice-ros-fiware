import sys
import signal
import rospy
from PyQt4.uic.properties import logger
from mercurial.httpclient._readers import logger

import requests
# import logging, logger

from logger import Log, initLog
import json

# from http.server import HTTPServer    # this is for use with python3
# from http.server import BaseHTTPRequestHandler   # this is for use with python3

# noinspection PyCompatibility
from BaseHTTPServer import HTTPServer  # this is for use with python2
# noinspection PyCompatibility
from BaseHTTPServer import BaseHTTPRequestHandler  # this is for use with python2
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM

pub2HRIDM = rospy.Publisher('fiwareTest', TaskExecution2HRIDM, queue_size=100)


def send_msg():
    global pub2HRIDM
    task_exec = TaskExecution2HRIDM()
    task_exec.request_id = 0
    task_exec.result = False
    task_exec.error_type = 'NavigationFailed'
    rospy.loginfo(task_exec)
    pub2HRIDM.publish(task_exec)


# Intercepts incoming messages
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        datalen = int(self.headers['Content-Length'])  # size receive message
        data = self.rfile.read(datalen)  # read receive messages
        obj = json.loads(data)  # convert message to json

        # this is to place the code
        print(obj)
        print(type(obj['data']))
        xdatalist = obj['data']
        print(xdatalist[0])
        # element=xdatalist[0]

        element = obj['data'][0]['id']
        send_msg()
        # Here add thr code for processing.

        print("------ DONE")

        # print(obj['data']['id'])

        Log("INFO", json.dumps(obj, indent=4, sort_keys=True))  # print receive messages
        self.send_response(200)
        self.end_headers()


class MyReceiver:
    def __init__(self, address="0.0.0.0", port=8080):
        self.address = address
        self.port = port
        self.stopped = False
        Protocol = "HTTP/1.0"

        # set ip and port my server
        server_address = (self.address, self.port)

        # initialize RequestHandler
        RequestHandler.protocol_version = Protocol
        self.httpd = HTTPServer(server_address, RequestHandler)

    def start(self):  # Start server method
        sa = self.httpd.socket.getsockname()
        Log("INFO", "\nServing HTTP on", sa[0], "port", sa[1], "...")

        while not self.stopped:
            print("inloop")
            self.httpd.handle_request()
            print("inloop....2")

    def close(self):  # Stop server method
        self.stopped = True


# CB_HEADER = {'Content-Type': 'application/json'}
# CB_BASE_URL = None
# selection_port = None
# selection_address = None

initLog()

# Input data acquisition
selection_port = '2620'
selection_address = '25.22.193.22'
selection_port_CB = '1026'
selection_address_CB = '25.45.111.204'

# "            \"idPattern\": \".*\",\n"\
# 25.74.68.25 MIXALIS
# 25.17.36.113 VAG

# subscription message
# msg = "{"\
# "    \"description\": \"FORTH Subscription\",\n"\
# "    \"subject\": {\n"\
# "        \"entities\":\n"\
# "        [{\n"\
# "            \"idPattern\": \"FHOOE.Orchestrator.*\",\n"\
# "            \"typePattern\": \".*\"\n"\
# "        }],\n"\
# "        \"conditions\": {\n"\
# "            \"attrs\": []\n"\
# "        }\n"\
# "    },\n"\
# "    \"notification\": {\n"\
# "        \"http\": {\n"\
# "            \"url\": \"http://25.74.68.25:2620/\",\n"\
# "            \"method\": \"POST\",\n"\
# "            \"headers\": {\n"\
# "                \"Content-Type\": \"application/json\"\n"\
# "            }\n"\
# "        }\n"\
# "    }\n}"
#
# CB_BASE_URL = "http://{}:{}/v2/".format(selection_address_CB, selection_port_CB) #url send notification
#
#
# response = requests.post(CB_BASE_URL+"subscriptions/", data = msg, headers = CB_HEADER) #send request to Context Broker
# if response.ok: #positive response, notification accepted
#     print("CB response -> status " + response.status_code.__str__())
# else: #error response
#     print("CB response -> " + response.text)
#

####
#### up to hear we do the subscription
####

#### if we do many subscriptions, we can delete them from "terminal" using:  curl --location --request DELETE 'http://25.45.111.204:1026/v2/subscriptions/ID'
### opoy to id to perneis apo edw  http://25.45.111.204:1026/v2/subscriptions/

Log("INFO", "Initialized")

rospy.init_node('fiware_ListenerFORTH', anonymous=True)

# Start server, receive message
try:
    server = MyReceiver(selection_address, int(selection_port))
except Exception as ex:
    raise Exception("Unable to create a Receiver")
else:  # close application and server
    def signal_handler(signal, frame):
        Log("INFO", '\nExiting from the application')
        server.close()
        Log("INFO", '\nExit')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

Log("INFO", "\nStarting...")
Log("INFO", "---------------------------------\n")
server.start()