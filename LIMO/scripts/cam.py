#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class CameraSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        rospy.init_node('camera_subscriber', anonymous=True)
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback)
        self.should_close = False  # Flag to indicate whether to close the window

    def image_callback(self, data):
        if self.should_close:
            return

        try:
            # Convert the ROS Image message to a format OpenCV can use
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))
            return

        # Display the image
        cv2.imshow("Camera Feed", cv_image)
        # Wait for a short period to allow image to be displayed
        key = cv2.waitKey(3)
        # Check if 'q' key is pressed to set the flag to close the window
        if key == ord('q'):
            self.should_close = True
            rospy.signal_shutdown("User requested shutdown")

    def start(self):
        rospy.spin()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        camera_subscriber = CameraSubscriber()
        camera_subscriber.start()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()

