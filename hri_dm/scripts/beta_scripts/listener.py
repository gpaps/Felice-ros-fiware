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

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy, sys
from std_msgs.msg import String
# fiware imports
# sys.path.append("humanRob_ws/src/fiware")
from src.hri_dm.scripts.fiware_v2.forthHRIHealthPost import HRI_HealthStatePost, HRI_Health
robotAction_jsonFName = r"/home/gpaps/humanRob_ws/src/beginner_tutorials/scripts/fiware_v2/health.json"
address = "25.45.111.204"
port = 1026

def check_callB(data):
    # this makes the response to what I've listened # function apeires
    global count
    rospy.loginfo('I took..> %s', data.data)
    string_ = 'kati_pira___' + str(count)
    pub.publish(string_)
    rospy.loginfo(string_)
    count = count + 1
    # stacked callback --> callback after callback
    # check_callBA

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listenerWhom', anonymous=True)
    rospy.Subscriber('chatterFORTH', String, check_callB)

    # rospy.Subscriber('chatter', String, callback)
    # dikos mou
    # rospy.Subscriber('native_chatter', String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def check_callBA(data):
    rospy.loginfo('I took..> %s', data.data)
    # this makes the response to what I listened
    #function apeires
    string_ = 'eipa kai egw thn dikia mou - 3'+str(count)
    pub.publish(string_)
    rospy.loginfo(string_)

if __name__ == '__main__':
    count = 0
    pub = rospy.Publisher('native_chatter', String, queue_size=10)
    # robotAction_jsonFName = 'health.json'
    HRI_HealthStatePost(address, port, robotAction_jsonFName)

    listener()
