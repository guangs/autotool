@echo off
if exist "%ProgramFiles(x86)%" (
set OSbit=64
set pythoninstaller=python-2.7.8.amd64.msi
) else (
set OSbit=32
set pythoninstaller=python-2.7.8.msi
)

if not exist "C:\Python27" (
echo "installing python27 ..., please wait"
msiexec /i \\sanya.eng.vmware.com\Exchange\gshi\automation\%pythoninstaller% /qn ADDLOCAL=ALL
)

sc query Autotool
if %errorlevel%==0 (
  c:\autotool\presoftware\nssm-2.24\win%OSbit%\nssm.exe stop Autotool
  ping 127.0.0.1 -n 3
  c:\autotool\presoftware\nssm-2.24\win%OSbit%\nssm.exe remove Autotool confirm
)
xcopy /s /e /i /y \\sanya.eng.vmware.com\Exchange\gshi\automation\autotool c:\autotool
c:\autotool\presoftware\nssm-2.24\win%OSbit%\nssm.exe install Autotool "c:\autotool\bin\startserver.bat"
c:\autotool\presoftware\nssm-2.24\win%OSbit%\nssm.exe set Autotool Type SERVICE_WIN32_OWN_PROCESS
::c:\autotool\presoftware\nssm-2.24\win%OSbit%\nssm.exe set Autotool ObjectName .\Administrator ca$hc0w
ping 127.0.0.1 -n 2
c:\autotool\presoftware\nssm-2.24\win%OSbit%\nssm.exe start Autotool