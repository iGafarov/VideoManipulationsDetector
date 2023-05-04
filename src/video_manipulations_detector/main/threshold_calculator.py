class ThresholdCalculator:
    def __init__(self, true_manipulations, result_manipulations):
        self.true_manipulations = true_manipulations
        self.result_manipulations = result_manipulations

    def calculate_percent_via_neyman_pearson(self, expected_percent):
        # TODO: dodelat
        neyman_pearson_percent = 0.0
        return neyman_pearson_percent

    def manipulations_formation_with_threshold(self, threshold_percent: float):
        all_manipulations_with_threshold = {}
        for video_name in self.result_manipulations.keys():
            manipulations = self.result_manipulations[video_name]
            manipulations_with_threshold = []
            for manipulation in manipulations:
                frame, percent = manipulation
                if percent >= threshold_percent:
                    manipulations_with_threshold.append((frame, percent))
            all_manipulations_with_threshold[video_name] = manipulations_with_threshold

        return all_manipulations_with_threshold
