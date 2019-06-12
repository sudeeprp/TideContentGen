from sheet_reader import get_sheetreader, read_range

MAX_ACTIVITY_ROWS = 4096


def map_headings(reader, activity_sheetid):
    heading_map = {}
    heading_range = 'A1:Z1'
    heading_rows = read_range(reader, activity_sheetid, heading_range)
    if len(heading_rows) > 0:
        headings = heading_rows[0]
        for i, heading in enumerate(headings):
            heading_map[heading.lower()] = i
    return heading_map


def get_cell_range(start_row, number_of_rows, number_of_cols):
    return 'A' + str(start_row) + ':' + chr(ord('A')+number_of_cols-1) + str(start_row + number_of_rows - 1)


def row_is_empty(row_dict):
    is_empty = True
    for d in row_dict:
        if len(row_dict[d]) > 0:
            is_empty = False
            break
    return is_empty

class RowReader:
    def __init__(self, reader, activity_sheetid, heading_row):
        self.reader = reader
        self.activity_sheetid = activity_sheetid
        self.heading_map = map_headings(reader, activity_sheetid)
        if len(self.heading_map) > 0:
            cell_range = get_cell_range(heading_row+1, MAX_ACTIVITY_ROWS, len(self.heading_map))
            self.cells = read_range(reader, activity_sheetid, cell_range)
    def is_empty(self):
        return len(self.heading_map) == 0
    def read_row(self, i):
        row_values = {}
        if i < len(self.cells):
            this_row = self.cells[i]
            for heading in self.heading_map:
                cell_value = ''
                if self.heading_map[heading] < len(this_row):
                    cell_value = this_row[self.heading_map[heading]]
                row_values[heading] = cell_value
        return row_values


def row_is_in_range(row_reader, current_row, col_name):
    row_dict = row_reader.read_row(current_row)
    return not row_is_empty(row_dict) and \
            (row_dict[col_name] is None or row_dict[col_name] == "")


def scan_row_range(row_reader, col_name, start_row, limit_row):
    row_dict = row_reader.read_row(start_row)
    name = row_dict[col_name]

    current_row = start_row + 1
    while current_row <= limit_row and row_is_in_range(row_reader, current_row, col_name):
        current_row += 1
    return name, start_row, current_row - 1


def collect_screen(row_reader, screen_start_row, screen_end_row):
    screen = []
    for row_number in range(screen_start_row, screen_end_row + 1):
        row_layout = []
        row_dict = row_reader.read_row(row_number)
        for column_number in ['1', '2', '3']:
            picture_col = 'images col' + column_number
            cell_value = row_dict[picture_col]
            if cell_value is None or cell_value == '':
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
                prior = row_dict['col' + column_number + ' after']
                if prior == None: prior = ''
                picture_desc['after'] = prior.strip()
                row_layout.append(picture_desc)
        screen.append(row_layout)
    return screen


def collect_activity(row_reader, activity_start_row, activity_end_row):
    # While generating activities, the name in the excel will not have 'Tab 2' and so on.
    activity_row_dict = row_reader.read_row(activity_start_row)
    activity = \
        {'activity identifier': activity_row_dict['activity identifier'],
         'activity folder': activity_row_dict['activity identifier'],
         'instruction.sound': activity_row_dict['instruction.sound'].strip(),
         'title': activity_row_dict['title'],
         'images.layout': []}
    current_row = activity_start_row
    while current_row <= activity_end_row:
        screen_number, screen_start_row, screen_end_row = \
            scan_row_range(row_reader, 'screen', current_row, activity_end_row)
        screen = collect_screen(row_reader, screen_start_row, screen_end_row)
        activity['images.layout'].append(screen)
        current_row = screen_end_row + 1
    return activity


def collect_activities(row_reader):
    activities = []
    current_row = 0
    while not row_is_empty(row_reader.read_row(current_row)):
        activity_ident, activity_start_row, activity_end_row = \
            scan_row_range(row_reader, 'activity identifier', current_row, MAX_ACTIVITY_ROWS)
        if activity_ident is not None:
            print(activity_ident)
            activities.append(collect_activity(row_reader, activity_start_row, activity_end_row))
        current_row = activity_end_row + 1
    return activities


def forge_activities(row_reader):
    return collect_activities(row_reader)


def pics_sounds_map(row_reader):
    pics_to_sounds = {}
    current_row = 0
    while not row_is_empty(row_reader.read_row(current_row)):
        row_dict = row_reader.read_row(current_row)
        picture_name = row_dict['picture']
        pics_to_sounds[picture_name.strip()] = row_dict['sound'].strip()
    return pics_to_sounds
