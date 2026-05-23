import cv2
import os
import numpy as np
import rclpy
import turtle_artist.canny as canny
from ament_index_python.packages import get_package_share_directory

def neighbors(x, y, img):
    h, w = img.shape
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w:
                if img[nx, ny]:
                    yield nx, ny

def trace_curve(img, visited, start):
    curve = []
    stack = [start]

    while stack:
        x, y = stack.pop()

        if visited[x, y]:
            continue

        visited[x, y] = True
        curve.append((x, y))

        next_pixels = [n for n in neighbors(x, y, img) if not visited[n]]

        if next_pixels:
            stack.append(next_pixels[0])  # follow one branch

    return curve


def extract_curves(img_edges):
    visited = np.zeros_like(img_edges, dtype=bool)
    curves = []

    h, w = img_edges.shape

    for x in range(h):
        for y in range(w):
            if img_edges[x, y] and not visited[x, y]:
                curve = trace_curve(img_edges, visited, (x, y))
                if len(curve) > 1:
                    curves.append(curve)

    return curves

def to_world(x, y, shape):
    h, w = shape
    wx = (y / w) * 10
    wy = (x / h) * 10
    return wx, wy

def main():
    rclpy.init()

    from turtle_artist.turtle_controller import TurtleController

    share_dir = get_package_share_directory('turtle-artist')
    image_path = os.path.join(share_dir, 'input.jpeg')

    img = cv2.imread(image_path)
    

    turtle = TurtleController()

    sigma = 3
    success = False
    max_curves = 400
    while not success:
        print(f"Running Canny Edge Detection with Sigma = {sigma}. Aiming for < {max_curves} curves")
        img_edges = canny.edge_detector(img, sigma)
        img_edges = (img_edges > 0).astype(np.bool_)
        img_edges = np.flipud(img_edges)
        curves = extract_curves(img_edges)
        success = len(curves) < max_curves
        sigma += 1
        print(f"Found {len(curves)} curves")

    
    turtle.pen_up()

    # follow each curve
    for curve in curves:

        if len(curve) < 2:
            continue

        # move to start
        x0, y0 = curve[0]
        wx, wy = to_world(x0, y0, img_edges.shape)

        turtle.teleport(wx, wy)
        turtle.pen_down()

        # follow curve
        for x, y in curve[1:]:
            wx, wy = to_world(x, y, img_edges.shape)
            turtle.teleport(wx, wy)

        turtle.pen_up()

    turtle.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()