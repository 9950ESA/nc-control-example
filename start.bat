@echo off

start cmd /k "python -m http.server 12345"


start cmd /k "python printer.py"

start cmd /k "python simulator.py"
REM Exit the script
exit
