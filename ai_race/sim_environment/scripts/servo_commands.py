#!/usr/bin/env python
import rospy
import time
import dynamic_reconfigure.client
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

flag_move = 0

pub_vel_left_rear_wheel = None
pub_vel_right_rear_wheel = None
pub_vel_left_front_wheel = None
pub_vel_right_front_wheel = None
pub_pos_left_steering_hinge = None
pub_pos_right_steering_hinge = None

Max_steer_angle = float(25)/float(180)*3.1415

dynamic_client = None
max_speed_coeff = 1.0

def dynamic_recon_callback(config):
    rospy.loginfo("Config set to {max_speed_coeff}".format(**config))
    global max_speed_coeff
    max_speed_coeff = config.max_speed_coeff

def set_throttle_steer(data):

    global flag_move
    global pub_vel_left_rear_wheel
    global pub_vel_right_rear_wheel
    global pub_vel_left_front_wheel
    global pub_vel_right_front_wheel
    global pub_pos_left_steering_hinge
    global pub_pos_right_steering_hinge
    global Max_steer_angle
    global max_speed_coeff

    throttle = max_speed_coeff * data.linear.x / (0.032*2*3.14) * 3.14 *2
    if data.angular.z > Max_steer_angle:
        steer = Max_steer_angle
    elif data.angular.z < -Max_steer_angle:
        steer = -Max_steer_angle
    else :
        steer = data.angular.z

    pub_vel_left_rear_wheel.publish(throttle)
    pub_vel_right_rear_wheel.publish(throttle)
    pub_vel_left_front_wheel.publish(throttle)
    pub_vel_right_front_wheel.publish(throttle)
    pub_pos_left_steering_hinge.publish(steer)
    pub_pos_right_steering_hinge.publish(steer)

def servo_commands():
    global pub_vel_left_rear_wheel
    global pub_vel_right_rear_wheel
    global pub_vel_left_front_wheel
    global pub_vel_right_front_wheel
    global pub_pos_left_steering_hinge
    global pub_pos_right_steering_hinge
    global dynamic_client

    time.sleep(2)
    rospy.init_node('servo_commands', anonymous=True)

    pub_vel_left_rear_wheel = rospy.Publisher('/rear_left_wheel_velocity_controller/command', Float64, queue_size=1)
    pub_vel_right_rear_wheel = rospy.Publisher('/rear_right_wheel_velocity_controller/command', Float64, queue_size=1)
    pub_vel_left_front_wheel = rospy.Publisher('/front_left_wheel_velocity_controller/command', Float64, queue_size=1)
    pub_vel_right_front_wheel = rospy.Publisher('/front_right_wheel_velocity_controller/command', Float64, queue_size=1)

    pub_pos_left_steering_hinge = rospy.Publisher('/front_left_hinge_position_controller/command', Float64, queue_size=1)
    pub_pos_right_steering_hinge = rospy.Publisher('/front_right_hinge_position_controller/command', Float64, queue_size=1)
    rospy.Subscriber("/cmd_vel", Twist, set_throttle_steer)
    try:
        dynamic_client = dynamic_reconfigure.client.Client("dynamic_recon_server_node", timeout=30, config_callback=dynamic_recon_callback)
    except rospy.exceptions.ROSException as e:
        print("dynamic_recon_server_node not found, do nothing")

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        servo_commands()
    except rospy.ROSInterruptException:
        pass
