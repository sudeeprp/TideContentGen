import GridHTMLPieces
import ChapterSelectorPieces
import shutil
import os
import json
from urllib.parse import quote

grid_images_to_copy = ['pencil.png']
chapter_images_to_copy = ['pencil.png', 'chapter_current.png', 'chapter_done.png', 'chapter_inprogress.png', 'chapter_pending.png']

def copy_files(images_to_copy, from_dir, to_dir):
    for image_filename in images_to_copy:
        shutil.copyfile(os.path.join(from_dir, image_filename), os.path.join(to_dir, image_filename))

def copy_activity_folder(activities_dir, activity_identifier, target_dir):
    copied_target = None
    for file_entry in os.listdir(activities_dir):
        activity_path = os.path.join(activities_dir, file_entry)
        if file_entry == activity_identifier:
            shutil.copytree(activity_path, os.path.join(target_dir, file_entry))
            copied_target = target_dir
            break
        elif os.path.isdir(activity_path):
            copied_target = copy_activity_folder(activity_path, activity_identifier, target_dir)
            if copied_target != None:
                break
    return copied_target

#TODO: Remove this
'''def form_activity_layout(html_file, activities):
    html_file.write('<tr class="activity_list">\n')
    for activity in activities:
        html_file.write('<td>\n')
        html_file.write('<a href="' + quote(activity['activity id'] + '/' + 'index.html') + '">')
        html_file.write('<figure>\n')
        html_file.write('<img src="' + quote(activity['activity id'] + '/' + activity['logo']) +
                        '" alt="Tab activity">\n')
        html_file.write('<figcaption>' + activity['activity name'] + '</figcaption>\n')
        html_file.write('</figure>\n')
        html_file.write('</a>')
        html_file.write('</td>\n')
    html_file.write('</tr>\n')


def forge_grid(milestones, content_folder_name):
    html_file = open(content_folder_name + '/' + content_folder_name + '.html', 'w')
    html_file.write(GridHTMLPieces.begin_head)
    html_file.write('<table class="grid_table">\n')
    for milestone in milestones:
        html_file.write('<tr class="milestone_head">\n')
        html_file.write('<td colspan=4>' + milestone['milestone name'] + ' (cmd = ' + str(milestone['cmd']) + ')</td>\n')
        html_file.write('</tr>\n')
        form_activity_layout(html_file, milestone['activities'])
    html_file.write('</table>\n')
    html_file.write(GridHTMLPieces.tail)
    html_file.close()
'''

def is_enrichment_remedial_pair(current_sequence, next_sequence):
    return ((current_sequence[0].lower().startswith('enrichment')) and
            (next_sequence[0].lower().startswith('remedial'))) \
            or \
            ((current_sequence[0].lower().startswith('remedial')) and
             (next_sequence[0].lower().startswith('enrichment')))

def sequence_break(current_sequence, next_sequence):
    sequence_is_broken = True
    if (len(current_sequence) > 2) and (len(next_sequence) > 2):
        if (current_sequence[0] == next_sequence[0]) and (current_sequence[1] == next_sequence[1]):
            sequence_is_broken = False
    elif is_enrichment_remedial_pair(current_sequence, next_sequence):
        sequence_is_broken= False
    return sequence_is_broken

def get_grid_column(grid, start_activity_index):
    current_activity_index = start_activity_index
    next_activity_index = current_activity_index + 1
    grid_column = [grid[current_activity_index]]
    while next_activity_index < len(grid):
        if not sequence_break(grid[current_activity_index]['sequence'], grid[next_activity_index]['sequence']):
            grid_column.append(grid[next_activity_index])
            current_activity_index = next_activity_index
            next_activity_index = current_activity_index + 1
        else:
            break
    return grid_column, next_activity_index


def write_image_html(html_file, image_name, caption, raw_material_dir):
    image_filename = image_name + '.png'
    html_file.write('<figure><img src="' + quote(image_filename) + '"' +
                    ' alt="' + image_name + '">\n')
    shutil.copyfile(os.path.join(raw_material_dir, image_filename),
                    os.path.join(os.path.dirname(html_file.name), image_filename))
    html_file.write('<figcaption>' + caption + '</figcaption></figure>\n')


def write_grid_html_columns(html_file, grid_columns, raw_material_dir, activities_dir):
    max_rows = 4
    lcm_of_max_rows = 12
    filled_rows_in_lcm = []
    for column in grid_columns:
        for i in range(0, lcm_of_max_rows, lcm_of_max_rows//len(column)):
            filled_rows_in_lcm.append(i)
    for table_row in range(lcm_of_max_rows):
        html_file.write('<tr>\n')
        if table_row in filled_rows_in_lcm:
            for activities in grid_columns:
                row_span = lcm_of_max_rows//len(activities)
                if table_row % row_span == 0:
                    row = table_row // row_span
                    html_file.write('<td rowspan="' + str(row_span) +
                                    '" onclick="Android.startActivity(\'' + activities[row]['Activity Identifier'] +
                                    '\');">\n')
                    #html_file.write('<a href="' +
                    #                quote(activities[row]['Activity Identifier'] + '/' + 'index.html') + '">\n')
                    write_image_html(html_file, activities[row]['Activity logo'],
                                     activities[row]['Display name'], raw_material_dir)
                    copy_target = copy_activity_folder(activities_dir, activities[row]['Activity Identifier'], os.path.dirname(html_file.name))
                    if copy_target == None:
                        print('Activity ' + activities[row]['Activity Identifier'] + ' not found')
                    #html_file.write('</a>')
                    html_file.write('</td>\n')
        html_file.write('</tr>\n')
    if max([len(activities) for activities in grid_columns]) > max_rows:
        print('WARNING: number of parallel activities exceeds ' + str(max_rows))


def forge_milestone_grid(grid, chapter_name, raw_material_dir, activities_dir, output_dir):
    print('Making grid in ' + output_dir)
    os.mkdir(output_dir)
    html_file = open(os.path.join(output_dir, 'index.html'), 'w')
    html_file.write(GridHTMLPieces.begin_head)
    html_file.write('<body onload="Android.chapterEntered(\'' + chapter_name + '\')">')
    html_file.write(GridHTMLPieces.body_table_start)
    html_file.write('<h1>' + chapter_name + '</h1>')
    html_file.write('<table class="grid_table">\n')
    current_activity_index = 0
    grid_columns = []
    while current_activity_index < len(grid):
        column, next_activity_index = get_grid_column(grid, current_activity_index)
        grid_columns.append(column)
        current_activity_index = next_activity_index
    write_grid_html_columns(html_file, grid_columns, raw_material_dir, activities_dir)
    html_file.write('</table>\n')
    html_file.write(GridHTMLPieces.body_table_end)
    html_file.write('</body>')
    html_file.write(GridHTMLPieces.tail)
    html_file.close()
    copy_files(grid_images_to_copy, raw_material_dir, output_dir)

def write_chapter_row(chapterselector_file, chapter):
    chapterselector_file.write('<tr>\n')
    chapterselector_file.write('<td class="chapter_cell" style="width:2cm; text-align:center;">\n')
    chapterselector_file.write('<img id=' + chapter['chapter_name'] + '.status src="chapter_pending.png" onclick="set_active_chapter(\'' + chapter['chapter_name'] + '\');" alt="Pending" style="max-width:1.5cm">')
    chapterselector_file.write('</td>\n')
    chapterselector_file.write('<td class="chapter_cell" style="width:8cm;">\n')
    chapterselector_file.write('<a href="' + chapter['chapter_name'] + '/index.html">\n')
    chapterselector_file.write('<figure><img src="pencil.png" alt="' + chapter['chapter_name'] + '">\n')
    chapterselector_file.write('<figcaption>' + chapter['chapter_name'] + '</figcaption></figure></a>\n')
    chapterselector_file.write('</td>')
    chapterselector_file.write('<td class="chapter_cell" style="height:2.5cm;">\n')
    chapterselector_file.write('<div id=' + chapter['chapter_name'] + '.students style="overflow:auto;height:100%;white-space:nowrap;"></div>')
    chapterselector_file.write('</td>\n')
    chapterselector_file.write('</tr>\n')

def chapter_array_html(chapter_activities):
    return json.dumps([chapter['chapter_name'] for chapter in chapter_activities])

def write_chapter_activity_characteristics(chapter_activities, output_dir):
    chapter_activity_file = open(os.path.join(output_dir, 'chapter_activities.json'), 'w')
    chapter_activity_file.write(json.dumps(chapter_activities))
    chapter_activity_file.close()

def write_chapter_html(chapter_activities, output_dir):
    chapterselector_file = open(os.path.join(output_dir, 'chapters.html'), 'w')
    chapterselector_file.write(ChapterSelectorPieces.begin_head)
    chapterselector_file.write(ChapterSelectorPieces.script_head)
    chapterselector_file.write('var chapters = ' + chapter_array_html(chapter_activities) + '\n')
    chapterselector_file.write(ChapterSelectorPieces.scripts)
    chapterselector_file.write(ChapterSelectorPieces.body_table_start)
    for chapter in chapter_activities:
        write_chapter_row(chapterselector_file, chapter)
    chapterselector_file.write(ChapterSelectorPieces.body_table_end)
    chapterselector_file.write(ChapterSelectorPieces.end_tail)
    chapterselector_file.close()

def write_chapter_activities(chapter_activities, raw_material_dir, output_dir):
    write_chapter_activity_characteristics(chapter_activities, output_dir)
    write_chapter_html(chapter_activities, output_dir)
    copy_files(chapter_images_to_copy, raw_material_dir, output_dir)
