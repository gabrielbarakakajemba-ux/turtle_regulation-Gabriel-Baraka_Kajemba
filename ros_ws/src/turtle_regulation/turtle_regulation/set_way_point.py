import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import math

class WaypointNode(Node):
    def __init__(self):
        super().__init__('set_way_point') 
        
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.moving_pub = self.create_publisher(Bool, 'is_moving', 10)
        
        self.waypoint = (7.0, 7.0)
        self.pose = None
        
        self.kp = 2.0  
        self.kpl = 0.5 
        self.distance_tolerance = 0.1 

    def pose_callback(self, msg):
        self.pose = msg
        self.compute_commands()

    def compute_commands(self):
        if self.pose is None:
            return
        
        distance = math.sqrt((self.waypoint[0] - self.pose.x)**2 + (self.waypoint[1] - self.pose.y)**2)
        el = distance 
        
    
        moving_msg = Bool()
        moving_msg.data = distance > self.distance_tolerance
        self.moving_pub.publish(moving_msg)

        cmd = Twist()

        if distance > self.distance_tolerance:
            theta_desired = math.atan2(self.waypoint[1] - self.pose.y, self.waypoint[0] - self.pose.x)
            error = math.atan2(math.sin(theta_desired - self.pose.theta), math.cos(theta_desired - self.pose.theta))
            cmd.angular.z = self.kp * error
            cmd.linear.x = self.kpl * el
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
