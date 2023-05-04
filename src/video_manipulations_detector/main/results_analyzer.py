import json
import cv2
from src.video_manipulations_detector.utils.constants import MANIPULATIONS_DETECTION_RESULT_PATH
from src.video_manipulations_detector.utils.constants import TRUE_MANIPULATIONS_PATH
from src.video_manipulations_detector.utils.constants import GRAPH_PATH
from src.video_manipulations_detector.utils.constants import PATH_TO_VIDEOS
from src.video_manipulations_detector.utils.video_paths_collector import VideoPathsCollector
from src.video_manipulations_detector.main.video_processor import get_video_name
import matplotlib.pyplot as plt
from threshold_calculator import ThresholdCalculator
from src.video_manipulations_detector.utils.results_analyzer_helper import *


def collect_frames_counts():
    video_paths_collector = VideoPathsCollector(PATH_TO_VIDEOS)
    frames_counts = {}
    for video_path in video_paths_collector.collect():
        cap = cv2.VideoCapture(video_path)
        frames_count = 0
        if cap.isOpened:
            frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_counts[get_video_name(video_path)] = frames_count
    return frames_counts


# def draw_graph(matrix_list: list):
#     TPR = []
#     FPR = []
#     index = 0
#     for matrix in matrix_list:
#         # if index == 13:
#         #     break
#         TN = matrix[1, 1]
#         TP = matrix[0, 0]
#         FP = matrix[0, 1]
#         FN = matrix[1, 0]
#         if TP == 0:
#             TPR.append(0.0)
#         else:
#             TPR.append(TP / (TP + FN))
#         if FP == 0:
#             FPR.append(0.0)
#         else:
#             FPR.append(FP / (TN + FP))
#         index += 1
#     plt.plot(FPR, TPR)
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     graph_path = GRAPH_PATH + '\\' + 'roc_auc' + '.png'
#     plt.savefig(graph_path)
#     print('FPR: ', FPR)
#     print('TPR: ', TPR)

# def draw_roc_auc(pred, true, name):
#     print('y_pred: ', pred)
#     print('y_true: ', true)
#     fpr, tpr, threshold = roc_curve(true, pred)
#     roc_auc_score(true, pred)
#     plt.plot(fpr, tpr)
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     graph_path = GRAPH_PATH + '\\rocauc\\' + name + '_roc_auc' + '.png'
#     print(name, '-auc: ', roc_auc_score(y_true, y_pred))
#     plt.savefig(graph_path)
#     plt.close()


def draw_graph(pred, name, frames_number):
    frames = []
    for i in range(0, frames_number):
        frames.append(i)
    graph_path = GRAPH_PATH + '\\graph\\' + name + '.png'
    plt.title('Video forgery')
    plt.xlabel('Frame Number')
    plt.ylabel('Manipulations Percent')
    plot_name = graph_path
    plt.plot(frames, pred)
    plt.savefig(plot_name)
    plt.close()


def draw_graphs(result_manipulations: dict, true_manipulations: dict, frames_numbers):
    for video_name in result_manipulations.keys():
        manipulations = result_manipulations[video_name]
        true_frames = true_manipulations[video_name]
        y_pred, y_true = calculate_samples_with_percent(manipulations, true_frames, frames_numbers[video_name])
        draw_graph(y_pred, video_name, frames_numbers[video_name])
        # print('y_pred: ', y_pred)
        # print('y_true: ', y_true)


def draw_error_matrices(result_manipulations: dict, true_manipulations: dict, frames_numbers):
    for video_name in result_manipulations.keys():
        manipulations = result_manipulations[video_name]
        true_frames = true_manipulations[video_name]
        result_frames = []
        for manipulation in manipulations:
            frame, percent = manipulation
            contains = False
            for result_frame in calculate_frame_with_accuracy(frame):
                if result_frames.__contains__(result_frame):
                    contains = True
            if not contains:
                result_frames.append(frame)
        y_pred, y_true = zeros_appending(result_frames, true_frames, frames_numbers[video_name])
        # print('y_pred: ', y_pred)
        # print('y_true: ', y_true)
        error_matrix = calculate_confusion_matrix(y_pred, y_true, frames_numbers[video_name])
        print(video_name + ': \n', error_matrix)


if __name__ == '__main__':
    all_result_manipulations = {}
    all_true_manipulations = {}
    frames_counts = collect_frames_counts()
    with open(MANIPULATIONS_DETECTION_RESULT_PATH, "r") as results_file:
        all_result_manipulations = json.load(results_file)
    with open(TRUE_MANIPULATIONS_PATH, "r") as true_results_file:
        all_true_manipulations = json.load(true_results_file)

    # Initialize Threshold Calculator
    threshold_calculator = ThresholdCalculator(all_true_manipulations, all_result_manipulations)
    # Parameter of Neyman Pearson algorithm
    # means the percentage of real Manipulation, at which we will get the threshold for the graph
    expected_all_manipulations_percent = 80
    percent = threshold_calculator.calculate_percent_via_neyman_pearson(expected_all_manipulations_percent)

    all_result_manipulations_with_threshold = threshold_calculator.manipulations_formation_with_threshold(60)

    # Draw manipulations graphs of all videos
    draw_graphs(all_result_manipulations, all_true_manipulations, frames_counts)
    # Draw error matrices of featured dictionary of manipulations
    draw_error_matrices(all_result_manipulations_with_threshold, all_true_manipulations, frames_counts)


    # with open(MANIPULATIONS_DETECTION_RESULT_PATH, "r") as results_file:
    #     all_manipulations = json.load(results_file)
    #     with open(TRUE_MANIPULATIONS_PATH, "r") as true_results_file:
    #         all_true_manipulations = json.load(true_results_file)
    #         error_matrix_list = []
    #         frames_counts = collect_frames_counts()
    #         y_preds = []
    #         y_trues = []
    #         for video_name in all_manipulations.keys():
    #             manipulations = all_manipulations[video_name]
    #             true_frames = all_true_manipulations[video_name]
    #             if len(manipulations) < frames_counts[video_name] - frames_counts[video_name] / 2:
    #                 result_frames = []
    #                 for manipulation in manipulations:
    #                     frame, percent = manipulation
    #                     contains = False
    #                     for result_frame in calculate_frame_with_accuracy(frame):
    #                         if result_frames.__contains__(result_frame):
    #                             contains = True
    #                     if not contains:
    #                         result_frames.append(frame)
    #                 y_pred, y_true = zeros_appending(result_frames, true_frames, frames_counts[video_name])
    #                 print('y_pred: ', y_pred)
    #                 print('y_true: ', y_true)
    #                 error_matrix = calculate_confusion_matrix(y_true, y_pred, frames_counts[video_name])
    #                 print(video_name + ': \n', error_matrix)
    #                 error_matrix_list.append(error_matrix)
    #             else:
    #                 # y_pred = np.zeros(frames_counts[video_name])
    #                 # for manipulation in manipulations:
    #                 #     frame, percent = manipulation
    #                 #     if frame == 3:
    #                 #         y_pred.append(0.0)
    #                 #         y_pred.append(0.0)
    #                 #     y_pred.append(percent)
    #                 y_pred, y_true = calculate_samples_with_percent(manipulations, true_frames, frames_counts[video_name])
    #                 draw_graph(y_pred, video_name, frames_counts[video_name])
    #                 # draw_roc_auc(y_pred, y_true, video_name)
    #                 y_preds.append(y_pred)
    #                 y_trues.append(y_true)
    #                 print('y_pred: ', y_pred)
    #                 print('y_true: ', y_true)
    #         y_true_general = []
    #         y_pred_general = []
    #         for y_true in y_trues:
    #             for percent in y_true:
    #                 y_true_general.append(percent)
    #
    #         for y_pred in y_preds:
    #             for percent in y_pred:
    #                 y_pred_general.append(percent)
    #         draw_roc_auc(y_pred_general, y_true_general, 'general')
    #     print('prikol')
