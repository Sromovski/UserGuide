@echo off
REM Drive both sales channels to a complete, published catalogue.
REM
REM Runs unattended every few hours. Safe to run any number of times: anything
REM already live is skipped, nothing is duplicated, and nothing is published
REM without its file attached.
REM
REM It exists because Gumroad caps product creation at 10 per rolling 24 hours,
REM so the catalogue cannot be loaded in one sitting — this converges instead.
REM
REM Scheduled as Windows Task "Publish All Products". Log: logs\publish_all.log

cd /d C:\Projects\UserGuide
if not exist logs mkdir logs

echo. >> logs\publish_all.log
python publish_all.py >> logs\publish_all.log 2>&1
set RC=%ERRORLEVEL%

echo EXIT %RC% >> logs\publish_all.log
exit /b %RC%
