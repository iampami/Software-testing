import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_login(driver):
    driver.get("https://demo.opencart.com/")

    try:
        my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/account')]")

        driver.execute_script("arguments[0].scrollIntoView();", my_account_link)

        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
            )
            close_button.click()
        except Exception:
            pass  # Nếu không có popup, tiếp tục

        my_account_link.click()
        time.sleep(20)
        driver.find_element(By.ID, "input-email").send_keys("jcandie@gmail.com")
        driver.find_element(By.ID, "input-password").send_keys("000000")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(3)
        account_header = driver.find_element(By.XPATH, "//h2[normalize-space()='My Account']")
        assert account_header.is_displayed()
    except Exception as e:
        print(f"An error occurred: {e}")

def test_invalid_login(driver):
    driver.get("https://demo.opencart.com/")

    try:
        my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/account')]")

        driver.execute_script("arguments[0].scrollIntoView();", my_account_link)

        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
            )
            close_button.click()
        except Exception:
            pass  # Nếu không có popup, tiếp tục

        my_account_link.click()
        time.sleep(20)
        driver.find_element(By.ID, "input-email").send_keys("j@gmail.com")
        driver.find_element(By.ID, "input-password").send_keys("044546546")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(3)

        assert driver.page_source,"Warning: No match for E-Mail Address and/or Password."
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")

def test_logout(driver):

    driver.get("https://demo.opencart.com/")

    try:
        my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/account')]")

        driver.execute_script("arguments[0].scrollIntoView();", my_account_link)

        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
            )
            close_button.click()
        except Exception:
            pass  # Nếu không có popup, tiếp tục

        driver.find_element(By.ID, "input-email").send_keys("testZoe@gmail.com")
        driver.find_element(By.ID, "input-password").send_keys("123456")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".dropdown-toggle").click()
        time.sleep(5)
        driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/logout')]")
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
        time.sleep(2)

        assert my_account_link.is_displayed()
    except Exception as e:
        print(f"An error occurred: {e}")

def test_search_valid_keyword(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[contains(@name, 'search')]").send_keys("a")
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[contains(@class, 'btn-light')]").click()  # Click the search button
    time.sleep(2)
    product_items = driver.find_element(By.CLASS_NAME, "product-thumb").text
    assert "Apple Cinema 30" in product_items

def test_addtoCart(driver):
    driver.get("https://demo.opencart.com/")
    driver.execute_script("window.scrollBy(0, 500);")  # Cuộn xuống 500px
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[contains(@title, 'MacBook')]").click()
    time.sleep(10)
    add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(@id, 'button-cart')]")
    add_to_cart_button.click()
    time.sleep(5)

    # Assert that the cart contains the product
    assert driver.page_source, "Success: You have added MacBook to your shopping cart!"

def test_form_submission(driver):
    driver.get("https://demo.opencart.com/")
    driver.execute_script("window.scrollBy(0, 700);")  # Cuộn xuống 700px
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[contains(text(), 'Contact Us')]").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[contains(@name, 'name')]").send_keys("Candy")
    driver.find_element(By.XPATH, "//input[contains(@name, 'email')]").send_keys("jcandie@gmail.com")
    driver.find_element(By.XPATH, "//textarea[contains(@name, 'enquiry')]").send_keys("hahahahahahahahahahaha")
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 700);")
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
    time.sleep(2)

    account_header = driver.find_element(By.XPATH, "//h1[normalize-space()='Contact Us']")
    assert account_header.is_displayed()

def test_checkout(driver):
    driver.get("https://demo.opencart.com/")
    driver.execute_script("window.scrollBy(0, 500);")  # Cuộn xuống 500px
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[contains(@title, 'iPhone')]").click()
    time.sleep(10)
    add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
    add_to_cart_button.click()
    time.sleep(6)

    driver.find_element(By.XPATH, "//a[contains(@href, 'route=checkout/checkout')]").click()
    time.sleep(6)
    driver.find_element(By.XPATH, "//label[contains(text(), 'Guest Checkout')]"). click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[contains(@id, 'input-firstname')]").send_keys("Jennifer")
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-lastname')]").send_keys("Candy")
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-email')]").send_keys("jcandie@gmail.com")
    time.sleep(5)

    driver.find_element(By.XPATH, "//input[contains(@id, 'input-shipping-company')]").send_keys("My Company")
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-shipping-address-1')]").send_keys("quan 1")
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-shipping-city')]").send_keys("Thành Phố Hồ Chí Minh")
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-shipping-postcode')]").send_keys("70000")
    time.sleep(2)
    driver.find_element(By.XPATH, "//select[contains(@id, 'input-shipping-country')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//option[contains(@value, '230')]").click()

    driver.execute_script("window.scrollBy(0, 500);")  # Cuộn xuống 500px
    time.sleep(2)
    driver.find_element(By.XPATH, "//select[contains(@name, 'shipping_zone_id')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//option[contains(@value, '3780')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-newsletter')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[contains(@id, 'button-register')]").click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, -1000);")
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[contains(@id, 'button-shipping-methods')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-shipping-method-flat-flat')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='text-end']/button[@id='button-shipping-method']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[contains(@id, 'button-payment-methods')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[contains(@id, 'input-payment-method-cod-cod')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='text-end']/button[@id='button-payment-method']").click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[contains(@id, 'button-confirm')]").click()
    time.sleep(2)


    order_success = driver.find_element(By.XPATH, "//h1[contains(text(), 'Your order has been placed!')]")
    assert order_success.is_displayed()

def test_data_validation(driver):
    driver.get("https://demo.opencart.com/")

    my_account_link = driver.find_element(By.NAME, "search")
    my_account_link.clear()
    my_account_link.send_keys("iphone")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-light.btn-lg").click()
    time.sleep(10)

    product_items = driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
    driver.execute_script("arguments[0].scrollIntoView();", product_items[0])
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "iPhone").click()
    time.sleep(5)
    quantity = driver.find_element(By.ID, "input-quantity")
    quantity.clear()
    random_integer = random.randint(1, 100)
    # random_integer_str = str(random_integer)

    quantity.send_keys(str(random_integer))
    time.sleep(3)

    price = driver.find_element(By.CLASS_NAME, "price-new")
    numeric_value = float(price.text.replace("$", ""))

    driver.find_element(By.ID, "button-cart").click()
    time.sleep(10)
    cart_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-inverse.btn-block.dropdown-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", cart_button)
    cart_button.click()
    time.sleep(3)
    total_value_element = driver.find_element(By.XPATH, "//td[.='Total']/following-sibling::td")
    total_value = total_value_element.text

    # Lấy giá trị số từ chuỗi actual_value và làm tròn
    total = random_integer*numeric_value
    formatted_value = f"${total:,.2f}"

    assert total_value == formatted_value, f"Expected {formatted_value} but got {total_value}"