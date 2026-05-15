@echo off
echo =======================================================
echo LAUNCHING INSTITUTIONAL PORTFOLIO DASHBOARDS...
echo =======================================================
echo.
echo Starting Project 1: Quantitative M.A. Sourcing Engine...
start /b C:\Users\evanb\AppData\Local\Programs\Python\Python312\python.exe -m streamlit run ma_dashboard.py --server.port 8501
echo.
echo Starting Project 2: Venture Capital Deal-Flow Engine...
start /b C:\Users\evanb\AppData\Local\Programs\Python\Python312\python.exe -m streamlit run vc_dashboard.py --server.port 8502
echo.
echo Starting Project 3: Sovereign Wealth Optimizer...
start /b C:\Users\evanb\AppData\Local\Programs\Python\Python312\python.exe -m streamlit run fo_dashboard.py --server.port 8503
echo.
echo Waiting for servers to spin up...
timeout /t 5 /nobreak > NUL
echo.
echo Opening all 3 dashboards in your web browser...
start http://localhost:8501
start http://localhost:8502
start http://localhost:8503
echo.
echo Dashboards are live! 
echo Keep this black window open as long as you want to view the websites.
echo When you are done, simply close this window to shut off the servers.
pause
