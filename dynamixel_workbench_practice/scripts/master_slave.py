#!/usr/bin/env python
import rospy

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from dynamixel_workbench_msgs.srv import DynamixelCommand
from dynamixel_workbench_msgs.srv import DynamixelCommandResponse

# Publisher
joint_traj_pub = rospy.Publisher('/dynamixel_workbench/joint_trajectory', JointTrajectory, queue_size=125)

# count
count = 0

# subscribe joint states and call dynamixel command service.
def joint_states_callback(msg):

    # count += 1

    position = msg.position[0] - msg.position[1]
    print "%s" % position
    print "pan: %s" % msg.position[0]
    print "tilt: %s" % msg.position[1]

    traj = JointTrajectory()

    traj.header.seq = msg.header.seq
    traj.header.stamp = rospy.Time.now()
    traj.header.frame_id = msg.header.frame_id

    print "%s" % traj.header.seq

    traj.joint_names = range(1)
    traj.joint_names = ['tilt']

    point = JointTrajectoryPoint()
    point.positions = range(1)
    point.positions = [position]
    point.time_from_start = rospy.Duration.from_sec(0.0125)

    traj.points = range(1)
    traj.points = [point]

    joint_traj_pub.publish(traj)

    rate = rospy.Rate(100)
    rate.sleep()

if __name__ == "__main__":

    # initialize node
    rospy.init_node('dynamixel_command_client')

    # turn off torque of master (id=1)
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:
        service = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        response = service('', 1, 'Torque_Enable', 0)
        print response.comm_result
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
        # return DynamixelCommandResponse

    # subscriber
    joint_states_sub = rospy.Subscriber('/dynamixel_workbench/joint_states', JointState, joint_states_callback, queue_size=125)

    # Spin
    rospy.spin()

    # ROS loop
    rate = rospy.Rate(125)
    while not rospy.is_shutdown():
        rate.sleep()