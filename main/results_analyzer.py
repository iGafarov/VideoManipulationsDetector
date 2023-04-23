import json
import numpy as np
from utils.constants import MANIPULATIONS_DETECTION_RESULT_PATH
from utils.constants import TRUE_MANIPULATIONS_PATH


def calculate_confusion_matrix(result_frames: list, true_frames: list):
    confusion_matrix = np.zeros((2, 2), dtype=int)
    TN, TP, FP, FN = 0, 0, 0, 0
    for i in range(0, len(result_frames) - 1):
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
    confusion_matrix[1][1] = TN
    confusion_matrix[0, 0] = TP
    confusion_matrix[0, 1] = FP
    confusion_matrix[1, 0] = FN
    return confusion_matrix


def zeros_appending(result_frames: list, true_frames: list):
    matched_count = 0
    matched_frames = []
    for result_frame in result_frames:
        if true_frames.__contains__(result_frame):
            matched_frames.append(result_frame)
            matched_count += 1

    missing_on_result = true_frames.copy()
    missing_on_true = result_frames.copy()
    for matched_frame in matched_frames:
        missing_on_result.remove(matched_frame)
        missing_on_true.remove(matched_frame)

    # result_size = len(true_frames) - matched_count + len(result_frames)
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


if __name__ == '__main__':
    with open(MANIPULATIONS_DETECTION_RESULT_PATH, "r") as results_file:
        all_manipulations = json.load(results_file)
        with open(TRUE_MANIPULATIONS_PATH, "r") as true_results_file:
            all_true_manipulations = json.load(true_results_file)
            for video_name in all_manipulations.keys():
                manipulations = all_manipulations[video_name]
                true_frames = all_true_manipulations[video_name]
                result_frames = []
                for manipulation in manipulations:
                    prev_frame, _, _ = manipulation
                    result_frames.append(prev_frame + 1)
                result_frames, true_frames = zeros_appending(result_frames, true_frames)
                matrix = calculate_confusion_matrix(result_frames, true_frames)
                print(matrix)
        print('prikol')
