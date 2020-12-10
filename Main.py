# https://chromedriver.chromium.org/downloads 
# download the above file and put it in the same folder

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

driver = None
URL = "https://teams.microsoft.com"
Email = "" # Enter email here
Passowrd = "" # Enter password here
waitTimer = 2
AllIsReady = False
AtLecture = -1

Courses = [
    # Day of meeting 0-6 starts with sunday , Meeting start time ex:1820 , Meeting end time ex:1820, Meeting name , meeting link
    ["0", "1820", "1830", "Meeting 1",
     "https://teams.microsoft.com/dl/launcher/launcher.html?url=%2F_%23%2Fl%2Fmeetup-join%2F19%3Ac820eb22b4064ef492d3506d75cdce10%40thread.tacv2%2F1603813316570%3Fcontext%3D%257B%2522Tid%2522%253A%25222b773d99-f229-4704-b562-5a3198831779%2522%252C%2522Oid%2522%253A%2522c4ce19c8-405e-4c12-b77f-f657d43c04b6%2522%257D%26anon%3Dtrue&type=meetup-join&deeplinkId=9a37a2ca-b30c-4c6f-82c0-e8a6f6827aac&directDl=true&msLaunch=true&enableMobilePage=true&suppressPrompt=true"],
]

print("Script is now running")

def start_browser():
    global driver
    driver = webdriver.Chrome(options=opt)

    driver.get(URL)

    WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

    # if "login.microsoftonline.com" in driver.current_url:
    login()


def login():
    # login required
    global driver, AllIsReady
    print("logging in")
    time.sleep(waitTimer)
    emailField = driver.find_element_by_xpath('//*[@id="i0116"]')
    emailField.click()
    emailField.send_keys(Email)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()  # Next button
    time.sleep(waitTimer)
    passwordField = driver.find_element_by_xpath('//*[@id="i0118"]')
    passwordField.click()
    passwordField.send_keys(Passowrd)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()  # Sign in button
    time.sleep(waitTimer)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()  # remember login
    time.sleep(waitTimer)
    AllIsReady = True
    print("Everything is running")
    Bot()


def joinMeeting(Link):
    driver.get(Link)  # Go to link of meeting
    driver.find_element_by_xpath('//*[@data-tid="joinOnWeb"]').click()  # Enter on web button
    time.sleep(waitTimer)


    for i in driver.find_elements_by_class_name("style-layer"):
        if i.get_attribute("title") == 'Turn camera off' or i.get_attribute("title") == 'Mute microphone':
            i.click()
            time.sleep(waitTimer)



    driver.find_element_by_class_name('button-col').click() # Join button


def Bot():
    global driver, AllIsReady, AtLecture
    while AllIsReady:

        t = time.localtime()
        current_time = time.strftime("%H%M%w", t)

        Hour = current_time[:2]
        Min = current_time[2:4]
        Day = current_time[4]

        if AtLecture == -1:
            for i in range(len(Courses)):
                if Courses[i][0] == Day and Courses[i][1][:2] == Hour and Courses[i][1][2:] == Min:
                    joinMeeting(Courses[i][4])
                    time.sleep(waitTimer)
                    AtLecture = i
                    print("Joined Course ", Courses[i][3])
        else:
            if Courses[AtLecture][0] == Day and Courses[AtLecture][2][:2] == Hour and Courses[AtLecture][2][2:] == Min:
                driver.find_element_by_class_name("ts-calling-screen").click()

                driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click()  # come back to homepage
                time.sleep(waitTimer)

                driver.find_element_by_xpath('//*[@id="hangup-button"]').click()

                print("Left Course ", Courses[AtLecture][3])
                AtLecture = -1

        time.sleep(waitTimer)


start_browser()
