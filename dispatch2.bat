sc query Autotool
if %errorlevel%==0 (
  c:\autotool\presoftware\nssm-2.24\win64\nssm.exe stop Autotool
  ping 127.0.0.1 -n 2
  c:\autotool\presoftware\nssm-2.24\win64\nssm.exe remove Autotool confirm
)
xcopy /s /e /i /y \\sanya.eng.vmware.com\Exchange\gshi\automation\autotool c:\autotool
if exist "%ProgramFiles(x86)%" (
c:\autotool\presoftware\nssm-2.24\win64\nssm.exe install Autotool "c:\autotool\bin\startserver.bat"
c:\autotool\presoftware\nssm-2.24\win64\nssm.exe set Autotool Type SERVICE_AUTO_START
ping 127.0.0.1 -n 2
c:\autotool\presoftware\nssm-2.24\win64\nssm.exe start Autotool
) else (
c:\autotool\presoftware\nssm-2.24\win32\nssm.exe install Autotool "c:\autotool\bin\startserver.bat"
c:\autotool\presoftware\nssm-2.24\win32\nssm.exe set Autotool Type SERVICE_AUTO_START
ping 127.0.0.1 -n 2
c:\autotool\presoftware\nssm-2.24\win32\nssm.exe start Autotool
)