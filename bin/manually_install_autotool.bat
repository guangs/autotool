@echo off
SET AUTOTOOL_HOME=%CD:\bin=%
SET PATH=%PATH%;%AUTOTOOL_HOME%
cd %AUTOTOOL_HOME%

if exist "%ProgramFiles(x86)%" (
set OSbit=64
) else (
set OSbit=32
)

sc query Autotool
if %errorlevel%==0 (
  %AUTOTOOL_HOME%\presoftware\nssm-2.24\win%OSbit%\nssm.exe stop Autotool
  ping 127.0.0.1 -n 3
  %AUTOTOOL_HOME%\presoftware\nssm-2.24\win%OSbit%\nssm.exe remove Autotool confirm
)
%AUTOTOOL_HOME%\presoftware\nssm-2.24\win%OSbit%\nssm.exe install Autotool "%AUTOTOOL_HOME%\bin\startserver.bat"
%AUTOTOOL_HOME%\presoftware\nssm-2.24\win%OSbit%\nssm.exe set Autotool Type SERVICE_WIN32_OWN_PROCESS
ping 127.0.0.1 -n 2
%AUTOTOOL_HOME%\presoftware\nssm-2.24\win%OSbit%\nssm.exe start Autotool