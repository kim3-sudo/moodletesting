import os
import json
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def generate(users, courses):
    """
    Generate a set of actions

    Parameters
    ----------
    None

    Return
    ------
    String, String
    Two strings with a random username and a random course
    """
    username = random.choice(users)
    course = random.choice(courses)
    return username,course


def login(uri, driver, username, password):
    """
    Login function

    Parameters
    ----------
    uri : string
        The host URI
    driver : Selenium webdriver
        A webdriver object to control browser with
    username : string
        A username string
    password : string
        The user's password

    Return
    ------
    None

    """
    driver.implicitly_wait(3)
    driver.get(uri)
    driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/nav/ul[2]/li[2]/div/span/a').click()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginbtn").click()
    try:
        driver.find_element(By.XPATH, '/html/body/span/div/div/div[4]/button[3]').click()
        print("Tutorial modal found and dismissed")
    except:
        print("No tutorial modal")

def logout(uri, driver):
    """
    Logout function

    Parameters
    ----------
    uri : string
        The host URI

    Return
    ------
    None
    """
    print("Logging out user")
    driver.find_element(By.XPATH, "//a[contains(@aria-label, 'User menu')]").click()
    driver.find_element(By.XPATH, "//a[contains(@href, 'logout.php')]").click()

def rng1(driver, course):
    """
    Accesses a course passed in

    Parameters
    ----------
    driver : Selenium webdriver
        A webdriver object to control browser with
    course : string
        A course string

    Return
    ------
    None

    """
    print("RNG 1: Access course")
    driver.find_element(By.XPATH, "//a[contains(@href, 'course/view.php?id=" + course + "')]").click()
    try:
        driver.find_element(By.XPATH, "/html/body/span/div/div/div[4]/button[3]").click()
        print("Course tutorial modal found and dismissed")
    except:
        print("No tutorial modal")

def rng2(driver, uri):
    """
    Accesses a random user's profile (ID between 2, 1000)

    Parameters
    ----------
    driver : Selenium webdriver
        A webdriver object to control browser with
    uri : string
        The host URI

    Return
    ------
    None

    """
    print("RNG 2: Access user")
    userid = str(random.choice(range(2, 1000)))
    driver.get(uri + "/user/view.php?id=" + userid)
    try:
        driver.find_element(By.XPATH, "/html/body/span/div/div/div[4]/button[3]").click()
        print("Course tutorial modal found and dismissed")
    except:
        print("No tutorial modal")

def rng3(driver, uri, course):
    """
    Accesses a random user's profile (ID between 2, 1000) also enrolled in course

    Parameters
    ----------
    driver : Selenium webdriver
        A webdriver object to control browser with
    uri : string
        The host URI
    course : string
        A course string

    Return
    ------
    None

    """
    print("RNG 3: Access user in course")
    userid = str(random.choice(range(2, 1000)))
    driver.get(uri + "/user/view.php?id=" + userid + "&course=" + course)
    try:
        driver.find_element(By.XPATH, "/html/body/span/div/div/div[4]/button[3]").click()
        print("Course tutorial modal found and dismissed")
    except:
        print("No tutorial modal")

def rng4(driver, uri):
    """
    Accesses a random user's profile (ID between 2, 1000) and submits Essay.odt on their behalf

    Parameters
    ----------
    driver : Selenium webdriver
        A webdriver object to control browser with
    uri : string
        The host URI

    Return
    ------
    None

    """
    print("Getting course 9")
    driver.find_element(By.XPATH, "//a[contains(@href, 'course/view.php?id=9')]").click()
    print("On course ID 9")
    driver.implicitly_wait(2)
    try:
        driver.find_element(By.XPATH, "/html/body/span/div/div/div[4]/button[3]").click()
        print("Course tutorial modal found and dismissed")
    except:
        print("No tutorial modal")
    driver.implicitly_wait(2)
    print("Selecting assignment")
    driver.find_element(By.XPATH, "//a[contains(@href, 'assign/view.php?id=140')]").click()
    driver.implicitly_wait(2)
    try:
        print("Trying to remove old submission")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Remove submission')]").click()
        driver.implicitly_wait(0.5)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
        driver.implicitly_wait(0.5)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Edit submission')]").click()
    except:
        print("Unable to remove old submission (maybe it doesn't exist). Adding instead.")
        print("Selecting Add submission button")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add submission')]").click()
    driver.implicitly_wait(0.5)
    submissiontype = random.choice([True, False]) # True is online text, false is upload
    #submissiontype = True
    if submissiontype == True:
        print("Uploading in web editor")
        essay = ""
        with open('./essay.txt', 'r') as f:
            essay = f.read()
        print("Essay preview: " + essay[0:50])
        driver.find_element(By.ID, "id_onlinetext_editoreditable").click()
        actions = ActionChains(driver)
        actions.send_keys(essay)
        actions.perform()
        #driver.find_element(By.ID, "id_onlinetext_editor").send_keys(essay)
        #driver.find_element(By.ID, "id_onlinetext_editor").send_keys(essay)
    else:
        print("Uploading as document")
        essay = "./Essay.odt"
        driver.find_element(By.XPATH, "//a[contains(@title, 'Add...')]").click()
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, "//span[contains(text(), 'Upload a file')]").click()
        driver.implicitly_wait(1)
        print("Sending essay string")
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(os.getcwd() + "/" + essay)
        print("Essay string sent")
        print("Uploading file")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Upload this file')]").click()
    driver.implicitly_wait(2)
    print("Submitting essay")
    driver.find_element(By.XPATH, "//input[contains(@name, 'submitbutton')]").click()
    print("Essay submitted")

def simaction(threads, driver, service, options, uri, users, courses, password):
    try:
        print("Generating random username and course")
        username, course = generate(users, courses)
        login(uri, driver, username, password)
        driver.implicitly_wait(5)
        rngaction = random.choice(list(range(1,4)))
        #rngaction = 4
        print("RNG action " + str(rngaction))
        if (rngaction == 1):
            rng1(driver, course)
        elif (rngaction == 2):
            rng2(driver, uri)
        elif (rngaction == 3):
            rng3(driver, uri, course)
        elif (rngaction == 4):
            rng4(driver, uri)
        else:
            rng1(driver, course)
        logout(uri, driver)
        print("Destroying driver")
        driver.quit()
        print("Driver destroyed")
    except:
        print("Destroying driver")
        driver.quit()
        print("Driver destroyed")

def main():
    print("Initializing options")
    options = Options()
    #print("Adding options: headless")
    #options.add_argument('--headless')
    print("Creating service")
    service = Service(ChromeDriverManager().install())
    uri = "http://192.168.122.61"
    print("Set URI to" + uri)
    print("Creating users list from usernames.json")
    users = json.loads(open("usernames.json").read())
    print("Creating courses list from courses.json")
    courses = json.loads(open("courses.json").read())
    print("Setting global user password")
    password = "Kenyon5%"
    while True:
        print("Initializing threads")
        numthreads = 5
        threads = []
        drivers = []
        for i in range(numthreads):
            print("Initializing driver " + str(i))
            drivers.append(webdriver.Chrome(service = service, options = options))
            print("Initialized driver " + str(i))
        print("Initialized thread environment")
        for i in range(numthreads):
            t = threading.Thread(target = simaction, args = (numthreads, drivers[i], service, options, uri, users, courses, password))
            print("Initialized thread")
            t.daemon = True
            threads.append(t)
        for i in range(numthreads):
            print("Starting threads")
            threads[i].start()
        for i in range(numthreads):
            print("Joining threads")
            threads[i].join()


if __name__ == "__main__":
    main()
