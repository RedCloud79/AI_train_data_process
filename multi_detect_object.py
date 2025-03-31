import rospy
import cv2
import torch
from ultralytics import YOLO
from geometry_msgs.msg import Point
from yolov8_ros.msg import DetectObject, DetectObjectArray
import rospkg

class YOLODetectorROS:
    def __init__(self):
        rospy.init_node('fire_detect_ros')

        rospack = rospkg.RosPack()
        pkg_path = rospack.get_path('yolov8_ros')
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        rospy.loginfo(f'Using device: {self.device}')

        self.model_path_1 = f"{pkg_path}/model/train76/weights/best.pt"
        self.model_path_2 = f"{pkg_path}/model/train70/weights/best.pt"
        self.model_path_3 = f"{pkg_path}/model/train72/weights/best.pt"

        self.model_1 = YOLO(self.model_path_1).to(self.device)
        self.model_2 = YOLO(self.model_path_2).to(self.device)
        self.model_3 = YOLO(self.model_path_3).to(self.device)
        
        self.classes_of_interest_1 = {'fire', 'smoke'}
        self.classes_of_interest_2 = {'person'}
        self.classes_of_interest_3 = {'car'}

        self.detect_pub = rospy.Publisher("/detected_objects", DetectObjectArray, queue_size=10)
        self.capture = cv2.VideoCapture("rtsp://admin:irop2020@192.168.1.108/cam/realmonitor?channel=1&subtype=1")
        self.rate = rospy.Rate(30)
        self.confidence_threshold = 0.2

    def process_model_results(self, results, model, classes_of_interest):
        detect_object_array = DetectObjectArray()
        if hasattr(results, 'boxes') and results.boxes is not None:
            boxes = results.boxes.data
            if len(boxes) > 0:
                for box in boxes:
                    confidence = float(box[4])
                    if confidence >= self.confidence_threshold:
                        class_id = int(box[5])
                        class_name = model.names[class_id]

                        if class_name in classes_of_interest:
                            x1, y1, x2, y2 = map(int, box[:4])
                            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2

                            object_msg = DetectObject()
                            object_msg.object_x = center_x
                            object_msg.object_y = center_y
                            object_msg.object_name = class_name
                            detect_object_array.objects.append(object_msg)
        
        if detect_object_array.objects:
            self.detect_pub.publish(detect_object_array)
        else:
            rospy.loginfo("No object detected")

    def process_frame(self, frame):
        results_1 = self.model_1(frame)[0]
        self.process_model_results(results_1, self.model_1, self.classes_of_interest_1)
        
        results_2 = self.model_2(frame)[0]
        self.process_model_results(results_2, self.model_2, self.classes_of_interest_2)
        
        results_3 = self.model_3(frame)[0]
        self.process_model_results(results_3, self.model_3, self.classes_of_interest_3)

    def run(self):
        while not rospy.is_shutdown():
            ret, frame = self.capture.read()
            if ret:
                self.process_frame(frame)
            self.rate.sleep()


def main():
    yolo_detector = YOLODetectorROS()
    yolo_detector.run()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()