class ManipulationsDetector:
    def __init__(self, trajectories, size_x, size_y):
        self.trajectories = trajectories
        self.size_x = size_x
        self.size_y = size_y

    def detect_manipulations(self, manipulations_percent):
        speed_measurement = 5
        borders_fault_percent = 5
        if len(self.trajectories) != 0:
            detected_manipulations = []
            logs = []
            for frame_number in self.trajectories.keys():
                saved_ids = []

                tracks_on_current_frame = self.trajectories[frame_number]
                tracks_on_prev_frame = []
                tracks_on_prev_prev_frame = []

                prev_frame_number = frame_number - 1
                prev_prev_frame_number = frame_number - 2

                if self.trajectories.__contains__(prev_frame_number):
                    tracks_on_prev_frame = self.trajectories[prev_frame_number]
                if self.trajectories.__contains__(prev_prev_frame_number):
                    tracks_on_prev_prev_frame = self.trajectories[prev_prev_frame_number]

                if len(tracks_on_prev_prev_frame) != 0:
                    ids_on_current_frame = []
                    ids_on_prev_frame = []
                    ids_on_prev_prev_frame = []

                    for current_object in tracks_on_current_frame:
                        ids_on_current_frame.append(list(current_object.keys())[0])
                    for prev_object in tracks_on_prev_frame:
                        ids_on_prev_frame.append(list(prev_object.keys())[0])
                    for prev_prev_object in tracks_on_prev_prev_frame:
                        ids_on_prev_prev_frame.append(list(prev_prev_object.keys())[0])

                    # FIRST SITUATION
                    # Getting missing ids from prev_prev to cur frame
                    manipulated_ids = ids_on_prev_prev_frame.copy()
                    for current_id in ids_on_current_frame:
                        if ids_on_prev_prev_frame.__contains__(current_id):
                            manipulated_ids.remove(current_id)
                            # Getting saved ids from prev_prev to cur frame
                            saved_ids.append(current_id)
                    # THIRD SITUATION (BORDERS)
                    for current_id in ids_on_current_frame:
                        for track in tracks_on_prev_prev_frame:
                            if track.__contains__(current_id):
                                x_border, y_border, _, _ = track[current_id]
                                if x_border > self.size_x * ((100 - borders_fault_percent) / 100) or \
                                        y_border > self.size_y * ((100 - borders_fault_percent) / 100):
                                    if manipulated_ids.__contains__(current_id):
                                        manipulated_ids.remove(current_id)

                    # Getting saved ids from prev_prev to prev frame
                    saved_prev_ids = []
                    for prev_id in ids_on_prev_frame:
                        if ids_on_prev_prev_frame.__contains__(prev_id):
                            saved_prev_ids.append(prev_id)

                    # FOR TEST (should be empty)
                    ids_that_saved_from_prev_prev_to_prev_but_not_saved_from_prev_prev_to_cur = []
                    for test_id in saved_prev_ids:
                        if not saved_ids.__contains__(test_id):
                            ids_that_saved_from_prev_prev_to_prev_but_not_saved_from_prev_prev_to_cur.append(test_id)
                    # print('test_list: ', ids_that_saved_from_prev_prev_to_prev_but_not_saved_from_prev_prev_to_cur)

                    # SECOND SITUATION
                    for saved_id in saved_ids:
                        (av_x, av_y) = self.calculate_average_speed(saved_id)
                        (potential_x, potential_y) = (0, 0)
                        (cur_x, cur_y) = (0, 0)

                        if saved_prev_ids.__contains__(saved_id):
                            # Checking object on previous frame
                            tracks_on_potential_frame = tracks_on_prev_frame
                        else:
                            # Checking object on prev prev frame
                            tracks_on_potential_frame = tracks_on_prev_prev_frame

                        for track in tracks_on_potential_frame:
                            if track.__contains__(saved_id):
                                (potential_x, potential_y, _, _) = track[saved_id]
                                break
                        for track in tracks_on_current_frame:
                            if track.__contains__(saved_id):
                                (cur_x, cur_y, _, _) = track[saved_id]
                                break

                        if abs(cur_x - potential_x) > av_x * speed_measurement \
                                or abs(cur_y - potential_y) > av_y * speed_measurement:
                            manipulated_ids.append(saved_id)
                            # print('id: ', saved_id)
                            # print('potential_x: ', potential_x)
                            # print('cur_x: ', cur_x)
                            # print('av_x: ', av_x)
                            # print('potential_y: ', potential_y)
                            # print('cur_y: ', cur_y)
                            # print('av_y: ', av_y)
                    print('===============================================================')
                    print('FRAMES: ', prev_prev_frame_number, '-', frame_number)
                    print('Manipulated ids: ', manipulated_ids)
                    print('Prev Prev ids: ', ids_on_prev_prev_frame)
                    print('Prev ids: ', ids_on_prev_frame)
                    print('Cur ids: ', ids_on_current_frame)

                    calculated_manipulations_percent = (len(manipulated_ids) / len(ids_on_prev_prev_frame)) * 100
                    print('Calculated percent: ', calculated_manipulations_percent)
                    print('===============================================================')

                    logs.append((prev_prev_frame_number, calculated_manipulations_percent))

                    if calculated_manipulations_percent >= manipulations_percent:
                        if prev_prev_frame_number == 1 and frame_number == 3:
                            continue
                        else:
                            last_detected_id = len(detected_manipulations) - 1
                            if last_detected_id >= 0:
                                from_frame, to_frame, _ = detected_manipulations[last_detected_id]
                                if prev_prev_frame_number - from_frame == 1:
                                    detected_manipulations.pop(last_detected_id)

                            detected_manipulations.append(
                                (prev_prev_frame_number, frame_number, calculated_manipulations_percent))

                            print('DETECTEEEED')
            return detected_manipulations, logs

    def calculate_average_speed(self, object_id):
        coord_deltas = []
        first_iteration = True
        (last_x, last_y) = (0, 0)
        for tracks_on_frame in self.trajectories.values():
            for tracked in tracks_on_frame:
                if tracked.__contains__(object_id):
                    (x, y, w, h) = tracked[object_id]
                    if first_iteration:
                        (last_x, last_y) = (x, y)
                        first_iteration = False
                        break
                    coord_deltas.append((abs(x - last_x), abs(y - last_y)))
                    (last_x, last_y) = (x, y)
                    break
        sum_delta_x = 0
        sum_delta_y = 0
        for (delta_x, delta_y) in coord_deltas:
            sum_delta_x = sum_delta_x + delta_x
            sum_delta_y = sum_delta_y + delta_y
        return sum_delta_x / len(coord_deltas), sum_delta_y / len(coord_deltas)
