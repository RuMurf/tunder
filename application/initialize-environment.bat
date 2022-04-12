@echo off
:: Intialize python virtual environment
python -m venv venv
:: Add root directory of application to PYTHONPATH
echo: >> venv\Scripts\activate.bat
echo set PYTHONPATH=%cd%;%%PYTHONPATH%% >> venv\Scripts\activate.bat
:: Activate virtual environment
venv\Scripts\activate.bat