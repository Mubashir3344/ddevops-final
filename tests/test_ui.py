from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

def test_frontend_sentiment():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(BASE_URL)

        text_input = driver.find_element(By.ID, "text-input")
        text_input.send_keys("This is a wonderful and amazing product")

        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()

        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.ID, "result-output").text.strip() != ""
        )

        result_output = driver.find_element(By.ID, "result-output")
        result_text = result_output.text

        assert result_text.strip() != "", "Result output should not be empty"
        assert any(word in result_text for word in ["POSITIVE", "NEGATIVE", "Confidence"]), \
            f"Expected POSITIVE, NEGATIVE, or Confidence in result, got: {result_text}"
    finally:
        driver.quit()
