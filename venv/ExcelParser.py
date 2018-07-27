from openpyxl import load_workbook
import re


class Sheet:
    def __init__(self, wsheet):
        self.wsheet = wsheet
    def __getitem__(self, item):
        return self.wsheet[item].value


def map_headings(ws, heading_row=1):
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
        {'Activity Identifier': ws[excel_col_map['Activity Identifier'] + str(activity_rows['start'])],
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


def collect_activities(ws, excel_col_map, row_range):
    activities = []
    current_row = row_range['start']
    while current_row <= row_range['end']:
        activity_ident, activity_rows = \
            scan_row_range(ws, 'Activity Identifier', excel_col_map, current_row, row_range['end'])
        if activity_ident is not None:
            activities.append(collect_activity(ws, excel_col_map, activity_rows))
        current_row = activity_rows['end'] + 1
    return activities


def forge_activities(excel_file):
    w = load_workbook(excel_file)
    ws = Sheet(w[w.sheetnames[0]])
    heading_row = 1
    activity_col_map = map_headings(ws, heading_row)
    return collect_activities(ws, activity_col_map, {'start': heading_row + 1, 'end': ws.wsheet.max_row})


def all_attributes_ok(activity_attributes):
    for activity_key in activity_attributes:
        if activity_attributes[activity_key] is None:
            return False
    return True


def row_is_blank(ws, row_number):
    row_with_values = sum(ws.wsheet.cell(row=row_number,column=i).value is not None for i in range(1,26))
    if row_with_values == 0:
        return True
    else:
        return False

def forge_grid(excel_file, milestone):
    print("Opening " + excel_file)
    w = load_workbook(excel_file)
    ws = Sheet(w[milestone])
    heading_row = 2
    print("Mapping columns")
    curriculum_col_map = map_headings(ws, heading_row=heading_row)
    current_row = heading_row + 1
    grid = []
    blank_rows = 0
    while current_row <= ws.wsheet.max_row:
        activity = ws[curriculum_col_map['Activity sequence'] + str(current_row)]
        if activity is not None:
            sequence = re.findall(r'\d+', activity)
            if len(sequence) < 1:
                sequence = [activity]
            activity_attributes = \
                {'sequence': sequence,
                 'Activity logo': ws[curriculum_col_map['Activity logo'] + str(current_row)],
                 'Activity Identifier': ws[curriculum_col_map['Activity Identifier'] + str(current_row)],
                 'Display name': ws[curriculum_col_map['Display name'] + str(current_row)],
                 'Activity details': ws[curriculum_col_map['Activity details'] + str(current_row)]}
            grid.append(activity_attributes)
            print(ws[curriculum_col_map['Activity Identifier'] + str(current_row)])
            if not all_attributes_ok(activity_attributes):
                print('Missing cells! Check merged-cells at ' + activity + ' (near row ' + str(current_row) + ')')
                break
        else:
            if row_is_blank(ws, current_row):
                blank_rows += 1
            else:
                blank_rows = 0
            if blank_rows > 20:
                break
        current_row += 1
    return grid
