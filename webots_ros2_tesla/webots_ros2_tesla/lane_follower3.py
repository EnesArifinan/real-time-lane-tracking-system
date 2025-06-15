#!/usr/bin/env python3
import cv2
import numpy as np
import rclpy
from sensor_msgs.msg import Image
from ackermann_msgs.msg import AckermannDrive
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy
from rclpy.node import Node

CONTROL_COEFFICIENT = 0.005

class LaneFollower(Node):
    def __init__(self):
        super().__init__('lane_follower_visual')
        # Publisher
        self.__ackermann_publisher = self.create_publisher(AckermannDrive, 'cmd_ackermann', 1)
        # Subscriber
        qos = qos_profile_sensor_data
        qos.reliability = QoSReliabilityPolicy.RELIABLE
        self.create_subscription(Image, 'vehicle/camera/image_color', self.__on_camera_image, qos)

        # OpenCV pencerelerini oluştur
        cv2.namedWindow("Mask",    cv2.WINDOW_NORMAL)
        cv2.namedWindow("Overlay", cv2.WINDOW_NORMAL)
        cv2.startWindowThread()

    def __on_camera_image(self, msg: Image):
        frame = np.frombuffer(msg.data, dtype=np.uint8)\
                  .reshape((msg.height, msg.width, 4))
        #roi = frame[:, :, :]
        #roi = frame[160:190, :, :]
        roi = frame[160:210, :, :]
        #roi = frame[480:570, :, :]

        rgb = cv2.cvtColor(roi, cv2.COLOR_RGBA2RGB)
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

        mask_yellow = cv2.inRange(hsv,
                        np.array([50,110,150]),
                        np.array([120,255,255]))
        mask_white = cv2.inRange(hsv,
                        np.array([0,  0, 200]),
                        np.array([180,30,255]))

        # Beyaz çizgileri daha düzgün hale getirmek için dilatasyon ve erozyon uyguluyoruz
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
        dilated_mask = cv2.dilate(mask_white, kernel, iterations=2)
        eroded_mask = cv2.erode(dilated_mask, kernel, iterations=2)

        # Sarı ve beyaz maskeleri birleştir
        combined_mask = cv2.bitwise_or(mask_yellow, eroded_mask)
        
        contours, _ = cv2.findContours(
            combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

   
        valid = [c for c in contours if cv2.contourArea(c) > 50]

        overlay = rgb.copy()
        center_x = center_y = None

        if len(valid) >= 2:
            centers = []
            for c in valid:
                M = cv2.moments(c)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    centers.append((cx, cy, c))

            centers.sort(key=lambda x: x[0])
            left_cx, left_cy, left_cnt  = centers[0]
            right_cx, right_cy, right_cnt = centers[-1]
            center_x = (left_cx + right_cx) // 2
            center_y = (left_cy + right_cy) // 2

            # Çizgileri ve merkezi çiz
            cv2.drawContours(overlay, [left_cnt, right_cnt], -1, (0,255,0), 2)
            cv2.circle(overlay, (left_cx, left_cy), 5, (0,0,255), -1)
            cv2.circle(overlay, (right_cx, right_cy), 5, (0,0,255), -1)
            cv2.circle(overlay, (center_x, center_y), 5, (255,0,0), -1)

        cv2.imshow("Mask",    combined_mask)
        cv2.imshow("Overlay", overlay)
        cv2.waitKey(1)

        cmd = AckermannDrive()
        cmd.speed = 50.0 
        cmd.steering_angle = 0.0
        if center_x is not None:
            error = center_x - (overlay.shape[1]//2)
            cmd.steering_angle = error * CONTROL_COEFFICIENT
        self.__ackermann_publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = LaneFollower()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
