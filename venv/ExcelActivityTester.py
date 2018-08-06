import ExcelParser

activities = ExcelParser.forge_activities('C:/WorkArea/contentgen/play.area/multiscreen/French-Grade1-activitygen.xlsx')
print('activities:\n' + str(activities))
