from src.video_manipulations_detector.utils.path_resolver import absolute_path

PATH_TO_VIDEOS = absolute_path("utils/video_paths").__str__()
# Requirements for Object Detector
WEIGHTS_PATH = absolute_path("dnn_model/yolov4.weights").__str__()
CFG_PATH = absolute_path("dnn_model/yolov4.cfg").__str__()
CLASSES_PATH = absolute_path("dnn_model/classes.txt").__str__()
# Requirements for Object Tracker
ENCODER_MODEL_PATH = absolute_path("model_data/mars-small128.pb").__str__()
# Result files
EXCEL_RESULTS_PATH = absolute_path("results/results.xlsx").__str__()
MANIPULATIONS_DETECTION_RESULT_PATH = absolute_path("results/json_results.json").__str__()
TRUE_MANIPULATIONS_PATH = absolute_path("results/true_results.json").__str__()
GRAPH_PATH = absolute_path("results/graphs").__str__()

