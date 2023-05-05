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


EXPECTED_ALL_MANIPULATIONS_PERCENT = 80


def collect_frames_counts():
    video_paths_collector = VideoPathsCollector(PATH_TO_VIDEOS)
    frames_numbers = {}
    for video_path in video_paths_collector.collect():
        cap = cv2.VideoCapture(video_path)
        frames_count = 0
        if cap.isOpened:
            frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_numbers[get_video_name(video_path)] = frames_count
    return frames_numbers


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


def draw_error_matrices(error_matrices: dict):
    for video_name in error_matrices.keys():
        print(video_name + ': \n', error_matrices[video_name])


if __name__ == '__main__':
    all_result_manipulations = {}
    all_true_manipulations = {}
    frames_counts = collect_frames_counts()

    with open(MANIPULATIONS_DETECTION_RESULT_PATH, "r") as results_file:
        all_result_manipulations = json.load(results_file)
    with open(TRUE_MANIPULATIONS_PATH, "r") as true_results_file:
        all_true_manipulations = json.load(true_results_file)

    # Initialize Threshold Calculator
    threshold_calculator = ThresholdCalculator(all_true_manipulations, all_result_manipulations, frames_counts)
    # Parameter of Neyman Pearson algorithm
    # means the percentage of real Manipulations, at which we will get the threshold for the graphs
    threshold = threshold_calculator.calculate_percent_via_neyman_pearson(EXPECTED_ALL_MANIPULATIONS_PERCENT)
    print('Neyman-Pearson threshold: ', threshold)

    all_result_manipulations_with_threshold = threshold_calculator.manipulations_formation_with_threshold(threshold)

    # Draw manipulations graphs of all videos
    draw_graphs(all_result_manipulations, all_true_manipulations, frames_counts)
    # Draw error matrices of featured dictionary of manipulations
    error_matrix_dict = calculate_error_matrices(
        all_result_manipulations_with_threshold, all_true_manipulations, frames_counts)
    draw_error_matrices(error_matrix_dict)
