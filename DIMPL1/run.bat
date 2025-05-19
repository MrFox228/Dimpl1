@echo off
title Run server
echo [1/1] The server is starting..

python -m uvicorn main:app --reload

pause