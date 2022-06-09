#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from beginner_tutorials.msg import HRIDM2TaskExecution, TaskExecution2HRIDM
# from listenerSubscriber import receiver, callback

global result

def callback(data):
    print('callback')
    rospy.loginfo('receiving message', data.data)
    send_msg()

def init_receiver():
    print('init_receiver always awaits.. .')
    rospy.init_node('receiver')
    rospy.loginfo('receiver node started')
    rospy.Subscriber('taskExecution', TaskExecution2HRIDM, callback)
    rospy.spin()

def listener():
    rospy.Subscriber(TaskExecution2HRIDM)
    if result == 1:
        string_ = 'next_action'
        pub2.publish(string_)
        rospy.loginfo(string_)

def send_msg():
    task_exec = TaskExecution2HRIDM()
    task_exec.request_id = 0
    task_exec.result = True
    task_exec.error_type = 'NavigationFailed'
    rospy.loginfo(task_exec)
    pub.publish(task_exec)


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
    pub2.publish(task_exec2)


def native_sender():
    rospy.loginfo('sender node starter')
    # for debug, we use a print
    print('sends the first message')
    result = 1
    pub.publish(result)
    rospy.loginfo(result)
    # send_msg()
    # rospy.loginfo(send_msg())


if __name__ == '__main__':
    # init the 1st publisher  or init the first pub-in
    rospy.init_node('TaskExecution2HRIDM', anonymous=True)
    pub = rospy.Publisher('taskExec_2HRIDM', TaskExecution2HRIDM, queue_size=10)

    rospy.init_node('HRIDM2TaskExecution', anonymous=True)
    pub2 = rospy.Publisher('HRIDM2_taskExec', HRIDM2TaskExecution, queue_size=10)

    rate = rospy.Rate(0.5)  # t=1/f, where f =0.5 <-- rospyRate

    try:
        native_sender()
    except rospy.ROSInterruptException:
        pass
