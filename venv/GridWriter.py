import GridHTMLPieces
import ChapterSelectorPieces
import SetOfSubPieces
import shutil
import os
import json
from urllib.parse import quote

grid_images_to_copy = ['map_paper.png', 'link1to1.png', 'link1to2.png', 'link1to3.png', 'link2to1.png', 'link3to1.png']
chapter_images_to_copy = ['chapter_icon.png', 'chapter_current.png', 'chapter_done.png', 'chapter_inprogress.png', 'chapter_pending.png']

def copy_files(images_to_copy, from_dir, to_dir):
    for image_filename in images_to_copy:
        shutil.copyfile(os.path.join(from_dir, image_filename), os.path.join(to_dir, image_filename))

def copy_activity_folder(activities_dir, activity_identifier, target_dir):
    copied_files = []
    for file_entry in os.listdir(activities_dir):
        activity_path = os.path.join(activities_dir, file_entry)
        if file_entry == activity_identifier or file_entry.startswith(activity_identifier + '.'):
            shutil.copytree(activity_path, os.path.join(target_dir, file_entry))
            copied_files.append(file_entry)
        elif os.path.isdir(activity_path):
            sub_copied_files = copy_activity_folder(activity_path, activity_identifier, target_dir)
            for file in sub_copied_files:
                copied_files.append(file)
    return copied_files

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

def write_pre_activity_links(html_file, lcm_of_max_rows, row_number, grid_columns, column_index):
    if column_index == 0:
        return
    if row_number == 0:
        pre_image = 'link1to' + str(len(grid_columns[column_index])) + '.png'
        html_file.write('<td rowspan="' + str(lcm_of_max_rows) + '">\n')
        html_file.write('<img src="' + pre_image + '" alt="one to x" class=linkimages>\n')
        html_file.write('</td>\n')

def write_post_activity_links(html_file, lcm_of_max_rows, row_number, grid_columns, column_index):
    if column_index == len(grid_columns) - 1:
        return
    if row_number == 0:
        post_image = 'link' + str(len(grid_columns[column_index])) + 'to1.png'
        html_file.write('<td rowspan="' + str(lcm_of_max_rows) + '">\n')
        html_file.write('<img src="' + post_image + '" alt="x to one" class=linkimages>\n')
        html_file.write('</td>\n')

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
            for i, activities in enumerate(grid_columns):
                write_pre_activity_links(html_file, lcm_of_max_rows, table_row, grid_columns, i)
                row_span = lcm_of_max_rows//len(activities)
                if table_row % row_span == 0:
                    row = table_row // row_span
                    activity_folder = activities[row]['Activity folder']
                    android_call = 'Android.startActivity'
                    copied_folders = copy_activity_folder(activities_dir, activity_folder, os.path.dirname(html_file.name))
                    if len(copied_folders) > 1:
                        android_call = 'Android.subActivity'
                        create_sub_activity_set(raw_material_dir, os.path.dirname(html_file.name),
                                                activities[row]['Display name'], activity_folder,
                                                activities[row]['Activity logo'], copied_folders)
                    if len(copied_folders) == 0:
                        print('Activity ' + activity_folder + ' not found')

                    html_file.write('<td rowspan="' + str(row_span) +
                                    '" onclick="' + android_call + '(\'' + activity_folder + '\');">\n')
                    write_image_html(html_file, activities[row]['Activity logo'],
                                     activities[row]['Display name'], raw_material_dir)
                    html_file.write('</td>\n')
                write_post_activity_links(html_file, lcm_of_max_rows, table_row, grid_columns, i)
        html_file.write('</tr>\n')
    if max([len(activities) for activities in grid_columns]) > max_rows:
        print('WARNING: number of parallel activities exceeds ' + str(max_rows))

def create_sub_activity_set(raw_material_dir, target_dir, activity_identifier, activity_folder, logo, copied_files):
    target_activity_folder = os.path.join(target_dir, activity_folder)
    logo_filename = logo + '.png'
    background_filename = "map_paper.png"
    os.mkdir(target_activity_folder)
    sub_activity_html = open(os.path.join(target_activity_folder, "index.html"), "w")
    shutil.copy(os.path.join(raw_material_dir, logo_filename), os.path.join(target_activity_folder, logo_filename))
    shutil.copy(os.path.join(raw_material_dir, background_filename), os.path.join(target_activity_folder, background_filename))
    sub_activity_html.write(SetOfSubPieces.begin_head)
    counter = 1
    for directory in copied_files:
        sub_activity_html.write('<figure><img src="' + logo_filename +
                                '" onclick="Android.startActivity(\'' + directory + '\');" alt="' + logo + '">' +
                                '<figcaption>' + activity_identifier + " (" + str(counter) + ')</figcaption></figure>\n')
        counter += 1
    sub_activity_html.write(SetOfSubPieces.tail)
    sub_activity_html.close()

def forge_milestone_grid(grid, chapter_name, raw_material_dir, activities_dir, output_dir):
    print('Making grid in ' + output_dir)
    os.mkdir(output_dir)
    html_file = open(os.path.join(output_dir, 'index.html'), 'w')
    html_file.write(GridHTMLPieces.begin_head)
    html_file.write('<body class=nomargins onload="Android.chapterEntered(\'' + chapter_name + '\');">\n')
    html_file.write('<h1  class=chapterhead><span onclick="Android.chapterSelector();">&nbsp;&#x21CB;&nbsp;&nbsp;</span>' +
                    chapter_name + '</h1>\n')
    html_file.write('<div style="overflow:auto; margin-top: 80px;">\n')
    html_file.write('<table class="grid_table">\n')
    current_activity_index = 0
    grid_columns = []
    while current_activity_index < len(grid):
        column, next_activity_index = get_grid_column(grid, current_activity_index)
        grid_columns.append(column)
        current_activity_index = next_activity_index
    write_grid_html_columns(html_file, grid_columns, raw_material_dir, activities_dir)
    html_file.write('</table>\n')
    html_file.write('</div>\n')
    html_file.write('</body>\n')
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
    chapterselector_file.write('<figure><img src="chapter_icon.png" alt="' + chapter['chapter_name'] + '">\n')
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
