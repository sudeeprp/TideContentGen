import GridWriter
import ExcelParser
import os
import shutil
import sys
import errno
import time

def make_clean_dir(output_dir, milestone_name):
    milestone_dir = os.path.join(output_dir, milestone_name)
    if os.path.isdir(milestone_dir):
        shutil.rmtree(milestone_dir)
    print('Look in ' + milestone_dir)
    for i in range(2):
        try:
            os.mkdir(milestone_dir)
            break
        except OSError as os_error:
            if os_error.errno != errno.EACCES:
                raise
            pass
        print('.')
        time.sleep(0.3)
    return milestone_dir


def generate_grid(curriculum_excel, milestone_name, raw_material_dir, output_dir):
    milestone_dir = make_clean_dir(output_dir, milestone_name)
    grid = ExcelParser.forge_grid(curriculum_excel, milestone_name)
    GridWriter.forge_milestone_grid(grid, milestone_name, raw_material_dir, milestone_dir)


if len(sys.argv) == 5:
    generate_grid(curriculum_excel=sys.argv[1], milestone_name=sys.argv[2],
                  raw_material_dir = sys.argv[3], output_dir=sys.argv[4])
else:
    print('Grid creator\nUsage: ' + sys.argv[0] + ' <excel filename> <milestone name> <raw material> <output dir>')
