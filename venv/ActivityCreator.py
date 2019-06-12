import ExcelParser
import ActivityWriter
import Compressor
from sheet_reader import get_sheetreader
import ActivitySheetParser
import sys
import os
import json
from pathlib import Path
import shutil
import time
import errno


def make_clean_content_folder(directory_name):
    if os.path.isdir(directory_name):
        shutil.rmtree(directory_name)
    print('Look in ' + directory_name)
    for i in range(2):
        try:
            os.makedirs(directory_name, exist_ok=True)
            break
        except FileExistsError:
            pass
        except OSError as os_error:
            if os_error.errno != errno.EACCES:
                raise
            pass
        print('.')
        time.sleep(0.3)
    return directory_name


def make_activity_in_content_folder(raw_materials_dir, content_folder_name, pics_to_sounds, activity):
    activity_writer = ActivityWriter.ActivityWriter(pics_to_sounds)
    activity_writer.write_tap_listen(raw_materials_dir, os.path.join(content_folder_name, activity['activity folder']), activity)


def parse_and_make_activities(raw_materials_dir, sheet_id, pics_sounds_excel, output_dir):
    reader = get_sheetreader()
    row_reader = ActivitySheetParser.RowReader(reader, sheet_id, heading_row=1)
    if not row_reader.is_empty():
        activities = ActivitySheetParser.forge_activities(row_reader)
        pics_to_sounds = ExcelParser.pics_sounds_map(os.path.join(raw_materials_dir, pics_sounds_excel))

        content_folder_name = make_clean_content_folder(output_dir)
        for activity in activities:
            make_activity_in_content_folder(raw_materials_dir, content_folder_name, pics_to_sounds, activity)
            Compressor.compress_path(content_folder_name)
    else:
        print('Sheet is empty')


if len(sys.argv) == 5:
    parse_and_make_activities(raw_materials_dir=sys.argv[1], sheet_id=sys.argv[2],
                                    pics_sounds_excel=sys.argv[3], output_dir=sys.argv[4])
else:
    print("Activity creator\nUsage: " + sys.argv[0] +
          " <raw materials dir> <tap-and-listen sheet-id> <pics-and-sounds excel filename> <target output dir>\n")
