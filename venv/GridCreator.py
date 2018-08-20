import GridWriter
import ExcelParser
import os
import shutil
import sys
import errno
import time
from openpyxl import load_workbook

def make_clean_dir(output_dir):
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    print('Look in ' + output_dir)
    for i in range(2):
        try:
            os.mkdir(output_dir)
            break
        except OSError as os_error:
            if os_error.errno != errno.EACCES:
                raise
            pass
        print('.')
        time.sleep(0.3)
    return output_dir


def make_activity_characteristics(grid):
    activity_map = {}
    for activity in grid:
        activity_map[activity['Activity Identifier']] = {'mandatory': activity['mandatory']}
    return activity_map

def generate_grid(curriculum_excel, raw_material_dir, output_dir):
    output_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(curriculum_excel))[0])
    make_clean_dir(output_dir)
    print("Opening " + curriculum_excel)
    w = load_workbook(curriculum_excel)
    chapter_activities = []
    for sheet_name in w.sheetnames:
        grid = ExcelParser.forge_grid(w[sheet_name])
        chapter_activities.append({'chapter_name': sheet_name, 'activities': make_activity_characteristics(grid)})
        GridWriter.forge_milestone_grid(grid, sheet_name, raw_material_dir, os.path.join(output_dir, sheet_name))
    GridWriter.write_chapter_activities(chapter_activities, raw_material_dir, output_dir)

if len(sys.argv) == 4:
    generate_grid(curriculum_excel=sys.argv[1],
                  raw_material_dir = sys.argv[2], output_dir=sys.argv[3])
else:
    print('Grid creator\nUsage: ' + sys.argv[0] + ' <excel filename> <raw material dir> <output dir>')
