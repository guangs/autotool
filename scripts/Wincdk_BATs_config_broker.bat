rem Launch 64bit cmd to run the ps command if on a 64bit system
if "%PROCESSOR_ARCHITEW6432%"=="" goto native
%SystemRoot%\Sysnative\cmd.exe /c %0 %*
exit

:native
rem set PS=%SystemRoot%\sysnative\WindowsPowerShell\v1.0\powershell.exe
Powershell set-executionpolicy unrestricted -force
echo add-pssnapin vmware.view.broker > C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
Powershell -command ". \"c:\Program Files\VMware\VMware View\Server\extras\PowerShell\add-snapin.ps1\"" 