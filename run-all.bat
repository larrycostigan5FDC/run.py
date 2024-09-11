@echo off

if [%1] NEQ [] GOTO lst

for /r %%i in (cfg\*) do start /D "%~dp0" python run.py %%~ni

GOTO end

:lst
for /F "tokens=*" %%A in (%1.lst) do (
    if /i "%%A:~0,1%"=="#" (
        echo "skip %%A"
    ) else (
        start /D "%~dp0" python run.py %%A
    )
)

:end
exit
