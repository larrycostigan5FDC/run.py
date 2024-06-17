@echo off

if [%1] NEQ [] GOTO lst

for /r %%i in (cfg\*) do start /D "%~dp0" python run.py %%~ni

GOTO end

:lst
for /F "tokens=*" %%A in (%1.lst) do start /D "%~dp0" python run.py %%A

:end
exit
