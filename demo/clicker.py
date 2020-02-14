from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep
import os, sys, argparse, contextlib, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netvd.settings')
django.setup()

from netvd.settings import DATABASES
from django.contrib.auth.models import User, Group
from xss.models import Session

def login(driver):
    driver.get("http://10.12.31.171:8000/register/login/")
    username = driver.find_element_by_name("username")
    username.send_keys("admin")
    password = driver.find_element_by_name("password")
    password.send_keys("")
    login_button = driver.find_element_by_xpath("/html/body/form/input[2]")
    login_button.click()

def is_fake(username):
    try:
        username.groups.get(name="FakeAdmin")
        return False
    except:
        return True

def get_users():
    users = User.objects.filter(is_staff=False)
    users = list(filter(is_fake,users))
    return users

def browser_session(driver1, i):
    login(driver1)
    driver1.get("http://10.12.31.171:8000/xss/204161404348169841998158196377303846736")
    sessionid = driver1.get_cookie("sessionid")["value"]
    user = User.objects.get(pk=i.id)
    Session.objects.get_or_create(user=user, number=sessionid)
    btn = driver1.find_element_by_name(i.id)
    btn.click()
    try:
        WebDriverWait(driver1, 2).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver1.switch_to.alert
        alert.accept()
        
    except TimeoutException:
        pass   

def main():
    while True:
        users = get_users()
        for i in users:
            options = Options()
            options.headless = True

            driver1 = webdriver.Firefox(options=options,executable_path=r"/geckodriver")
            driver1.set_page_load_timeout(5)

            try:
                browser_session(driver1, i)

            except TimeoutException:
                print("timeout hit")
                driver1.close()            
            
        print("sleeping")
        sleep(60)

            




if __name__ == "__main__":
    main()