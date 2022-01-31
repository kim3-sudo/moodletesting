import json
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')

service = Service(ChromeDriverManager().install())


uri = "http://192.168.122.61/index.php"

users = json.loads(open("usernames.json").read())
courses = json.loads(open("courses.json").read())
password = "Kenyon5%"

def generate():
    """
    Generate a set of actions
    """
    username = random.choice(users)
    course = random.choice(courses)
    return username,course


def simulatelogin():
    """
    Main execution

    Parameters
    ----------
    None

    Return
    ------
    None

    """
    print("Initialized thread")
    print("Initializing driver")
    driver = webdriver.Chrome(service = service, options = options)
    driver.implicitly_wait(5)
    driver.get(uri)
    username, course = generate()
    LoginXpath = '//*[@id="page-wrapper"]/nav/ul[2]/li[2]/div/span/a'
    driver.find_element(By.XPATH, LoginXpath).click()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginbtn").click()
    try:
        NextXpath = '/html/body/span/div/div/div[4]/button[3]'
        driver.find_element(By.XPATH, NextXpath).click()
    except:
        print("No tutorial modal")
    rngaction = random.choice(list(range(1, 3)))
    if (rngaction == 1):
        CourseXpath = course
        driver.find_element(By.XPATH, CourseXpath).click()
    elif (rngaction == 2):
        CourseXpath = course
        driver.find_element(By.XPATH, CourseXpath).click()
    else:
        CourseXpath = course
        driver.find_element(By.XPATH, CourseXpath).click()
    driver.quit()

def main():
    while True:
        print("Initializing threads")
        numthreads = 10
        threads = []
        for i in range(numthreads):
            t = threading.Thread(target = simulatelogin)
            t.daemon = True
            threads.append(t)
        for i in range(numthreads):
            threads[i].start()
        for i in range(numthreads):
            threads[i].join()


if __name__ == "__main__":
    main()
