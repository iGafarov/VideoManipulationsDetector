import json
import numpy as np
from src.video_manipulations_detector.utils.constants import MANIPULATIONS_DETECTION_RESULT_PATH
from src.video_manipulations_detector.utils.constants import TRUE_MANIPULATIONS_PATH
from src.video_manipulations_detector.utils.constants import GRAPH_PATH
import matplotlib.pyplot as plt


def calculate_confusion_matrix(result_frames: list, true_frames: list):
    confusion_matrix = np.zeros((2, 2), dtype=int)
    TN, TP, FP, FN = 0, 0, 0, 0
    for i in range(0, len(result_frames)):
        if result_frames[i] > 0:
            if true_frames[i] > 0:
                TP += 1
            else:
                FP += 1
        else:
            if true_frames[i] > 0:
                FN += 1
            else:
                TN += 1
    confusion_matrix[1, 1] = TN
    confusion_matrix[0, 0] = TP
    confusion_matrix[0, 1] = FP
    confusion_matrix[1, 0] = FN
    return confusion_matrix


def calculate_frame_with_accuracy(frame: int):
    accuracy = 5
    frame_with_accuracy = []

    left = frame - accuracy
    right = frame + accuracy
    if left < 0:
        left = 0
    for i in range(left, right + 1):
        frame_with_accuracy.append(i)

    return frame_with_accuracy


def zeros_appending(result_frames: list, true_frames: list):
    matched_count = 0
    matched_frames = []

    for result_frame in result_frames:
        for accuracy_frame in calculate_frame_with_accuracy(result_frame):
            if true_frames.__contains__(accuracy_frame):
                result_frames[result_frames.index(result_frame)] = accuracy_frame
                matched_frames.append(accuracy_frame)
                matched_count += 1
                break

    missing_on_result = true_frames.copy()
    missing_on_true = result_frames.copy()

    for matched_frame in matched_frames:
        missing_on_result.remove(matched_frame)
        missing_on_true.remove(matched_frame)

    for missing in missing_on_result:
        result_frames.append(missing)
    for missing in missing_on_true:
        true_frames.append(missing)

    calculated_result_frames = sorted(result_frames)
    calculated_true_frames = sorted(true_frames)

    index = 0
    for result_frame in calculated_result_frames:
        if missing_on_result.__contains__(result_frame):
            calculated_result_frames[index] = 0
        index += 1

    index = 0
    for true_frame in calculated_true_frames:
        if missing_on_true.__contains__(true_frame):
            calculated_true_frames[index] = 0
        index += 1

    return calculated_result_frames, calculated_true_frames


def draw_graph(matrix_list: list):
    TPR = []
    FPR = []
    index = 0
    for matrix in matrix_list:
        # if index == 13:
        #     break
        TN = matrix[1, 1]
        TP = matrix[0, 0]
        FP = matrix[0, 1]
        FN = matrix[1, 0]
        if TP == 0:
            TPR.append(0.0)
        else:
            TPR.append(TP / (TP + FN))
        if FP == 0:
            FPR.append(0.0)
        else:
            FPR.append(FP / (TN + FP))
        index += 1
    plt.plot(FPR, TPR)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    graph_path = GRAPH_PATH + '\\' + 'roc_auc' + '.png'
    plt.savefig(graph_path)
    print('FPR: ', FPR)
    print('TPR: ', TPR)


if __name__ == '__main__':
    with open(MANIPULATIONS_DETECTION_RESULT_PATH, "r") as results_file:
        all_manipulations = json.load(results_file)
        with open(TRUE_MANIPULATIONS_PATH, "r") as true_results_file:
            all_true_manipulations = json.load(true_results_file)
            error_matrix_list = []
            for video_name in all_manipulations.keys():
                manipulations = all_manipulations[video_name]
                true_frames = all_true_manipulations[video_name]
                result_frames = []
                for manipulation in manipulations:
                    prev_frame, _, _ = manipulation
                    result_frames.append(prev_frame + 1)
                result_frames, true_frames = zeros_appending(result_frames, true_frames)
                error_matrix = calculate_confusion_matrix(result_frames, true_frames)
                print(video_name + ': \n', error_matrix)
                error_matrix_list.append(error_matrix)
            draw_graph(error_matrix_list)
        print('prikol')
