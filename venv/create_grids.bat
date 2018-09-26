pushd "C:\WorkArea\contentgen"
python "%~dp0\GridCreator.py" "1_french.xlsx" C:\WorkArea\contentgen\activitygen-rawmaterial C:\WorkArea\contentgen\French-Grade1-activities C:\WorkArea\contentgen\IC-grid
python "%~dp0\GridCreator.py" "2_french.xlsx" C:\WorkArea\contentgen\activitygen-rawmaterial C:\WorkArea\contentgen\French-Grade2-activities C:\WorkArea\contentgen\IC-grid
python "%~dp0\GridCreator.py" "1_math.xlsx" C:\WorkArea\contentgen\activitygen-rawmaterial C:\WorkArea\contentgen\Math-Grade1-activities C:\WorkArea\contentgen\IC-grid
python "%~dp0\GridCreator.py" "2_math.xlsx" C:\WorkArea\contentgen\activitygen-rawmaterial C:\WorkArea\contentgen\Math-Grade2-activities C:\WorkArea\contentgen\IC-grid
popd
pause
