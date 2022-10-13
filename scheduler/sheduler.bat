@echo off
rem delay 5 minutes
timeout /t 300
rem run app.py locate in previous folder use relative path
cd ..
python app.py
@pause