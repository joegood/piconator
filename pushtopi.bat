@echo off

:: This will be run via postbuild commands.
:: It pushes files over via pscp (http://the.earth.li/~sgtatham/putty/latest/x86/pscp.exe)
:: PowerShell will soon support SSH and at that time I will probably change.
:: 

setlocal
pushd .

set app="C:\Program Files (x86)\PuTTY\pscp.exe"
set REMOTE_FOLDER="/home/pi/matrix/piconator/bin/Debug"

pscp -l pi -pw ##91x3Aa woah.xyzzy "wifi config.txt" 10.10.10.144:
%app% woah.xyzzy "wifi config.txt" pi@10.10.10.144:

start %app% "SysAdmin - 0 - Guide.bmml"

popd
endlocal

