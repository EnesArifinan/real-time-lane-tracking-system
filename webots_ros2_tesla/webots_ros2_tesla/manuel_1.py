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
        self.pub = self.create_publisher(AckermannDrive, '/cmd_ackermann', 10)

        # Başlangıç değerleri
        self.speed = 0.0               # m/s
        self.steering_angle = 0.0      # rad
        self.speed_step = 10          # her tuşta 0.5 m/s artış/azalış
        self.angle_step = 0.1          # her tuşta 0.1 rad artış/azalış
        self.speed_limit = 500.0        # maksimum hız
        self.angle_limit = 1.0         # maksimum direksiyon açısı

        # 10 Hz yayın
        self.create_timer(0.1, self.publish_command)

        # Klavye dinleme thread’i
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.keyboard_thread = threading.Thread(target=self.keyboard_loop, daemon=True)
        self.keyboard_thread.start()

    def publish_command(self):
        msg = AckermannDrive()
        msg.speed = self.speed
        msg.steering_angle = self.steering_angle
        self.pub.publish(msg)

    def keyboard_loop(self):
        tty.setraw(sys.stdin.fileno())
        try:
            while rclpy.ok():
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch == '\x03':  # Ctrl-C
                        break

                    # Arrow keys
                    if ch == '\x1b':
                        seq = sys.stdin.read(2)  # e.g. "[A", "[B", "[C", "[D"
                        if seq == '[A':      # ↑
                            self.speed = min(self.speed + self.speed_step, self.speed_limit)
                        elif seq == '[B':    # ↓
                            self.speed = max(self.speed - self.speed_step, -self.speed_limit)
                        elif seq == '[C':    # →
                            self.steering_angle = min(self.steering_angle + self.angle_step, self.angle_limit)
                        elif seq == '[D':    # ←
                            self.steering_angle = max(self.steering_angle - self.angle_step, -self.angle_limit)

                    # WASD controls (case-insensitive)
                    elif ch.lower() == 'w':
                        self.speed = min(self.speed + self.speed_step, self.speed_limit)
                    elif ch.lower() == 's':
                        self.speed = max(self.speed - self.speed_step, -self.speed_limit)
                    elif ch.lower() == 'd':
                        self.steering_angle = min(self.steering_angle + self.angle_step, self.angle_limit)
                    elif ch.lower() == 'a':
                        self.steering_angle = max(self.steering_angle - self.angle_step, -self.angle_limit)

                    # Boşluk: dur
                    elif ch == ' ':
                        self.speed = 0.0
                        self.steering_angle = 0.0

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
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
