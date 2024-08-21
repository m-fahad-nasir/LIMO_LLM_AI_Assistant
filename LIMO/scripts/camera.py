#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class CameraSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        rospy.init_node('camera_subscriber', anonymous=True)
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)

    def image_callback(self, data):
        try:
            # Convert the ROS Image message to a format OpenCV can use
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))

        # Display the image
        cv2.imshow("Camera Feed", cv_image)
        cv2.waitKey(3)
	        

    def start(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        camera_subscriber = CameraSubscriber()
        camera_subscriber.start()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()

