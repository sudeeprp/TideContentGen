import GridHTMLPieces
import shutil
import os
from urllib.parse import quote

grid_images_to_copy = ['pencil.png']

def form_activity_layout(html_file, activities):
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

def get_grid_column(grid, start_activity_index):
    current_activity_index = start_activity_index
    next_activity_index = current_activity_index + 1
    grid_column = [grid[current_activity_index]]
    while next_activity_index < len(grid):
        next_activity_is_in_this_col = False
        if (len(grid[current_activity_index]['sequence']) > 2) and \
                (len(grid[next_activity_index]['sequence']) > 2):
            next_activity_is_in_this_col = True
        elif (grid[current_activity_index]['sequence'][0].lower().startswith('enrichment')) and \
                (grid[next_activity_index]['sequence'][0].lower().startswith('remedials')):
            next_activity_is_in_this_col = True
        if next_activity_is_in_this_col:
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


def write_grid_html_columns(html_file, grid_columns, raw_material_dir):
    max_rows = 4
    lcm_of_max_rows = 12
    filled_rows_in_lcm = []
    for column in grid_columns:
        for i in range(0, lcm_of_max_rows, lcm_of_max_rows//len(column)):
            filled_rows_in_lcm.append(i)
    row = 0
    for table_row in range(lcm_of_max_rows):
        html_file.write('<tr>\n')
        if table_row in filled_rows_in_lcm:
            for activities in grid_columns:
                row_span = lcm_of_max_rows//len(activities)
                if table_row % row_span == 0 and row < len(activities):
                    html_file.write('<td rowspan="' + str(row_span) + '">\n')
                    html_file.write('<a href="' +
                                    quote(activities[row]['Activity Identifier'] + '/' + 'index.html') + '">\n')
                    write_image_html(html_file, activities[row]['Activity logo'],
                                     activities[row]['Display name'], raw_material_dir)
                    html_file.write('</a></td>\n')
            if row == 0:
                html_file.write('<td rowspan="12" style="width:60px; border-left: none;"></td>')
            row += 1
        html_file.write('</tr>\n')
    if max([len(activities) for activities in grid_columns]) > max_rows:
        print('WARNING: number of parallel activities exceeds ' + str(max_rows))


def forge_milestone_grid(grid, milestone_name, raw_material_dir, output_dir):
    print('Making grid in ' + output_dir)
    html_file = open(os.path.join(output_dir, 'index.html'), 'w')
    html_file.write(GridHTMLPieces.begin_head)
    html_file.write(GridHTMLPieces.body_start)
    html_file.write('<table class="grid_table">\n')
    current_activity_index = 0
    grid_columns = []
    while current_activity_index < len(grid):
        column, next_activity_index = get_grid_column(grid, current_activity_index)
        grid_columns.append(column)
        current_activity_index = next_activity_index
    write_grid_html_columns(html_file, grid_columns, raw_material_dir)
    html_file.write('</table>\n')
    html_file.write(GridHTMLPieces.body_end)
    html_file.write(GridHTMLPieces.tail)
    html_file.close()
    for image_filename in grid_images_to_copy:
        shutil.copyfile(os.path.join(raw_material_dir, image_filename), os.path.join(output_dir, image_filename))
