from src.video_manipulations_detector.utils.constants import *
from src.video_manipulations_detector.utils.video_paths_collector import VideoPathsCollector
from src.video_manipulations_detector.utils.excel_writer import ExcelWriter
from src.video_manipulations_detector.object_detection_tracking.detector import Detector
from src.video_manipulations_detector.object_detection_tracking.tracker import Tracker
from video_processor import VideoProcessor
from video_processor import get_video_name
from manipulations_detector import ManipulationsDetector
import json
import time

# Initialize Videos Collector
video_paths_collector = VideoPathsCollector(PATH_TO_VIDEOS)
# Initialize Excel Writer
excel_writer = ExcelWriter(EXCEL_RESULTS_PATH)


if __name__ == '__main__':
    videos_paths = video_paths_collector.collect()
    all_manipulations = {}
    # all_logs = {}
    each_video_time = []
    start = time.time()
    for video_path in videos_paths:
        # Initialize YOLO Object Detector
        detector = Detector(WEIGHTS_PATH, CFG_PATH, CLASSES_PATH)
        # Initialize Deep Sort Tracker
        tracker = Tracker(ENCODER_MODEL_PATH)

        video_processor = VideoProcessor(video_path, 5000)
        tracks_per_frame, size_x, size_y = video_processor.process_video(0, detector, tracker)

        manipulations_detector = ManipulationsDetector(tracks_per_frame, size_x, size_y)
        manipulations = manipulations_detector.detect_manipulations(65)
        print('Manipulations on ', video_path, ':\n', manipulations)
        all_manipulations[get_video_name(video_path)] = manipulations
        # all_logs[get_video_name(video_path)] = logs
        # print('LOGS: ', logs)
    end = time.time()
    general_time = end - start
    print('general_time: ', general_time)
    if len(all_manipulations) != 0:
        ExcelWriter.write(excel_writer, all_manipulations, False)
        with open(MANIPULATIONS_DETECTION_RESULT_PATH, "w") as write_file:
            json.dump(all_manipulations, write_file)
        print(all_manipulations)


