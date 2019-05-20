from openpyxl import load_workbook
from openpyxl import styles
import re

# Excel columns - these need to be the same in every milestone sheet!
activity_sequence_col_head = '#'
activity_logo_col_head = 'logo'
activity_numid_col_head = 'numid'
head_row = 3
start_col = 'B'
running_numid = {}
numid_color_map = {}

class Sheet:
    def __init__(self, wsheet):
        self.wsheet = wsheet

    def __getitem__(self, item):
        cell_value = self.wsheet[item].value
        if cell_value is not None:
            try:
                cell_value = '{0:g}'.format(cell_value)
            except ValueError:
                cell_value = str(self.wsheet[item].value).strip()
        return cell_value


def map_headings(ws, heading_row=1, start_scan='A'):
    excel_col_map = {}
    cur_column = start_scan
    head_row = str(heading_row)
    col_ord = ord(cur_column)
    while ws[cur_column + head_row] is not None and ws[cur_column + head_row] != "" and cur_column != 'Z':
        excel_col_map[ws[cur_column + head_row].lower()] = chr(col_ord)
        col_ord += 1
        cur_column = chr(col_ord)
    if cur_column == 'Z':
        print('** Warning: more columns than expected!\n')
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
    for row_number in range(screen_rows['start'], screen_rows['end'] + 1):
        row_layout = []
        for column_number in ['1', '2', '3']:
            picture_col = 'images col' + column_number

            cell_value = ws[excel_col_map[picture_col] + str(row_number)]
            if cell_value is None:
                row_layout.append(None)
            else:
                cell_value = cell_value.strip()
                picture_desc = {}
                if cell_value.lower().endswith('.png') or cell_value.lower().endswith('.jpg') or \
                        cell_value.lower().endswith('.jpeg'):
                    picture_desc['image'] = cell_value
                elif cell_value.startswith('|'):
                    picture_desc['merge_above'] = 1
                else:
                    picture_desc['text'] = cell_value
                prior = ws[excel_col_map['col' + column_number + ' after'] + str(row_number)]
                if prior == None: prior = ''
                picture_desc['after'] = prior.strip()
                row_layout.append(picture_desc)
            # if you want to specify style: add more columns and use re.findall(r'(\w+=".+?")
        screen.append(row_layout)
    return screen


def collect_activity(ws, excel_col_map, activity_rows):
    # While generating activities, the name in the excel will not have 'Tab 2' and so on.
    activity = \
        {'activity identifier': ws[excel_col_map['activity identifier'] + str(activity_rows['start'])],
         'activity folder': ws[excel_col_map['activity identifier'] + str(activity_rows['start'])],
         'instruction.sound': ws[excel_col_map['instruction.sound'] + str(activity_rows['start'])].strip(),
         'title': ws[excel_col_map['title'] + str(activity_rows['start'])],
         'images.layout': []}
    current_row = activity_rows['start']
    while current_row <= activity_rows['end']:
        screen_number, screen_rows = scan_row_range(ws, 'screen', excel_col_map, current_row, activity_rows['end'])
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
            scan_row_range(ws, 'activity identifier', excel_col_map, current_row, row_range['end'])
        if activity_ident is not None:
            print(activity_ident)
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
    row_with_values = sum(ws.wsheet.cell(row=row_number, column=i).value is not None for i in range(1, 26))
    if row_with_values == 0:
        return True
    else:
        return False


def activity_to_folder(logo, numid):
    #if it's in the form of 'tab <digit>', then ignore the digit - that's the number of students
    if logo.lower().startswith('tab'):
        logo_words = logo.split()
        if len(logo_words) > 1 and logo_words[1].isdigit():
            logo = 'tab'
    activity_folder = logo + "_" + str(numid)
    return activity_folder

def repair_keywords(input):
    output = input.lower().replace('remedial', 'reinforcement')
    return output

def get_qualifier_and_logo(ws, curriculum_col_map, current_row):
    qualifiers = ['enrichment', 'reinforcement']
    sequence_str = ''
    if activity_sequence_col_head in curriculum_col_map:
        try:
            sequence_str = ws[curriculum_col_map[activity_sequence_col_head] + str(current_row)].lower()
            sequence_str = repair_keywords(sequence_str)
        except(AttributeError):
            print("No # value found at row " + str(current_row))
    logo_str = (ws[curriculum_col_map[activity_logo_col_head] + str(current_row)]).lower()

    found_qualifier = ''
    extracted_logo = activity_type = repair_keywords(logo_str)
    for qualifier in qualifiers:
        if sequence_str.find(qualifier) != -1 or logo_str.find(qualifier) != -1:
            found_qualifier = qualifier
            activity_type = extracted_logo.split('-')[0]
            break
    extracted_logo = extracted_logo.strip()
    return found_qualifier, extracted_logo, activity_type

def run_numid(activity_type):
    if activity_type in running_numid:
        running_numid[activity_type] += 1
    else:
        running_numid[activity_type] = 1
    return running_numid[activity_type]

def compute_numid(chapterID, activity_type, numid, numid_color):
    activity_ref = ""
    if numid_color is not None:
        activity_ref = chapterID + activity_type + numid_color

    if numid is None:
        if activity_ref in numid_color_map:
            numid = numid_color_map[activity_ref]
        else:
            numid = run_numid(activity_type)
    elif numid.isnumeric():
        running_numid[activity_type] = int(numid)

    if activity_ref != "":
        numid_color_map[activity_ref] = numid
    return numid

def get_numid(ws, curriculum_col_map, current_row, logo):
    numid = None
    predefined = False
    numid_color = None
    if activity_numid_col_head in curriculum_col_map:
        numid = ws[curriculum_col_map[activity_numid_col_head] + str(current_row)]
        numid_color = cell_color_strID(ws.wsheet, curriculum_col_map, activity_numid_col_head, current_row)
        if numid is not None: predefined = True
    numid = compute_numid(str(ws.wsheet), logo, numid, numid_color)
    return numid, predefined

def write_numid(display_numid, numid_is_predef, ws, curriculum_col_map, current_row):
    prefix = ""
    if not numid_is_predef:
        prefix = "'"
    if activity_numid_col_head in curriculum_col_map:
        ws.wsheet[curriculum_col_map[activity_numid_col_head] + str(current_row)].value = prefix + display_numid

def cell_color(worksheet, curriculum_col_map, col_name, activity_row):
    rgb = None
    tint = None
    colors = styles.colors.COLOR_INDEX
    color = worksheet[curriculum_col_map[col_name] +
                                           str(activity_row)].fill.start_color
    if isinstance(color.index, str) and color.index != '00000000' and color.index != 'FFFFFFFF':
        rgb = color.index
        tint = color.tint
    elif isinstance(color.index, int) and colors[color.index] != '00FFFFFF':
        rgb = colors[color.index]
        tint = color.tint
    return rgb, tint

def cell_color_strID(worksheet, curriculum_col_map, col_name, activity_row):
    color_strID = None
    rgb, tint = cell_color(worksheet, curriculum_col_map, col_name, activity_row)
    if rgb is not None:
        color_strID = str(rgb) + " " + str(tint)
    return color_strID

def activity_is_parallel_with_next(worksheet, curriculum_col_map, activity_row):
    is_parallel_with_next = False
    activity_bk_color = cell_color_strID(worksheet, curriculum_col_map, activity_logo_col_head, activity_row)
    if(activity_bk_color is not None):
        next_activity_bk_color = cell_color_strID(worksheet, curriculum_col_map, activity_logo_col_head, activity_row + 1)
        if activity_bk_color == next_activity_bk_color:
            is_parallel_with_next = True
    return is_parallel_with_next

def activity_type_is_mandatory(activity_type):
    is_mandatory = False
    try:
        if 'tab assessment' in activity_type.lower():
            is_mandatory = True
    except TypeError:
        print('logo parsing error: ' + str(activity_type))
    return is_mandatory

def ascii_number_to_local(ascii_numstr, zero_symbol_offset):
    local_numstr = ''
    for c in ascii_numstr:
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            local_numstr += chr(ord(c) + zero_symbol_offset)
        else:
            local_numstr += c
    return local_numstr


def forge_grid(worksheet, zero_symbol_offset):
    ws = Sheet(worksheet)
    curriculum_col_map = map_headings(ws, heading_row=head_row, start_scan=start_col)
    if activity_logo_col_head not in curriculum_col_map:
        print('Ignoring ' + str(worksheet) + ': no logo-column found.')
        return None
    current_row = head_row + 1
    grid = []
    blank_rows = 0
    prev_activity = ''
    while current_row <= ws.wsheet.max_row:
        activity = ws[curriculum_col_map[activity_logo_col_head] + str(current_row)]
        if activity is None or activity == "":
            break
        activity = str(activity).lower()
        is_with_next = activity_is_parallel_with_next(worksheet, curriculum_col_map, current_row)
        if activity is not None:
            qualifier, logo, activity_type = get_qualifier_and_logo(ws, curriculum_col_map, current_row)
            numid, numid_is_predef = get_numid(ws, curriculum_col_map, current_row, activity_type)
            display_numid = ascii_number_to_local(str(numid), zero_symbol_offset)
            write_numid(display_numid, numid_is_predef, ws, curriculum_col_map, current_row)
            is_mandatory = activity_type_is_mandatory(activity_type)
            #data-collection is done based on activity_id. so keep the displayed logo and the ascii numid
            activity_id = logo + '_' + str(numid)
            activity_attributes = \
                {'qualifier': qualifier,
                 'activity logo': logo,
                 'activity identifier': activity_id,
                 'activity folder': activity_to_folder(activity_type, display_numid),
                 'display name': display_numid,
                 'mandatory': is_mandatory,
                 'withnext': is_with_next
                 }
            grid.append(activity_attributes)
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
        prev_activity = activity
    return grid


def pics_sounds_map(excel_file):
    w = load_workbook(excel_file, data_only=True)
    ws = Sheet(w[w.sheetnames[0]])
    heading_row = 1
    excel_col_map = map_headings(ws, heading_row)
    pics_to_sounds = {}

    try:
        for current_row in range(heading_row + 1, ws.wsheet.max_row + 1):
            pics_to_sounds[ws[excel_col_map['picture'] + str(current_row)].strip()] = \
                ws[excel_col_map['sound'] + str(current_row)].strip()
    except AttributeError:
        print("Error at row " + str(current_row))
        raise
    return pics_to_sounds

def grab_config(workbook):
    config_dict = {}
    if 'config' in workbook:
        worksheet = workbook['config']
        current_row = 1
        while worksheet['A' + str(current_row)].value is not None:
            key = worksheet['A' + str(current_row)].value
            value = worksheet['B' + str(current_row)].value
            if value[0] == "'":
                value = value[1:]
            config_dict[key] = value
            current_row += 1
    return config_dict
