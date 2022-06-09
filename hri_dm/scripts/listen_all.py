#!/usr/bin/env python

import requests
import rospy, sys
from std_msgs.msg import String
# from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM
from hri_dm import msg

link = 'http://25.45.111.204:1026/v2/entities/' \
       'FHOOE.Orchestrator.Runtime.WorkflowCommand:466dfc51-c3ce-4e32-9cce-1a8407ab657e'
rt_Action = 'FHOOE.Orchestrator.Runtime.Action:d7451d3f-2cee-4e41-a40f-30a511183a26'


def get_adaptId(*args):
    # r1 = requests.get("http://25.45.111.204:1026/v2/entities/" + str(rt_Action))
    r = requests.get(link)
    print (r.status_code,
           r.headers['Date'],
           r.headers['Connection'],
           )
    return r


r = get_adaptId(link)
r.json()


# print (r)


#  fiware imports
# sys.path.append("humanRob_ws/src/fiware")

def callback1(data):
    print('callback____1')
    rospy.loginfo('receiving message %s', data.error_type)
    if data.result == True:
        print ("peirame TRUE")
        rospy.loginfo('we got Truesszz')
        newtask = msg.HRIDM2TaskExecution()
        newtask.action = 'next_task111111'
        rospy.loginfo(newtask)
    else:
        print('FALSE')
        newtask = msg.HRIDM2TaskExecution()
        newtask.action = 'please try again1111'
        rospy.loginfo(newtask)


def callback2(data):
    # rospy.sleep(.5)
    print('callback___2')
    rospy.loginfo('receiving message2222 %s', data.action)


def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver_all node started')
    print('init_receiver_all always awaits.. .')
    rospy.Subscriber('taskExec_2HRIDM', msg.TaskExecution2HRIDM, callback1)
    rospy.Subscriber('HRIDM2_taskExec', msg.HRIDM2TaskExecution, callback2)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)

    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
