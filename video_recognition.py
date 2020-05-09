from imageai.Detection import VideoObjectDetection
import cv2
import os


class VideoRecognition:

    def __init__(self, output_video, input_video=0, type='fromVideo'):
        self.execution_path = os.getcwd()
        self.detector = VideoObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(self.execution_path, "resnet50_coco_best_v2.0.1.h5"))
        self.detector.loadModel()
        self.start_process(output_video=output_video, input_video=input_video, type=type)
        self.count = 0
        self.text = []
        print(self.video_path)

    def start_process(self, output_video, input_video, type):
        if type == 'fromvideo':
            self.video_path = self.detector.detectObjectsFromVideo(
                input_file_path=os.path.join(self.execution_path, input_video),
                output_file_path=os.path.join(self.execution_path, output_video),
                frames_per_second=10,
                per_second_function=self.forSeconds,
                log_progress=True,
                minimum_percentage_probability=50
            )
        else:
            self.camera = cv2.VideoCapture(input_video)
            self.video_path = self.detector.detectObjectsFromVideo(
                camera_input=self.camera,
                output_file_path=os.path.join(self.execution_path, output_video),
                frames_per_second=10,
                per_second_function=self.forSeconds,
                log_progress=True,
                minimum_percentage_probability=50)

    def forSeconds(self, second_number, output_arrays, count_arrays, average_output_count):
        text_file = open('res.txt', 'a')
        print("SECOND : ", second_number)
        print("Array for the outputs of each frame ", output_arrays, file=text_file)
        print("Array for output count for unique objects in each frame : ", count_arrays, file=text_file)
        print("Output average count for unique objects in the last second: ", average_output_count, file=text_file)
        counter = 0
        if self.count / 5 == 0:
            for el in output_arrays[1]:
                if counter == 0:
                    counter += 1
                    pass#self.text.append(' ', el['name'], ' ')
                    continue
                pass#self.text.append('and ', el['name'], ' ')
        print("------------END OF A SECOND --------------")



