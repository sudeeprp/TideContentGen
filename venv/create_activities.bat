pushd "G:\My Drive\activitygen-rawmaterial"
python "%~dp0\ActivityCreator.py" "_1_french-do-not-edit.xlsx" "_do-not-edit pics to sounds.xlsx" C:\WorkArea\contentgen\French-Grade1-activities
python "%~dp0\ActivityCreator.py" "_2_french-do-not-edit.xlsx" "_do-not-edit pics to sounds.xlsx" C:\WorkArea\contentgen\French-Grade2-activities
rem python "%~dp0\ActivityCreator.py" "_1_math-do-not-edit.xlsx" "_do-not-edit pics to sounds.xlsx" C:\WorkArea\contentgen\Math-Grade1-activities
popd
pause
