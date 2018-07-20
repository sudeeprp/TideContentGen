from openpyxl import load_workbook
import re

heading_row = 1


class Sheet:
    def __init__(self, wsheet):
        self.wsheet = wsheet
    def __getitem__(self, item):
        return self.wsheet[item].value


def map_headings(ws):
    excel_col_map = {}
    cur_column = 'A'
    head_row = str(heading_row)
    col_ord = ord(cur_column)
    while ws[cur_column+head_row] is not None and ws[cur_column+head_row] != "" and cur_column != 'Z':
        excel_col_map[ws[cur_column+head_row]] = chr(col_ord)
        col_ord += 1
        cur_column = chr(col_ord)
    if cur_column == 'Z':
        print('ERROR: more columns than expected!\n')
        return None
    return excel_col_map


def scan_row_range(ws, col_name, excel_col_map, start_row, limit_row):
    row_range = {'start': start_row, 'end': start_row}
    name = ws[excel_col_map[col_name] + str(start_row)]
    current_row = start_row + 1
    while current_row <= limit_row and (ws[excel_col_map[col_name] + str(current_row)] is None or
                                        ws[excel_col_map[col_name] + str(current_row)] == ""):
        current_row += 1
    row_range['end'] = current_row - 1
    return name, row_range


def collect_activity(ws, excel_col_map, activity_rows):
    activity = \
        {'activity id': ws[excel_col_map['activity id'] + str(activity_rows['start'])],
         'activity name': ws[excel_col_map['activity name'] + str(activity_rows['start'])],
         'logo': ws[excel_col_map['logo'] + str(activity_rows['start'])],
         'type': ws[excel_col_map['type'] + str(activity_rows['start'])],
         'instruction.sound': ws[excel_col_map['instruction.sound'] + str(activity_rows['start'])],
         'images.layout': []}
    image_range = ws.wsheet[excel_col_map['images col1'] + str(activity_rows['start']) +
                     ':' + excel_col_map['images col3'] + str(activity_rows['end'])]
    for image_row_cells in image_range:
        image_row_layout = []
        for image_cell in image_row_cells:
            image_layout = {'image': image_cell.value}
            if image_cell.comment is not None:
                image_layout['attrs'] = re.findall(r'(\w+=".+?")', str(image_cell.comment))
            image_row_layout.append(image_layout)
        activity['images.layout'].append(image_row_layout)
    return activity


def collect_milestone(ws, excel_col_map, milestone_rows):
    milestone = \
        {'milestone name': ws[excel_col_map['milestone name'] + str(milestone_rows['start'])],
         'cmd': ws[excel_col_map['cmd'] + str(milestone_rows['start'])],
         'activities': []}
    current_row = milestone_rows['start']
    while current_row <= milestone_rows['end']:
        activity_name, activity_rows = \
            scan_row_range(ws, 'activity name', excel_col_map, current_row, milestone_rows['end'])
        if activity_name is not None:
            milestone['activities'].append(collect_activity(ws, excel_col_map, activity_rows))
        current_row = activity_rows['end'] + 1
    return milestone


def forge_milestones(excel_file):
    milestones = []
    w = load_workbook(excel_file)
    ws = Sheet(w[w.sheetnames[0]])
    excel_col_map = map_headings(ws)
    current_row = heading_row + 1
    while current_row <= ws.wsheet.max_row:
        ms_name, milestone_rows = scan_row_range(ws, 'milestone name', excel_col_map, current_row, ws.wsheet.max_row)
        if ms_name is not None:
            milestones.append(collect_milestone(ws, excel_col_map, milestone_rows))
        current_row = milestone_rows['end'] + 1
    return milestones