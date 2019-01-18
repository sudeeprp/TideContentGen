import GridHTMLPieces
import ChapterSelectorPieces
import SetOfSubPieces
import shutil
import os
import json
from urllib.parse import quote

grid_images_to_copy = ['map_paper.png', 'link1to1.png',
                       'link1to2.png', 'link1to3.png', 'link1to4.png',
                       'link2to1.png', 'link3to1.png', 'link4to1.png',
                       'refresh.png',
                       'chapter_none.png', 'chapter_assessment_ready.png',
                       'chapter_done.png', 'chapter_inprogress.png',
                       'chapter_pending.png', 'chapter_approved.png',
                       'chapter_to_be_done.png'
                       ]
chapter_images_to_copy = ['chapter_icon.png', 'chapter_current.png', 'chapter_none.png', 'chapter_assessment_ready.png',
                          'chapter_done.png', 'chapter_inprogress.png', 'chapter_pending.png', 'chapter_approved.png',
                          'chapter_to_be_done.png',
                          'refresh.png']

def copy_files(images_to_copy, from_dir, to_dir):
    for image_filename in images_to_copy:
        shutil.copyfile(os.path.join(from_dir, image_filename), os.path.join(to_dir, image_filename))

def copy_activity_folder(activities_dir, activity_folder, target_dir):
    copied_files = []
    directories = []
    for file_entry in os.listdir(activities_dir):
        if os.path.isdir(os.path.join(activities_dir, file_entry)):
            directories.append(file_entry)
    activity_folder_lowercase = activity_folder.lower()
    for directory_name in directories:
        activity_path = os.path.join(activities_dir, directory_name)
        if directory_name.lower() == activity_folder_lowercase or \
                 directory_name.lower().startswith(activity_folder_lowercase + '.'):
            shutil.copytree(activity_path, os.path.join(target_dir, directory_name))
            copied_files.append(directory_name)
        else:
            sub_copied_files = copy_activity_folder(activity_path, activity_folder, target_dir)
            for file in sub_copied_files:
                copied_files.append(file)
    return copied_files

def html_encoded_name(name):
    return name.encode('ascii', 'xmlcharrefreplace').decode("utf-8")

def html_encoded_id(name):
    return quote(name)

def is_enrichment_remedial_pair(current_activity, next_activity):
    return (current_activity['qualifier'] == 'enrichment' and next_activity['qualifier'] == 'reinforcement') or \
            (current_activity['qualifier'] == 'reinforcement' and next_activity['qualifier'] == 'enrichment')

def get_grid_column(grid, start_activity_index):
    current_activity_index = start_activity_index
    next_activity_index = current_activity_index + 1
    grid_column = [grid[current_activity_index]]
    while next_activity_index < len(grid):
        if grid[current_activity_index]['withnext']:
            grid_column.append(grid[next_activity_index])
            current_activity_index = next_activity_index
            next_activity_index = current_activity_index + 1
        else:
            break
    return grid_column, next_activity_index


def write_image_html(html_file, logo_name, caption, raw_material_dir):
    image_filename = logo_name + '.png'
    html_file.write('<figure><img src="' + quote(image_filename) + '"' +
                    ' alt="' + logo_name + '">\n')
    try:
        shutil.copyfile(os.path.join(raw_material_dir, image_filename),
                    os.path.join(os.path.dirname(html_file.name), image_filename))
    except FileNotFoundError:
        print(image_filename + " not found - while copying to " + os.path.dirname(html_file.name))
    html_file.write('<figcaption>' + caption + '<img id=' + html_encoded_id(logo_name + "_" + caption) +
                    '_status class=activity_status_pic></figcaption></figure>\n')

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
    activities = []
    for column in grid_columns:
        for i in range(0, lcm_of_max_rows, lcm_of_max_rows//len(column)):
            filled_rows_in_lcm.append(i)
    for table_row in range(lcm_of_max_rows):
        html_file.write('<tr>\n')
        if table_row in filled_rows_in_lcm:
            for i, activities in enumerate(grid_columns):
                write_pre_activity_links(html_file, lcm_of_max_rows, table_row, grid_columns, i)
                if len(activities) > max_rows:
                    print("ERROR: too much parallel: " + str(activities))
                row_span = lcm_of_max_rows//len(activities)
                if table_row % row_span == 0:
                    row = table_row // row_span
                    activity_folder = activities[row]['activity folder']
                    android_call = 'Android.startActivity'
                    copied_folders = []
                    if os.path.isdir(activities_dir):
                        copied_folders = copy_activity_folder(activities_dir, activity_folder, os.path.dirname(html_file.name))
                    if len(copied_folders) > 1:
                        android_call = 'Android.subActivity'
                        create_sub_activity_set(raw_material_dir, os.path.dirname(html_file.name),
                                                activities[row]['display name'], activity_folder,
                                                activities[row]['activity logo'], copied_folders)
                    ''' TODO: Put this back when cards are there, to check that no cards are missed.
                    if len(copied_folders) == 0:
                        print('<<insert activity not found message')
                    '''
                    html_file.write('<td rowspan="' + str(row_span) +
                                    '" onclick="' + android_call + '(\'' + activity_folder + '\');">\n')
                    write_image_html(html_file, activities[row]['activity logo'],
                                     activities[row]['display name'], raw_material_dir)
                    html_file.write('</td>\n')
                write_post_activity_links(html_file, lcm_of_max_rows, table_row, grid_columns, i)
        html_file.write('</tr>\n')
    if len(activities) > 0 and \
            max([len(activities) for activities in grid_columns]) > max_rows:
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

def forge_milestone_grid(grid, chapter_name, chapter_id, raw_material_dir, activities_dir, output_dir):
    os.mkdir(output_dir)
    html_filename = os.path.join(output_dir, 'index.html')
    html_file = open(html_filename, 'w')
    html_file.write(GridHTMLPieces.begin_head)
    html_file.write('<body class=nomargins onload="Android.chapterEntered(\'' + chapter_id + '\');refresh();">\n')
    html_file.write('<h1  class=chapterhead><span onclick="Android.chapterSelector();">&nbsp;&#x21CB;&nbsp;&nbsp;</span>' +
                    chapter_name + '</h1>\n')
    html_file.write('<img class=refresh_pic onclick="refresh();" src="refresh.png">\n')
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
    return html_filename

def write_chapter_row(chapterselector_file, chapter):
    chapter_name = html_encoded_name(chapter['chapter_name'])
    chapter_id = chapter['chapter_id']
    chapterselector_file.write('<tr>\n')
    chapterselector_file.write('<td class="chapter_cell" style="width:2cm; text-align:center;">\n')
    chapterselector_file.write('<img id=' + chapter_id + '.status src="chapter_pending.png" ' +
                               'onclick="set_active_chapter(\'' + chapter_id + '\');" alt="Pending" style="max-width:1.5cm">')
    chapterselector_file.write('</td>\n')
    chapterselector_file.write('<td class="chapter_icon">\n')
    chapterselector_file.write('<a href="' + chapter_id + '/index.html">\n')
    chapterselector_file.write('<figure><img src="chapter_icon.png" alt="' + chapter_name + '">\n')
    chapterselector_file.write('<figcaption class="chapter_figcaption">' + chapter_name + '</figcaption></figure></a>\n')
    chapterselector_file.write('</td>')
    chapterselector_file.write('<td class="chapter_cell">\n')
    chapterselector_file.write('<div id=' + chapter_id + '.students style="overflow:auto;height:100%;white-space:nowrap;"></div>')
    chapterselector_file.write('</td>\n')
    chapterselector_file.write('</tr>\n')

def chapter_array_html(chapter_activities):
    return json.dumps([chapter['chapter_id'] for chapter in chapter_activities])

def write_chapter_activity_characteristics(chapter_activities, output_dir):
    chapter_activity_file = open(os.path.join(output_dir, 'chapter_activities.json'), 'w')
    chapter_activity_file.write(json.dumps(chapter_activities, indent=2))
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
