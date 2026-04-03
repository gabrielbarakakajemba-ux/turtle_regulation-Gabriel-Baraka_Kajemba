import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class WaypointNode(Node):
    def __init__(self):
        super().__init__('set_way_point')
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        self.waypoint = (7.0, 7.0)
        self.pose = None
        self.kp = 2.0 
    def pose_callback(self, msg):
        self.pose = msg
        self.compute_commands()

    def compute_commands(self):
        if self.pose is None:
            return
        

        theta_desired = math.atan2(self.waypoint[1] - self.pose.y, self.waypoint[0] - self.pose.x)
        
        error = math.atan2(math.sin(theta_desired - self.pose.theta), math.cos(theta_desired - self.pose.theta))
        u = self.kp * error
        
        cmd = Twist()
        cmd.angular.z = u
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNode()
    rclpy.spin(node)
    rclpy.shutdown()