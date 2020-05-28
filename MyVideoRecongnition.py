from imageai.Detection import VideoObjectDetection
import cv2
import os


class MyVideoRecognition:

    def __init__(self, b_start_process, output_video, input_video, type):
        self.execution_path = os.getcwd()
        self.detector = None
        self.video_path = None
        self.camera = None
        if b_start_process:
            self.start_process(output_video, input_video, type)

    def start_process(self, output_video, input_video, type):
        self.execution_path = os.getcwd()
        self.detector = VideoObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(self.execution_path, "resnet50_coco_best_v2.0.1.h5"))
        self.detector.loadModel()

        if type == 'fromvideo':
            self.start_process_from_video(output_video, input_video)
        else:
            self.start_process_from_camera(output_video, input_video)

        print("start_process")

    def stop_process(self):
        self.detector = None


#"private" functions
    def start_process_from_video(self, output_video, input_video):
        self.video_path = self.detector.detectObjectsFromVideo(
            input_file_path=os.path.join(self.execution_path, input_video),
            output_file_path=os.path.join(self.execution_path, output_video),
            frames_per_second=10,
            per_second_function=self.forSeconds,
            log_progress=True,
            minimum_percentage_probability=50
        )

    def start_process_from_camera(self, output_video, input_video):
        self.camera = cv2.VideoCapture(input_video)
        self.video_path = self.detector.detectObjectsFromVideo(
            camera_input=self.camera,
            output_file_path=os.path.join(self.execution_path, output_video),
            frames_per_second=10,
            per_second_function=self.forSeconds,
            log_progress=True,
            minimum_percentage_probability=50)

#@todo : idl what is the purpose of this function
    def forSeconds(self, second_number, output_arrays, count_arrays, average_output_count):
        text_file = open('res.txt', 'a')
        print("SECOND : ", second_number)
        print("Array for the outputs of each frame ", output_arrays, file=text_file)
        print("Array for output count for unique objects in each frame : ", count_arrays, file=text_file)
        print("Output average count for unique objects in the last second: ", average_output_count, file=text_file)
        print("------------END OF A SECOND --------------")
