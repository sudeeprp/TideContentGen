from continue_copy import continue_copy
import os
import sys


def write_local_info(localinfo_dir, output_dir):
    continue_copy(os.path.join(localinfo_dir, "display names of grades.json"), output_dir)
    continue_copy(os.path.join(localinfo_dir, "display names of subjects.json"), output_dir)

def write_content_description(output_dir):
    content_description = '{"content_version": "8 loca stat"}'
    print("Packaging: " + content_description)
    content_desc_file = open(output_dir + '/content_descriptor.json', 'w')
    content_desc_file.write(content_description)
    content_desc_file.close()

def get_grade_set(parentdir):
    grade_set = []
    subdirs = [entry for entry in os.listdir(parentdir) if os.path.isdir(os.path.join(parentdir, entry))]
    for dir_entry in subdirs:
        dir_pieces = dir_entry.split('_')
        if len(dir_pieces) > 1 and dir_pieces[0].isdigit():
            grade_set.append(str(dir_pieces[0]))
    return grade_set

def write_grade_backgrounds(raw_material_dir, output_parent):
    grade_set = get_grade_set(output_parent)
    for grade in grade_set:
        grade_resource = "grade" + grade + '_logo.png'
        continue_copy(os.path.join(raw_material_dir, grade_resource), os.path.join(output_parent, grade_resource))


if len(sys.argv) == 4:
    output_dir = sys.argv[3]
    write_grade_backgrounds(raw_material_dir=sys.argv[1], output_parent=output_dir)
    write_local_info(localinfo_dir=sys.argv[2], output_dir=output_dir)
    write_content_description(output_dir)
    print("Package done.")
else:
    print('Grid packager\nUsage: ' + sys.argv[0] + ' <raw material dir> <localinfo dir> <output dir>')
