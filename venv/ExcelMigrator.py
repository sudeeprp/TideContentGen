import sys
import os
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill, Color
from ExcelParser import map_headings, Sheet, cell_color

NEWSHEET_NUMID = 'num id'
NEWSHEET_TYPE = 'type'
NEWSHEET_PHASE = 'phase'
OUTPUT_START_COL = 2

def emptyOnNoCell(cell):
    if cell is not None and cell.value is not None:
        return cell.value
    else:
        return ""

def fill_row(sheet, row, values):
    if values[0] is not None and values[0] != "":
        for index, v in enumerate(values):
            sheet.cell(row, column=index+OUTPUT_START_COL).value = v
        return True
    else:
        return False

def removeLeadingUnderscore(numid):
    if isinstance(numid, str) and len(numid) > 0 and numid[0] == '_':
        numid = numid[1:]
    return numid

def makeLogo(chosenPhase, chosenType):
    logo = chosenType.lower()
    phase = chosenPhase.lower()
    if phase == 'enrichment' or phase == 'reinforcement':
        logo = logo + '-' + phase
    return logo

def migrate_row(sheet, row, col_map):
    logo = makeLogo(emptyOnNoCell(sheet.wsheet[col_map[NEWSHEET_PHASE] + str(row)]),
                    emptyOnNoCell(sheet.wsheet[col_map[NEWSHEET_TYPE] + str(row)]))
    numid = removeLeadingUnderscore(emptyOnNoCell(sheet.wsheet[col_map[NEWSHEET_NUMID] + str(row)]))
    return [logo, numid]

def row_color(source_sheet, col_map, row):
    rgb = None
    tint = None
    type_rgb, type_tint = cell_color(source_sheet.wsheet, col_map, NEWSHEET_TYPE, row)
    phase_rgb, phase_tint = cell_color(source_sheet.wsheet, col_map, NEWSHEET_PHASE, row)
    if type_rgb is not None:
        rgb = type_rgb
        tint = type_tint
    elif phase_rgb is not None:
        rgb = phase_rgb
        tint = phase_tint
    return rgb, tint

def migrate_sheet(newsheet, outputwb, migratedsheet_name):
    col_map = map_headings(newsheet, heading_row=3)
    if NEWSHEET_NUMID in col_map:
        output_sheet = outputwb.create_sheet(migratedsheet_name)
        fill_row(output_sheet, 3, ['logo', 'numid'])
        row = 4
        while fill_row(output_sheet, row, migrate_row(newsheet, row, col_map)):
            rgb, tint = row_color(newsheet, col_map, row)
            if rgb is not None:
                fill_color = Color(rgb=rgb, tint=tint)
                output_sheet.cell(row, OUTPUT_START_COL).fill = \
                    PatternFill(start_color=fill_color, end_color=fill_color, fill_type='solid')
            row+=1

def collate_sheets(oldformat_excel, newformat_excel, output_excel):
    if os.path.isfile(oldformat_excel):
        outputwb = load_workbook(oldformat_excel, data_only=True)
    else:
        outputwb = Workbook()
    neww = load_workbook(newformat_excel, data_only=True)
    for sheetname in neww.sheetnames:
        migrate_sheet(Sheet(neww[sheetname]), outputwb, sheetname)
    outputwb.save(output_excel)

if len(sys.argv) == 4:
    collate_sheets(oldformat_excel=sys.argv[1],
                   newformat_excel=sys.argv[2], output_excel=sys.argv[3])
else:
    print('Excel migrator\nUsage: ' + sys.argv[0] + ' <old format excel> <new format excel> <output excel>')
