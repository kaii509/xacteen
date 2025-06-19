from appium.webdriver.common.appiumby import AppiumBy

def test_activity_indicators(driver):
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Activity Indicators").click()