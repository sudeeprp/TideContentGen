import unittest
from sheet_reader import get_sheetreader, read_range
import ActivitySheetParser as asp

ACTIVITY_SHEET_ID = '1RA8A72tnBjfpLsBNkIkqPR3XtBh4948lbXL_-5R4m34'
PICSOUNDS_SHEET_ID = '1zMsRIfrTDEm2W-Pu_ZAMN14xyUkHA2Yh'

class TestActivitySheetParser(unittest.TestCase):
    def testHeadingMap(self):
        reader = get_sheetreader()
        heading_map = asp.map_headings(reader, ACTIVITY_SHEET_ID)
        self.assertEqual(len(heading_map), 11, 'heading map has ' + str(len(heading_map)) + ' elements')

    def testRowRange(self):
        A1range = asp.get_cell_range(4, 3, 13)
        self.assertEqual(A1range, 'A4:M6', 'range turned out to be ' + A1range)

    def testRowReader(self):
        reader = get_sheetreader()
        row_reader = asp.RowReader(reader, ACTIVITY_SHEET_ID, heading_row=1)
        test_rows = 5
        for i in range(test_rows):
            row_values = row_reader.read_row(i)
            self.assertGreater(len(row_values), 0, 'Empty row encountered in first ' + str(test_rows) + ' rows')

    def testForgeActivity(self):
        reader = get_sheetreader()
        row_reader = asp.RowReader(reader, ACTIVITY_SHEET_ID, heading_row=1)
        activity = asp.forge_activities(row_reader)
        self.assertGreater(len(activity), 0, 'Empty activity list encountered')

    def testPicsSoundsMap(self):
        reader = get_sheetreader()
        row_reader = asp.RowReader(reader, PICSOUNDS_SHEET_ID, heading_row=1)
        pics_sounds = asp.pics_sounds_map(row_reader)
        self.assertGreater(len(pics_sounds), 0, "Empty pics-to-sounds encountered")


if __name__ == '__main__':
    unittest.main()
