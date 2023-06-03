import cv2
import numpy as np
import random


def get_video_name(path: str):
    parsed = path.split("\\")
    return parsed[len(parsed) - 1]


class VideoProcessor:
    def __init__(self, video_path, colors_size):
        self.video_path = video_path
        self.colors_size = colors_size

    def calculate_colors(self):
        colors = []
        for j in range(self.colors_size):
            colors.append(((int)(random.randrange(255)), (int)(random.randrange(255)), (int)(random.randrange(255))))
        return colors

    def process_video(self, skip, object_detector, object_tracker):
        print('Starting video processing with path: ', self.video_path)
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        frame_for_save_shape = frame.copy()
        size_y, size_x, _ = frame_for_save_shape.shape
        colors_list = self.calculate_colors()
        # Dictionary of calculated tracks of each founded object
        tracks_per_frame = {}
        # Initialize frame counter
        frame_counter = 0
        while True:
            frame_counter += 1
            if not ret:
                break
            # if frame_counter > 0:
            if frame_counter > skip:
                # Detect objects on frame
                (class_ids, scores, boxes) = object_detector.detect(frame)

                detects = []
                for i in range(0, len(class_ids)):
                    # Save only Person detection info
                    if class_ids[i] == 0:
                        (x, y, w, h, s) = np.append(boxes[i], scores[i])
                        x = int(x)
                        y = int(y)
                        w = int(w)
                        h = int(h)
                        detection = [x, y, w, h, s]
                        detects.append(detection)

                object_tracker.update(frame, detects)

                # print("frame  x  y  w  h  id")

                for track in object_tracker.tracks:
                    (x1, y1, x2, y2) = track.bbox

                    x = int(x1)
                    y = int(y1)
                    w = int(x2 - x1)
                    h = int(y2 - y1)
                    id = track.track_id

                    tracked_object = {id: (x, y, w, h)}

                    if not tracks_per_frame.__contains__(frame_counter):
                        tracks_per_frame[frame_counter] = [tracked_object]
                    else:
                        tracks_per_frame[frame_counter].append(tracked_object)

                    print(frame_counter, " : ", x, y, w, h, id)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), colors_list[(int)(id)], 2)

            cv2.imshow(get_video_name(self.video_path), frame)

            ret, frame = cap.read()
            if frame_counter > skip:
                key = cv2.waitKey(1)
            else:
                key = cv2.waitKey(1)
            if key == 27:
                # print(tracks_per_frame)
                break
        cap.release()
        cv2.destroyAllWindows()
        return tracks_per_frame, size_x, size_y
