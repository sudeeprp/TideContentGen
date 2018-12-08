import GridWriter
import ExcelParser
import os
import shutil
import sys
import errno
import time
from openpyxl import load_workbook

def write_content_description(output_dir):
    content_description = '{"content_version": "6 Color"}'
    content_desc_file = open(output_dir + '/content_descriptor.json', 'w')
    content_desc_file.write(content_description)
    content_desc_file.close()

def make_clean_dir(output_dir):
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    print('Look in ' + output_dir)
    for i in range(2):
        try:
            os.makedirs(output_dir)
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
        activity_map[activity['activity identifier']] = {'mandatory': activity['mandatory']}
    return activity_map

def generate_grid(curriculum_excel, raw_material_dir, activities_dir, output_parent):
    grid_output_dir = os.path.join(output_parent, os.path.splitext(os.path.basename(curriculum_excel))[0])
    make_clean_dir(grid_output_dir)
    w = load_workbook(curriculum_excel)
    chapter_activities = []
    for sheet_name in w.sheetnames:
        chapter_id = sheet_name
        chapter_name = GridWriter.html_encoded_name(w[sheet_name]['A1'].value)
        if chapter_name is not None:
            chapter_name = str(chapter_name).strip()
        else:
            chapter_name = chapter_id
        grid = ExcelParser.forge_grid(w[sheet_name])
        if grid is not None:
            chapter_activities.append({'chapter_name': chapter_name, 'chapter_id': chapter_id, 'activities': make_activity_characteristics(grid)})
            GridWriter.forge_milestone_grid(grid, chapter_name, chapter_id, raw_material_dir, activities_dir, os.path.join(grid_output_dir, chapter_id))
    GridWriter.write_chapter_activities(chapter_activities, raw_material_dir, grid_output_dir)
    write_content_description(output_parent)
    for dirName, subdirList, fileList in os.walk(output_parent):
        if dirName.lower().endswith('projectfile'):
            shutil.rmtree(dirName)
            print('deleted: %s' % dirName)

if len(sys.argv) == 5:
    generate_grid(curriculum_excel=sys.argv[1],
                  raw_material_dir=sys.argv[2], activities_dir=sys.argv[3], output_parent=sys.argv[4])
else:
    print('Grid creator\nUsage: ' + sys.argv[0] + ' <excel filename> <raw material dir> <activities dir> <output dir>')
