#!/usr/bin/env python
from Cython.Compiler.PyrexTypes import error_type

import sys
import rospy

# import from files
from std_msgs.msg import String
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM
from src.hri_dm.scripts.listenerSubscriber import init_receiver, callback

# fiware imports
from src.hri_dm.scripts.fiware_v2.forthHRIHealthPost import HRI_HealthStatePost, HRI_Health
robotAction_jsonFName = r"/home/gpaps/humanRob_ws/src/beginner_tutorials/scripts/fiware_v2/health.json"
address = "25.45.111.204"
port = 1026

pub2HRIDM = rospy.Publisher('taskExec_2HRIDM', TaskExecution2HRIDM, queue_size=100)

def send_msg():
    global pub2HRIDM
    task_exec = TaskExecution2HRIDM()
    task_exec.request_id = 0
    task_exec.result = False
    task_exec.error_type = 'NavigationFailed'
    rospy.loginfo(task_exec)
    pub2HRIDM.publish(task_exec)


def send_msg2():
    task_exec2 = HRIDM2TaskExecution()
    task_exec2.action = 'NavigationRecovery'
    task_exec2.tool_id = 4
    task_exec2.theta = 45.0
    task_exec2.request_id = 5
    task_exec2.x = 2.2
    task_exec2.y = 2.32
    task_exec2.z = 1.0
    rospy.loginfo(task_exec2)
    # pub2task.publish(task_exec2)


def native_sender():
    global result
    rospy.loginfo('sender node starter')
    send_msg()


if __name__ == '__main__':
    # init the 1st publisher  or init the first pub-in
    rospy.init_node('TaskExecution2HRIDM', anonymous=True)
    HRI_HealthStatePost(address, port, robotAction_jsonFName)
    # rospy.init_node('HRIDM2TaskExecution', anonymous=True)
    # pub1 = rospy.Publisher('HRIDM2_taskExec', HRIDM2TaskExecution, queue_size=10)

    # rate = rospy.Rate(0.5)  # t=1/f, where f =0.5 <-- rospyRate
    try:
        native_sender()
        # rospy.spin()
    except rospy.ROSInterruptException:
        pass
