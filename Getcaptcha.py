import logging
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
from tkinter import messagebox


def get_captcha(url, website_Xpath, upload_path, upload_path_filename, log_path):
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 避免讓網站自動關閉
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        # 關閉 "Chrome is being controlled by automated test software" 通知
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # chrome載入aa套件(.crx)
        if hasattr(sys, "_MEIPASS"):
            extension = os.path.join(sys._MEIPASS, "3.2.0.0_0.crx")
        else:
            extension = os.path.join(os.path.dirname(__file__), "3.2.0.0_0.crx")

        options.add_extension(extension)
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        # 輸入要爬取的網站url
        logging.info(f"造訪網站: {url}")
        driver.get(url)

        # ---------須執行javascript開啟網銀的網站---------#
        # 合庫
        if url == "https://cobank.tcb-bank.com.tw/home/newIBHome.html":
            # 切到新開啟的視窗
            driver.execute_script(
                "window.open('https://cobank.tcb-bank.com.tw/TCB.TWNB.CORP.WEB/','tcbcorpframe','resizable=yes, height=768, width=1024, scrollbars=yes, status=1, left=0, top=0, location=no');"
            )
            driver.switch_to.window(driver.window_handles[1])
            driver.maximize_window()

        # 瑞興
        if url == "https://ebank.taipeistarbank.com.tw":
            driver.execute_script("doLogin();")
        # ---------須執行javascript開啟網銀的網站---------#

        # 等待頁面完全載入
        time.sleep(5)

        element = None
        try:
            element = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, website_Xpath))
            )
            logging.info("在main中找到Xpath_element")
        except:
            logging.info("在main中未找到Xpath_element，開始在frame和iframe查詢")
            # 查找frames
            if element is None:
                frames = driver.find_elements(By.TAG_NAME, "frame")
                for frame in frames:
                    try:
                        driver.switch_to.frame(frame)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, website_Xpath)
                                )
                            )
                            if element:
                                logging.info("在frame中找到Xpath_element")
                                break
                        except:
                            driver.switch_to.default_content()
                            continue
                    except Exception as e:
                        logging.error(f"切換frame時發生錯誤: {e}")
                        driver.switch_to.default_content()
                        continue

            # 查找iframes
            if element is None:
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    try:
                        driver.switch_to.frame(iframe)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, website_Xpath)
                                )
                            )
                            if element:
                                logging.info("在iframe中找到Xpath_element")
                                break
                        except:
                            driver.switch_to.default_content()
                            continue
                    except Exception as e:
                        logging.error(f"切換iframe時發生錯誤: {e}")
                        driver.switch_to.default_content()
                        continue

        # 未找到元素
        if element is None:
            logging.error("未找到指定的元素，請檢查input")
            sys.exit(1)

        # 驗證碼截圖並存檔
        screenshot_path = os.path.join(upload_path, upload_path_filename)
        logging.info(f"驗證碼截圖並存檔至: {screenshot_path}")
        element.screenshot(screenshot_path)
        logging.info("截圖和存檔成功")

        # 解除自動化控制
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        messagebox.showinfo("Return", "驗證碼截取成功")
    except Exception as e:
        logging.error(f"發生錯誤: {e}")
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    url = sys.argv[1]
    website_Xpath = sys.argv[2]
    upload_path = sys.argv[3]
    upload_path_filename = sys.argv[4]
    log_path = sys.argv[5]

    result = get_captcha(
        url, website_Xpath, upload_path, upload_path_filename, log_path
    )
    print(result)
