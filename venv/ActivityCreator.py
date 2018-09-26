import ExcelParser
import ActivityWriter
import GridWriter
import Compressor
import sys
import os
from pathlib import Path
import shutil
import time
import errno


def make_clean_content_folder(output_dir, excel_filename):
    content_folder_name = os.path.join(output_dir, Path(excel_filename).resolve().stem)
    if os.path.isdir(content_folder_name):
        shutil.rmtree(content_folder_name)
    print('Look in ' + content_folder_name)
    for i in range(2):
        try:
            os.mkdir(content_folder_name)
            break
        except OSError as os_error:
            if os_error.errno != errno.EACCES:
                raise
            pass
        print('.')
        time.sleep(0.3)
    return content_folder_name


def make_activity_in_content_folder(content_folder_name, pics_to_sounds, activity):
    activity_writer = ActivityWriter.ActivityWriter(pics_to_sounds)
    activity_writer.write_tap_listen(os.path.join(content_folder_name, activity['Activity folder']), activity)


def parse_excel_and_make_activities(excel_filename, pics_sounds_excel, output_dir):
    activities = ExcelParser.forge_activities(excel_filename)
    pics_to_sounds = ExcelParser.pics_sounds_map(pics_sounds_excel)

    content_folder_name = make_clean_content_folder(output_dir, excel_filename)
    for activity in activities:
        make_activity_in_content_folder(content_folder_name, pics_to_sounds, activity)
        Compressor.compress_path(content_folder_name)


if len(sys.argv) == 4:
    parse_excel_and_make_activities(excel_filename=sys.argv[1], pics_sounds_excel=sys.argv[2], output_dir=sys.argv[3])
else:
    print("Activity creator\nUsage: " + sys.argv[0] + " <excel filename> <pics and sounds excel> <output dir>\n")
