
rem КМД запустит от имени админа

rem @echo off
cd /d "%~dp0"
powershell -Command "Start-Process cmd -Verb RunAs"

rem https://grok.com/share/bGVnYWN5_78382a0c-a3b2-4df3-b67a-95da42f0331b