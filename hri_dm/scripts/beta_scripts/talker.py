#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

from hri_dm.msg import info
from src.hri_dm.scripts.beta_scripts.listener import *

def msg_me():
    print('msg_me')
    msg_info = info()
    msg_info.name = 'ICS'
    msg_info.name2 = 'FORTH'
    msg_info.age = 8
    msg_info.score = 99
    msg_info.a = 1234567890
    msg_info.b = 1234567890.1234567890

    rospy.loginfo(msg_info)
    pub.publish(msg_info.name)
    print('end')

def talker():
    rospy.init_node('talker_Gpaps', anonymous=True)
    rate = rospy.Rate(0.5)  # 10hz t=1/f

    string_ = 'ROS Knowledge(talker)'
    pub.publish(string_)
    rospy.loginfo(string_)
    # fcn
    msg_me()
    listener()

    rate.sleep()
    # rospy.spin()

        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        # pub.publish(hello_str)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    # rospy.init_node('listener_2', anonymous=True)
    rospy.Subscriber('native_chatter', String, check_callBA)
    string_ = 'listener2_SPEAKS'
    pub.publish(string_)
    rospy.loginfo(string_)
    # rospy.spin()  # spin() simply keeps python from exiting until this node is stopped


if __name__ == '__main__':

    pub = rospy.Publisher('chatterFORTH', String, queue_size=10)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
