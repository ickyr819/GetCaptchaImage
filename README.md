# GetCaptchaImage
使用方法:
1. 將整包CLONE到本地端
2. 開啟CMD
3. cd to getcaptha.exe path
4. Getcaptha.exe [parameters]
--parameters 包含 [url, website_Xpath, upload_path, upload_path_filename, log_path]--

把.py打包成exe
指令 :  pyinstaller --onefile --add-data "..\3.2.0.0_0.crx;." --noconsole Getcaptcha.py