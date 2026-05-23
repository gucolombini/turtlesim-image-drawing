import rclpy
from rclpy.node import Node

from turtlesim.srv import TeleportAbsolute, SetPen, TeleportRelative

class TurtleController(Node):
    def __init__(self, turtle_name="turtle1"):
        super().__init__("turtle_controller")

        self.teleport_client = self.create_client(
            TeleportAbsolute,
            f"/{turtle_name}/teleport_absolute"
        )

        self.pen_client = self.create_client(
            SetPen,
            f"/{turtle_name}/set_pen"
        )

        self.teleport_relative_client = self.create_client(
            TeleportRelative,
            f"/{turtle_name}/teleport_relative"
        )

        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for teleport service...")

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for set_pen service...")

    def teleport(self, x, y, theta=0.0):
        request = TeleportAbsolute.Request()
        request.x = float(x)
        request.y = float(y)
        request.theta = float(theta)

        future = self.teleport_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def teleport_relative(self, lin, ang=0.0):
        request = TeleportRelative.Request()
        request.linear = float(lin)
        request.angular = float(ang)

        future = self.teleport_relative_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def pen_up(self):
        request = SetPen.Request()
        request.r = 0
        request.g = 0
        request.b = 0
        request.width = 1
        request.off = 1

        future = self.pen_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def pen_down(self, r=255, g=255, b=255, width=3):
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = 0

        future = self.pen_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)


def main():
    rclpy.init()

    turtle = TurtleController()

    turtle.pen_up()
    turtle.teleport(2.0, 2.0)

    turtle.pen_down(255, 0, 0, 5)
    turtle.teleport(8.0, 8.0)

    turtle.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()