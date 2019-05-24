set migrate=python "%~dp0\ExcelMigrator.py"
set create=python "%~dp0\GridCreator.py"
set sourcedrive=G:\My Drive\IC_curriculum
set rawmaterial=G:\My Drive\activitygen-rawmaterial
set stage=C:\TideStage\IC
set activitysource=C:\TideStage\ActivityLab\empty

%migrate% "%sourcedrive%\1_french.xlsx" "%sourcedrive%\V6_F_CP1_New_T2.xlsx" "%stage%\1_french.xlsx"
%create% "%stage%\1_french.xlsx" "%rawmaterial%" "%activitysource%\1_french" "%stage%\LearningGrid"

%migrate% "%sourcedrive%\2_french.xlsx" "%sourcedrive%\F_CP2_New_T2.xlsx" "%stage%\2_french.xlsx"
%create% "%stage%\2_french.xlsx" "%rawmaterial%" "%activitysource%\2_french" "%stage%\LearningGrid"

%migrate% "%sourcedrive%\1_math.xlsx" "%sourcedrive%\V6_Math_CP1_new_template_MS8_onwards.xlsx" "%stage%\1_math.xlsx"
%create% "%stage%\1_math.xlsx" "%rawmaterial%" "%activitysource%\1_math" "%stage%\LearningGrid"

%migrate% "%sourcedrive%\2_math.xlsx" "%sourcedrive%\V6_Math_CP2_new_template_MS8_onwards.xlsx" "%stage%\2_math.xlsx"
%create% "%stage%\2_math.xlsx" "%rawmaterial%" "%activitysource%\2_math" "%stage%\LearningGrid"

python "%~dp0\GridPackager.py" "%rawmaterial%" "%sourcedrive%" "%stage%\LearningGrid"

