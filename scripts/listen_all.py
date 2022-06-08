#!/usr/bin/env python

import rospy, sys
from std_msgs.msg import String
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM

#  fiware imports
sys.path.append("humanRob_ws/src/fiware")
from fiware_v2.forthHRIHealthPost import HRI_HealthStatePost as healthState_spam


def callback1(data):
    print('callback____1')
    rospy.loginfo('receiving message %s', data.error_type)
    if data.result == True:
        print ("peirame TRUE")
        rospy.loginfo('we got Truesszz')
        newtask = HRIDM2TaskExecution()
        newtask.action = 'next_task111111'
        rospy.loginfo(newtask)
    else:
        print('FALSE')
        newtask = HRIDM2TaskExecution()
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
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback1)
    rospy.Subscriber('HRIDM2_taskExec', HRIDM2TaskExecution, callback2)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)
    # healthState_spam()
    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
