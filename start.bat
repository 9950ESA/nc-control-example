@echo off

REM Start the simulator in a new command prompt window
start cmd /k "python simulator.py"

REM Start the client in another new command prompt window
start cmd /k "python client.py"

REM Exit the batch script
exit
