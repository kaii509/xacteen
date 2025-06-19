import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.app_package = "mn.xacbank.teen"
    options.app_activity = "mn.xacbank.teen.MainActivity"
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()


USERNAME = "akhuska"
PASSWORD = "2()1C@rtier$09"

def test_login_once(driver):
    wait = WebDriverWait(driver, 15)

    # Step 1: Tap the Sign In button
    try:
        sign_in_btn = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Нэвтрэх")')))
        sign_in_btn.click()
        time.sleep(1)
    except Exception as e:
        print(f"Failed to find Sign In button: {e}")
        return

    # Step 2: Determine screen type
    try:
        # Try finding the "Сайн уу" text indicating saved user flow
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Сайн уу")')))
        print("Detected saved-user login screen.")

        # If so, go back to full login screen
        back_button = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Өөр хэрэглэгч?")')))
        back_button.click()
        time.sleep(1)
    except:
        print("[i] Default login screen detected.")

    # Step 3: Enter username and password
    try:
        username_field = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText").instance(0)' )))
        username_field.clear()
        username_field.send_keys(USERNAME)
    except Exception as e:
        print(f"Username field error: {e}")
        return

    try:
        password_field = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.EditText").instance(1)')))
        password_field.clear()
        password_field.send_keys(PASSWORD)
    except Exception as e:
        print(f"Password field error: {e}")
        return

    try:
        login_btn = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Нэвтрэх")')))
        login_btn.click()
        print("Login button clicked.")
    except Exception as e:
        print(f"Login button error: {e}")

