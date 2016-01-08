xcopy /s /e /i /y \\10.117.47.199\Exchange\gshi\automation\autotool c:\autotool
xcopy /y c:\autotool\bin\dispatch\autotool.lnk "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
start c:\autotool\bin\dispatch\autotool.bat