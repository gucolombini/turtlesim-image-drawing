import cv2
import os
import turtle_artist.canny as canny
from ament_index_python.packages import get_package_share_directory
import rclpy

def main():
    rclpy.init()

    from turtle_artist.turtle_controller import TurtleController

    share_dir = get_package_share_directory('turtle-artist')
    image_path = os.path.join(share_dir, 'input.jpeg')

    img = cv2.imread(image_path)
    img_edges = canny.edge_detector(img)
    img_stepx = 10/len(img[0])
    img_stepy = 10/len(img)

    turtle = TurtleController()

    i = 0
    while i < len(img_edges):
        j = 0
        while j < len(img_edges[0]):
            if img_edges[i][j]:
                turtle.teleport(i*img_stepx, j*img_stepy)
                turtle.pen_down()
                turtle.teleport_relative(img_stepx)
                turtle.pen_up()
            print(f'x: {i}, y: {j}')
            j += 1
        i += 1

    turtle.destroy_node()
    rclpy.shutdown()






