from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from PIL import Image
from anticaptchaofficial.imagecaptcha import *
from vars import *
import os
import glob, sys, fitz


def captcha_solver(path):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(os.environ.get("CAPTCHA_SOLVER_KEY"))
    captcha_text = solver.solve_and_return_solution(path)
    if captcha_text != 0:
        print("solved successfully, the captcha is "+captcha_text)
        return captcha_text
    else:
        print("task finished with error "+solver.error_code)
        return -1
    

def get_captcha(driver,path):
    # driver.set_window_size(1080, 960)
    js = "window.scrollTo(0, 500);"
    driver.execute_script(js)
    driver.save_screenshot(os.path.join(path,"captcha.png"))
    img = Image.open(os.path.join(path,"captcha.png"))
    img = img.crop((149,210,327,263))
    # img = img.crop((295,210,474,264))
    img.save(os.path.join(path,"capture.png"),"png")

def pdf_to_images(input_path, path):
    zoom_x = 4.0  # horizontal zoom
    zoom_y = 4.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
    all_files = glob.glob(input_path)

    for filename in all_files:
        doc = fitz.open(filename)  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image
            pix.save(os.path.join(path,"page-%i.png") % page.number)  # store image as a PNG

def get_pdf_file():
    url = 'https://ebpp.cht.com.tw/ebpp/login/access.xhtml'
    store_path = "/tmp/"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    prefs = {'download.default_directory' : store_path}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    print("connecting...")
    driver.get(url) #發送請求
    print("connected")
    element = WebDriverWait(driver,1000).until(
        EC.presence_of_element_located((By.CLASS_NAME,"ui-button"))
        #原本是find by ID jdt_32, 但不知道為甚麼會變，改成固定抓取第一個ui-btn
    )
    element.click()
    account_input = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"uid"))
    )
    account_input.send_keys(ACCOUNT)

    #prevent captcha error
    while len(driver.find_elements(By.ID,"loginMsg")) != 0:
        driver.execute_script('el = document.elementFromPoint(0, 0); el.click();')#click anywhere, skip error hint
        time.sleep(1)
        password_input = driver.find_element(By.ID,"pw")
        password_input.send_keys(PASSWORD)
        get_captcha(driver,store_path)
        # break
        captcha_input = driver.find_element(By.ID,"confirmcode")
        solved_captcha = captcha_solver(os.path.join(store_path,"capture.png"))
        if solved_captcha == -1:
            return
        captcha_input.send_keys(solved_captcha)
        driver.find_element(By.ID,"btn-login").click()
        time.sleep(5)
        print("press login")
    # return "captcha.png"
    if len(driver.find_elements(By.ID,"nextBtn"))!=0:
        driver.find_element(By.ID,"nextBtn").click()
        time.sleep(3)
    print("login successful")
    if len(driver.find_elements(By.ID,"form:tbl:0:j_idt234_menuButton"))!=0:
        driver.find_element(By.ID,"form:tbl:0:j_idt234_menuButton").click()
        time.sleep(1)
        print("pressed open 0")
        driver.find_element(By.ID,"form:tbl:0:j_idt235").click()
        time.sleep(5)
        print("pressed download 0")
    else:
        driver.find_element(By.ID,"form:tbl:0:j_idt300_menuButton").click()
        time.sleep(1)
        print("pressed open 1")
        driver.find_element(By.ID,"form:tbl:0:j_idt301").click()
        time.sleep(5)
        print("pressed download 1")

    # WebDriverWait(driver,1000).until(
    #     EC.presence_of_element_located((By.ID,"form:j_idt111"))
    # ).click()
    #click 關閉

    print(os.listdir(store_path))
    for f in os.listdir(store_path):
        if f[-3:len(f)] == "pdf": 
            target_file = f

    print("download end")
    return target_file

