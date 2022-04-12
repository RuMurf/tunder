@echo off
title Install Dependencies
:: Install dependencies from requirements.txt
pip install -r requirements.txt
:: Madmom is a special little madam and won't register the fact that her dependencies 
:: are installed if she's installed from the same command as said dependencies.
:: Hence, she has to be installed from a separate command,
:: making this batch file necessary and my life even more difficult than it already had to be.
pip install madmom