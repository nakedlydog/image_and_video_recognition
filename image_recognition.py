from imageai.Detection import ObjectDetection
import os


exec_path = os.getcwd()


detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(
    exec_path, 'yolo.h5'
))
detector.loadModel()

detections = detector.detectObjectsFromImage(
    input_image=os.path.join(exec_path, 'objects.jpg'),
    output_image_path=os.path.join(exec_path, 'new_objects.jpg'),
    minimum_percentage_probability=80
)

for eachObject in detections:
    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    print("--------------------------------")