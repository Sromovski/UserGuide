@echo off
REM Finish loading the Gumroad catalogue: create the products that hit yesterday's
REM 10-per-day creation cap, verify every one, then publish those that pass.
REM
REM Safe to run more than once. Creation is resumable (anything with a recorded
REM product id is skipped) and publishing an already-published product is a no-op.
REM Nothing is published without a file attached.
REM
REM Scheduled as Windows Task "Gumroad Finish Load" — see CLAUDE.md.

cd /d C:\Projects\UserGuide
if not exist logs mkdir logs

echo ============================================ >> logs\gumroad.log
echo RUN %DATE% %TIME% >> logs\gumroad.log

python -m gumroadpub.publish --finish >> logs\gumroad.log 2>&1
set RC=%ERRORLEVEL%

echo EXIT %RC% >> logs\gumroad.log
exit /b %RC%
