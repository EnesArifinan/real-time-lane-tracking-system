#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDrive
import threading
import sys
import select
import termios
import tty

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        # Publisher: /cmd_ackermann topiğine AckermannDrive tipinde mesaj
        self.pub = self.create_publisher(AckermannDrive, '/cmd_ackermann', 10)

        # Başlangıç değerleri
        self.speed = 0.0               # m/s
        self.steering_angle = 0.0      # rad
        self.speed_step = 5          # her ok basışında 0.5 m/s artış/azalış
        self.angle_step = 0.1          # her ok basışında 0.1 rad artış/azalış
        self.speed_limit = 50.0         # maksimum hız
        self.angle_limit = 1.0         # maksimum direksiyon açısı

        # Sabit frekansta yayın yapmak için timer (10 Hz)
        self.create_timer(0.1, self.publish_command)

        # Klavye dinleme işlevini ayrı bir thread'de çalıştır
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.keyboard_thread = threading.Thread(target=self.keyboard_loop, daemon=True)
        self.keyboard_thread.start()

    def publish_command(self):
        msg = AckermannDrive()
        msg.speed = self.speed
        msg.steering_angle = self.steering_angle
        # (opsiyonel) ivme ve jerk de kullanılabilir:
        # msg.acceleration = 0.0
        # msg.jerk = 0.0
        self.pub.publish(msg)

    def keyboard_loop(self):
        # Terminali raw moda al
        tty.setraw(sys.stdin.fileno())
        try:
            while rclpy.ok():
                # 100 ms bekleyip klavye girişi var mı diye kontrol et
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch == '\x03':  # Ctrl-C
                        break
                    # Ok tuşları ESC [ A/B/C/D şeklinde gelir
                    if ch == '\x1b':
                        seq = sys.stdin.read(2)
                        if seq == '[A':       # yukarı oku: hız artır
                            self.speed = min(self.speed + self.speed_step, self.speed_limit)
                        elif seq == '[B':     # aşağı oku: hız azalt (geri de olabilir)
                            self.speed = max(self.speed - self.speed_step, -self.speed_limit)
                        elif seq == '[C':     # sağ oku: sağa dönüş (negatif açı)
                            self.steering_angle = min(self.steering_angle + self.angle_step, self.angle_limit)
                        elif seq == '[D':     # sol oku: sola dönüş (pozitif açı)
                            self.steering_angle = max(self.steering_angle - self.angle_step, -self.angle_limit)

                    elif ch == ' ':         # boşluk: dur
                        self.speed = 0.0
                        self.steering_angle = 0.0
        finally:
            # Terminal ayarlarını geri yükle
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            # ROS 2'yi kapat
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
