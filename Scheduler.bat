@echo off
chdir /d <your_folder_path>
python RandomScriptRunner.py Amazon
taskkill /F /IM chrome.exe /T

#.... and more for other scripts and websites
