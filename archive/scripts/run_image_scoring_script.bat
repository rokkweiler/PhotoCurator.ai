@echo off


set CONDA_PATH=C:\Users\ryanr\anaconda3


set ENV_NAME=ImageScore


call "%CONDA_PATH%\Scripts\activate.bat" %ENV_NAME%


cd /d "C:\Users\ryanr\OneDrive\Documents\Programming\ImageScore"

python capture_irfanview_Scoring.py


call conda deactivate

pause