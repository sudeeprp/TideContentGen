import GridHTMLPieces
import shutil


def form_activity_layout(html_file, activities):
    html_file.write('<tr class="activity_list">\n')
    for activity in activities:
        html_file.write('<td>\n')
        html_file.write('<a href="' + activity['activity id'] + '/' + 'index.html">')
        html_file.write('<figure>\n')
        html_file.write('<img src=' + activity['activity id'] + '/' + activity['logo'] + ' alt="Tab activity">\n')
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
