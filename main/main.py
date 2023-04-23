from detector import Detector
from tracker import Tracker
from manipulations_detector import ManipulationsDetector
from utils.constants import *
from utils.path_resolver import absolute_path
from video_processor import VideoProcessor
from video_processor import get_video_name
from utils.video_paths_collector import VideoPathsCollector
from utils.excel_writer import ExcelWriter
import json

# Initialize Videos Collector
video_paths_collector = VideoPathsCollector(path_to_videos)
# Initialize Excel Writer
excel_writer = ExcelWriter("C:\\Users\\iskan\\PycharmProjects\\ObjectDetectionAndTracking\\resources\\results.xlsx")


if __name__ == '__main__':
    videos_paths = video_paths_collector.collect()
    all_manipulations = {}
    all_logs = {}
    for video_path in videos_paths:
        # Initialize YOLO Object Detector
        detector = Detector(weights_path, cfg_path, classes_path)
        # Initialize Deep Sort Tracker
        tracker = Tracker(encoder_model_path)

        video_processor = VideoProcessor(video_path, 5000)
        tracks_per_frame, size_x, size_y = video_processor.process_video(0, detector, tracker)

        manipulations_detector = ManipulationsDetector(tracks_per_frame, size_x, size_y)
        manipulations, logs = manipulations_detector.detect_manipulations(65)
        print('Manipulations on ', video_path, ':\n', manipulations)
        all_manipulations[get_video_name(video_path)] = manipulations
        all_logs[get_video_name(video_path)] = logs
    if len(all_manipulations) != 0:
        ExcelWriter.write(excel_writer, all_manipulations, False)
        with open(absolute_path(manipulations_detection_result_path), "w") as write_file:
            json.dump(all_manipulations, write_file)
        print(all_manipulations)

