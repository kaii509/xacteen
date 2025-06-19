import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions

@pytest.fixture
def driver():
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = "iPhone 16 Pro" 
    options.app = "/Users/khus1en/Library/Developer/Xcode/DerivedData/SimpleLogin-bahtonvuyipykkekefhifsjwwhht/Build/Products/Debug-iphonesimulator/SimpleLogin.app"
    options.set_capability("showXcodeLog", True)


    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()
