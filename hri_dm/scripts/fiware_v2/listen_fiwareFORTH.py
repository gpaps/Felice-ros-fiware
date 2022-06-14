import sys
import json
import rospy
import signal
import requests
from logger import Log, initLog
from http.server import HTTPServer  # this is for use with python3
from http.server import BaseHTTPRequestHandler  # this is for use with python3
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM

pub2TaskExe = rospy.Publisher('Task2Execute', HRIDM2TaskExecution, queue_size=100)

link_pickup = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:9ed181c2-2971-456c-b0e1-63bb1cf0c3c6'
link_navigate = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:6d763707-7bb0-4888-b42d-6039a840ace7'
link_release = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:084d5ef5-b30b-4089-a430-0880f569cd65'
link_handover = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:f29a6ca9-5f04-4c1e-a15a-4b3baaa1f0d0'

def get_adaptId(wfc):
    r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(wfc))
    print(r.status_code, 'first_query')
    action_link = r.json()['refAction']['value']
    action_r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(action_link))
    print(action_r.status_code, 'second_query')
    action_name = action_r.json()['adaptType']['value']
    # params = r.json()['parameters']['value']['location']
    return r, action_name


def send_msg():
    global pub2TaskExe
    task_exec = HRIDM2TaskExecution()
    r, task_exec.action = get_adaptId(link_navigate)
    if task_exec.action == 'handover':
        params_handover = r.json()['parameters']['value']['tool']['toolId']

    if task_exec.action == 'navigate':
        params_nav = r.json()['parameters']['value']['location']['namedLocation']
        # params_nav0 = r.json()['parameters']['value']['location']
        print(params_nav)
        task_exec.navpos.x = 12
        task_exec.navpos.y = 13

    # task_exec.action = 'pickup'
    task_exec.tool_id = 2
    # TODO vector3Pose2D
    task_exec.request_id = 5232
    rospy.loginfo(task_exec)
    pub2TaskExe.publish(task_exec)


# Intercepts incoming messages
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        datalen = int(self.headers['Content-Length'])  # size receive message
        data = self.rfile.read(datalen)  # read receive messages
        obj = json.loads(data)  # convert message to json

        # this is to place the code
        # element = obj['data'][0]['id']

        # Here add thr code for processing.
        print(" Received Fiware Msg ")
        send_msg()

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
selection_address = '25.28.115.246'
selection_port_CB = '1026'
selection_address_CB = '25.45.111.204'


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
