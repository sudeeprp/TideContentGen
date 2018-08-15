from openpyxl import load_workbook
import re


class Sheet:
    def __init__(self, wsheet):
        self.wsheet = wsheet
    def __getitem__(self, item):
        return self.wsheet[item].value


def map_headings(ws, heading_row=1, start_col = 'A'):
    excel_col_map = {}
    cur_column = start_col
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


def collect_screen(ws, excel_col_map, screen_rows):
    screen = []
    for row_number in range(screen_rows['start'], screen_rows['end']+1):
        row_layout = []
        for column in ['images col1', 'images col2', 'images col3']:
            cell_value = ws[excel_col_map[column] + str(row_number)]
            if cell_value is None:
                row_layout.append(None)
            else:
                cell_value = cell_value.strip()
                if cell_value.lower().endswith('.png') or cell_value.lower().endswith('.jpg') or \
                                           cell_value.lower().endswith('.jpeg'):
                    row_layout.append({'image': cell_value})
                elif cell_value.startswith('|'):
                    row_layout.append({'merge_above': 1})
                else:
                    row_layout.append({'text': cell_value})
            #if you want to specify style: add more columns and use re.findall(r'(\w+=".+?")
        screen.append(row_layout)
    return screen


def collect_activity(ws, excel_col_map, activity_rows):
    activity = \
        {'Activity Identifier': ws[excel_col_map['Activity Identifier'] + str(activity_rows['start'])],
         'instruction.sound': ws[excel_col_map['instruction.sound'] + str(activity_rows['start'])].strip(),
         'images.layout': []}
    current_row = activity_rows['start']
    while current_row <= activity_rows['end']:
        screen_number, screen_rows = scan_row_range(ws, 'Screen', excel_col_map, current_row, activity_rows['end'])
        if screen_number is None:
            screen_number = '1'
        screen = collect_screen(ws, excel_col_map, screen_rows)
        activity['images.layout'].append(screen)
        current_row = screen_rows['end'] + 1
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

def dot_separate(sequence):
    seq_str = ''
    for i in sequence:
        seq_str += str(i) + '.'
    return seq_str[:-1]

#Excel columns - these need to be the same in every milestone sheet!
activity_sequence_col_head = '#'
activity_logo_col_head = 'Logo'
activity_numid_col_head = 'numid'
head_row = 3
start_col = 'B'

def forge_grid(excel_file, milestone):
    print("Opening " + excel_file)
    w = load_workbook(excel_file)
    ws = Sheet(w[milestone])
    print("Mapping columns")
    curriculum_col_map = map_headings(ws, heading_row=head_row, start_col=start_col)
    current_row = head_row + 1
    grid = []
    blank_rows = 0
    while current_row <= ws.wsheet.max_row:
        activity = ws[curriculum_col_map[activity_sequence_col_head] + str(current_row)]
        if activity is not None:
            sequence = re.findall(r'\d+', activity)
            if len(sequence) < 1:
                sequence = [activity]
            logo = ws[curriculum_col_map[activity_logo_col_head] + str(current_row)]
            numid = ws[curriculum_col_map[activity_numid_col_head] + str(current_row)]
            activity_id = logo + '_' + str(numid)
            activity_attributes = \
                {'sequence': sequence,
                 'Activity logo': logo,
                 'Activity Identifier': activity_id,
                 'Display name': dot_separate(sequence)
                }
            grid.append(activity_attributes)
            print(activity_id)
            if not all_attributes_ok(activity_attributes):
                print('Missing cells at ' + activity_id + ' (near row ' + str(current_row) + ')')
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

def pics_sounds_map(excel_file):
    w = load_workbook(excel_file, read_only=True, data_only=True)
    ws = Sheet(w[w.sheetnames[0]])
    heading_row = 1
    excel_col_map = map_headings(ws, heading_row)
    pics_to_sounds = {}

    for current_row in range(heading_row + 1, ws.wsheet.max_row + 1):
        pics_to_sounds[ws[excel_col_map['Picture'] + str(current_row)]] = ws[excel_col_map['Sound'] + str(current_row)]
    return pics_to_sounds