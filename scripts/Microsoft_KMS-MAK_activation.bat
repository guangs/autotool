@echo off & setLocal enabledelayedexpansion
mode con: cols=110 lines=40
cls
REM Created: 2014-11-12
REM Created by: James Holmes x56161
REM Updated by: Brooks Peppin 13-Oct-2015
net session >nul 2>&1 & IF ERRORLEVEL 1 (ECHO You must right-click and select & ECHO. & ECHO "RUN AS ADMINISTRATOR"  to run this batch file. & ECHO. & ECHO Exiting... & ECHO. & PAUSE & EXIT /D)
REM Echo Note! Make sure you have run this batch file "as administrator" before continuing.



:MENU
echo.
echo  ############################################################
echo  #   Make sure you're on the VPN or on the VMware Network   #
echo  #                                                          #
echo  #   CHECK SYSTEM TIME: Fix it if it is not correct         #
echo  #                                                          #
echo  #   Also make sure to run this "as administrator"          #
echo  #                                                          #
echo  #   Note: This is both 32bit and 64bit compatible          #
echo  ############################################################
echo.
echo  Reference KB's: 
echo    Windows: https://kb.eng.vmware.com/node/1361
echo    Office: https://kb.eng.vmware.com/node/1438
echo.
echo  Activate via KMS
echo  1 - MS Office Professional 2013
echo  2 - MS Windows 7, Server 2008, Server 2008 R2
echo  3 - MS Windows 8.x
echo  4 - MS Office 2010
echo  5 - MS Windows 10
Echo.
Echo Activate via MAK
echo  6 - MS Office Professional 2013
echo  7 - MS Office Professional 2016
echo  8 - Windows 7 Enterprise
echo  9 - Windows 8.1 Enterprise
echo.
echo Check Status of Activation
echo  10 - Check on Office key
echo  11 - Check on Windows key
echo.
echo  12 - Exit
echo.
set /p activateOption=Choose an option 1-10:
echo.
IF %activateOption%==1 GOTO activate2013
IF %activateOption%==2 GOTO activateWin7
IF %activateOption%==3 GOTO activateWin8
IF %activateOption%==4 GOTO activate2010
IF %activateOption%==5 GOTO Windows10
IF %activateOption%==6 GOTO MAK2013
IF %activateOption%==7 GOTO MAK2016
IF %activateOption%==8 GOTO MAKWin7
IF %activateOption%==9 GOTO MAKWin8.1
IF %activateOption%==10 GOTO OfficeCheck
IF %activateOption%==11 GOTO WindowsCheck
IF %activateOption%==12 GOTO END

echo.

:activate2013
cls 
echo.
echo Activating MS Office 2013 via KMS
echo =========================
echo.
if exist "C:\Program Files\Microsoft Office\Office15\OSPP.VBS" (
 set PPATH="C:\Program Files\Microsoft Office\Office15"
) else (
 set PPATH="C:\Program Files (x86)\Microsoft Office\Office15"
)
cscript.exe %PPATH%\OSPP.VBS /sethst:kms-win8.eng.vmware.com
cscript.exe %PPATH%\OSPP.VBS /act
echo.
pause
GOTO MENU

:activateWin7
cls 
echo.
echo Activating MS Windows 7, Server 2008, Server 2008 R2 via KMS
echo ====================================================
echo.
cscript C:\windows\system32\slmgr.vbs -skms kmsserver.eng.vmware.com
cscript C:\windows\system32\slmgr.vbs -ato
pause
GOTO MENU

:activateWin8
cls 
echo.
echo Activating Windows 8.x via KMS
echo ======================
echo.

cscript C:\windows\system32\slmgr.vbs -skms kms-win8.eng.vmware.com
cscript C:\windows\system32\slmgr.vbs -ato
pause
GOTO MENU

:activate2010
cls 
echo.
echo Activating Office 2010
echo ======================
echo.
echo Get user to update to Office 2013
echo.
pause
GOTO MENU

:Windows10
cls 
echo.
echo Activating Windows 10 via KMS
echo ======================
echo.
cscript C:\windows\system32\slmgr.vbs -skms kms-win10.eng.vmware.com
cscript C:\windows\system32\slmgr.vbs -ato
pause
GOTO MENU

:MAK2013
cls 
echo.
echo Activating MS Office 2013 via MAK
echo =========================
echo.
if exist "C:\Program Files\Microsoft Office\Office15\OSPP.VBS" (
 set PPATH="C:\Program Files\Microsoft Office\Office15"
) else (
 set PPATH="C:\Program Files (x86)\Microsoft Office\Office15"
)
cscript.exe %PPATH%\OSPP.VBS /inpkey:TG3VM-VDNKJ-26D7R-BFQ7H-XD43H
cscript.exe %PPATH%\OSPP.VBS /act
pause
GOTO MENU

:MAK2016
cls 
echo.
if exist "C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE" (
ECHO Office 365 version installed. User must activate using vmware email address
pause
cls
GOTO MENU
) else (if exist "C:\Program Files\Microsoft Office\Office16\OSPP.VBS" (
 set PPATH="C:\Program Files\Microsoft Office\Office16"
) else (
 set PPATH="C:\Program Files (x86)\Microsoft Office\Office16"
)
)
echo Activating MS Office 2016 via MAK
echo =========================
echo.
cscript.exe %PPATH%\OSPP.VBS /inpkey:T9XTQ-WN7GW-8CX9F-CW38F-3DBVM
cscript.exe %PPATH%\OSPP.VBS /act
pause
GOTO MENU

:MAKWin7
cls 
echo.
echo Activating MS Windows 7 via MAK
echo ====================================================
echo.
cscript C:\windows\system32\slmgr.vbs /ipk YVKKV-JHDX6-XKQ27-VPHVJ-8THGG
cscript c:\windows\system32\slmgr.vbs /ato
pause
GOTO MENU

:MAKWin8.1
cls 
echo.
echo Activating MS Windows 8.1 via MAK
echo ====================================================
echo.
cscript C:\windows\system32\slmgr.vbs /ipk J7NG6-CQHV6-XWM6Q-FXJMJ-WB33Q
cscript c:\windows\system32\slmgr.vbs /ato
pause
GOTO MENU

:OfficeCheck
cls
if exist "C:\Program Files\Microsoft Office\Office16\OSPP.VBS" (
 set PPATH="C:\Program Files\Microsoft Office\Office16"
) else (
 set PPATH="C:\Program Files (x86)\Microsoft Office\Office16"
)
cscript %PPATH%\OSPP.VBS /dstatus
pause
GOTO Menu

:WindowsCheck
cls
cscript c:\windows\system32\slmgr.vbs /dlv
pause
GOTO Menu

:END
exit

