#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from beginner_tutorials.msg import HRIDM2TaskExecution, TaskExecution2HRIDM

global rate


def send_msg():
    task_exec = TaskExecution2HRIDM()
    task_exec.request_id = 0
    task_exec.result = True
    task_exec.error_type = 'Something went wrong'
    rospy.loginfo(task_exec)
    pub.publish(task_exec)


def native_sender():
    global pub
    rospy.loginfo('sender node starter')
    # init the 1st publisher  or init the first pub-in
    rospy.init_node('TaskExecution2HRIDM', anonymous=True)
    pub = rospy.Publisher('taskExecution', TaskExecution2HRIDM, queue_size=10)
    rate = rospy.Rate(0.5)  # t=1/f, where f =0.5 <-- rospyRate
    # for debug, we use a print
    print('sends the first message')
    send_msg()
    return pub


if __name__ == '__main__':
    try:
        native_sender()
    except rospy.ROSInterruptException:
        pass
