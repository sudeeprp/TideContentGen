import ExcelParser
import ActivityWriter
import GridWriter
import sys
import os
from pathlib import Path
import shutil
import time
import errno


def make_clean_content_folder(excel_filename):
    content_folder_name = Path(sys.argv[1]).resolve().stem
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


def make_activity_in_content_folder(content_folder_name, activity):
    if activity['type'].startswith('take'):
        shutil.copytree(activity['activity id'], content_folder_name + '/' + activity['activity id'])
        shutil.copyfile(activity['logo'], content_folder_name + '/' + activity['activity id'] + '/' + activity['logo'])
    else:
        activity_writer = ActivityWriter.ActivityWriter()
        activity_writer.write_tap_listen(content_folder_name + '/' + activity['activity id'], activity)


def parse_excel_and_make_content(excel_filename):
    milestones = ExcelParser.forge_milestones(excel_filename)
    content_folder_name = make_clean_content_folder(sys.argv[1])
    for milestone in milestones:
        for activity in milestone['activities']:
            make_activity_in_content_folder(content_folder_name, activity)
    GridWriter.forge_grid(milestones, content_folder_name)


if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " excel-file\n")
else:
    parse_excel_and_make_content(sys.argv[1])
