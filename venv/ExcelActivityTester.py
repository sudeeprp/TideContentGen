import ExcelParser

activities = ExcelParser.forge_activities('c:/workarea/contentgen/French-Grade1-activitygen.xlsx')
print('activities:\n' + str(activities))
