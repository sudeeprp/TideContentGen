import sys
from openpyxl import load_workbook
from ExcelParser import map_headings, Sheet

NEWSHEET_NUMID = 'num id'
NEWSHEET_TYPE = 'type'

def emptyOnNoCell(cell):
    if cell is not None:
        return cell.value
    else:
        return ""

def fill_row(sheet, row, values):
    if values[0] is not None and values[0] != "":
        for index, v in enumerate(values):
            sheet.cell(row, column=index+1).value = v
        return True
    else:
        return False

def migrate_row(sheet, row, col_map):
    logo = emptyOnNoCell(sheet.wsheet[col_map[NEWSHEET_TYPE] + str(row)])
    numid = emptyOnNoCell(sheet.wsheet[col_map[NEWSHEET_NUMID] + str(row)])
    return [logo, numid]

def migrate_sheet(newsheet, outputwb, migratedsheet_name):
    col_map = map_headings(newsheet, heading_row=3)
    if NEWSHEET_NUMID in col_map:
        migrated_sheet = outputwb.create_sheet(migratedsheet_name)
        fill_row(migrated_sheet, 3, ['logo', 'numid'])
        row = 4
        while fill_row(migrated_sheet, row, migrate_row(newsheet, row, col_map)):
            row+=1

def collate_sheets(oldformat_excel, newformat_excel, output_excel):
    outputwb = load_workbook(oldformat_excel, data_only=True)
    neww = load_workbook(newformat_excel, data_only=True)
    for sheetname in neww.sheetnames:
        migrate_sheet(Sheet(neww[sheetname]), outputwb, sheetname)
    outputwb.save(output_excel)

if len(sys.argv) == 4:
    collate_sheets(oldformat_excel=sys.argv[1],
                   newformat_excel=sys.argv[2], output_excel=sys.argv[3])
else:
    print('Excel migrator\nUsage: ' + sys.argv[0] + ' <old format excel> <new format excel> <output excel>')
