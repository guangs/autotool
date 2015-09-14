xcopy /s /e /i /y \\sanya.eng.vmware.com\Exchange\gshi\automation\autotool c:\autotool
xcopy c:\autotool\bin\autotool.lnk "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
start c:\autotool\bin\startserver.bat