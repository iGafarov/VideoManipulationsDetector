import os

import xlsxwriter


class ExcelWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, all_manipulations: dict, remove_last_results: bool):
        if remove_last_results:
            os.remove(self.output_path)
        workbook = xlsxwriter.Workbook(self.output_path)
        worksheet = workbook.add_worksheet()
        i = 0
        for video_name in all_manipulations.keys():
            manipulations = all_manipulations[video_name]
            worksheet.write(0, 0 + i, video_name)
            worksheet.write(0, 1 + i, 'frames')
            worksheet.write(0, 2 + i, 'percent')
            j = 0
            if manipulations is None:
                continue
            for manipulation in manipulations:
                prev_frame, cur_frame, percent = manipulation
                frames = '(%d - %d)' % (prev_frame, cur_frame)
                worksheet.write(1 + j, 1 + i, frames)
                worksheet.write(1 + j, 2 + i, percent)
                j += 1
            i += 3
        workbook.close()
