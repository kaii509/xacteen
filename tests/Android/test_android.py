import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
from selenium.common.exceptions import TimeoutException

# Declare constants
APP_PACKAGE = "mn.xacbank.teen"
EXCEL_PATH = "/Users/khus1en/Documents/Internship Xac/XacTeen/tests/credentials.xlsx"

@pytest.fixture(scope="module")
def sheet():
    wb = load_workbook(EXCEL_PATH)
    ws = wb.active
    ws.cell(row=1, column=3).value = "Result"
    yield ws
    wb.save(EXCEL_PATH)
    wb.close()

def is_logged_in(driver):
    try:
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Сүүлийн гүйлгээнүүд")')
        return True
    except:
        return False

def logout(driver):
    wait = WebDriverWait(driver, 10)
    try:
        profile_btn = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(3)')))
        profile_btn.click()

        logout_btn = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Апп-аас гарах")')))
        logout_btn.click()
    except Exception as e:
        print(f"[!] Logout failed: {e}")

def ensure_login_screen(driver):
    wait = WebDriverWait(driver, 1)

    try:
        # CASE 1: Logged in → navigate to profile and log out
        profile_icon = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.ImageView").instance(3)'
        )))
        print("[i] Already logged in. Logging out.")
        profile_icon.click()

        logout_btn = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Апп-аас гарах")'
        )))
        logout_btn.click()
        time.sleep(2)

        # Wait for login button to appear again
        wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Нэвтрэх")'
        )))
        return

    except Exception:
        print("[i] Not already logged in. Checking screen...")

    # CASE 2: Press sign in button if present
    try:
        sign_in = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Нэвтрэх")'
        )))
        sign_in.click()
        time.sleep(1)
    except Exception:
        print("[!] Sign-in button not found, maybe already in login screen.")

    # CASE 3: Handle saved-user screen (e.g., greeting)
    try:
        wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Сайн уу")'
        )))
        print("[i] Found saved user screen. Navigating to default login.")

        other_user_btn = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Өөр хэрэглэгч?")'
        )))
        other_user_btn.click()
        time.sleep(1)
    except:
        print("[i] Default login screen ready.")


def test_login_from_excel(driver, sheet):
    wait = WebDriverWait(driver, 1)
    driver.activate_app(APP_PACKAGE)
    row = 2 # Starting from the second row in the Excel file

    while True:
        ensure_login_screen(driver)

        username = sheet.cell(row=row, column=1).value
        password = sheet.cell(row=row, column=2).value

        if not username or not password:
            break

        # Enter username
        try:
            username_field = wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)'
            )))
            username_field.clear()
            username_field.send_keys(username)
        except Exception as e:
            sheet.cell(row=row, column=3).value = "failed"
            continue

        # Enter password
        try:
            password_field = wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)'
            )))
            password_field.clear()
            password_field.send_keys(password)
        except Exception as e:
            sheet.cell(row=row, column=3).value = "failed"
            continue

        # press on login button
        try:
            login_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Нэвтрэх")')))
            login_btn.click()
        except:
            print("Login button click failed.")

        time.sleep(2)
        if is_logged_in(driver):
            sheet.cell(row=row, column=3).value = "passed"
            logout(driver)
        else:
            sheet.cell(row=row, column=3).value = "failed"

        row += 1 
        
        # Reset app for next test
        driver.terminate_app(APP_PACKAGE)
        time.sleep(2)
        driver.activate_app(APP_PACKAGE)
        time.sleep(2)



