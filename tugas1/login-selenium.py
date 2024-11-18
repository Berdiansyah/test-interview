from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pickle
import time
import os

# Path untuk menyimpan cookies
COOKIE_PATH = "shopee_cookies.pkl"

# Path ke chromedriver
CHROMEDRIVER_PATH = "Path your chromedriver"

# Konfigurasi WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Fungsi untuk menyimpan cookies
def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

# Fungsi untuk memuat cookies
def load_cookies(driver, path):
    if os.path.exists(path):
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                # Menghindari error karena key 'expiry' pada cookie
                if 'expiry' in cookie:
                    del cookie['expiry']
                driver.add_cookie(cookie)

# Fungsi login
def login_shopee(driver):
    driver.get("https://shopee.co.id/buyer/login")  # URL halaman login Shopee
    
    # Tunggu halaman termuat
    time.sleep(5)

    # Input username/email dan password
    username_input = driver.find_element(By.NAME, "loginKey")
    password_input = driver.find_element(By.NAME, "password")

    username = "Input Your Username"
    password = "Input Your Password"

    # Menunggu CAPTCHA atau 2FA diselesaikan
    print("Jika CAPTCHA atau 2FA muncul, selesaikan secara manual.")
    while True:
        time.sleep(5)  # Tunggu beberapa saat
        if "login" not in driver.current_url:  # Periksa apakah berhasil login
            print("Login berhasil.")
            break
        print("Masih di halaman login. Pastikan CAPTCHA atau 2FA diselesaikan.")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # Simpan cookies setelah login berhasil
    save_cookies(driver, COOKIE_PATH)
    print("Cookies berhasil disimpan.")

# Fungsi untuk memuat sesi dengan cookies
def load_session(driver):
    driver.get("https://shopee.co.id/")
    load_cookies(driver, COOKIE_PATH)
    driver.refresh()  # Refresh agar cookies diterapkan
    time.sleep(5)
    if "login" not in driver.current_url:
        print("Berhasil memuat sesi dengan cookies!")
    else:
        print("Cookies kadaluarsa atau belum login.")


def logout_shopee(driver):
    try:
        # Klik menu profil atau ikon logout
        profile_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")  # Sesuaikan dengan elemen logout Shopee
        profile_button.click()
        print("Berhasil logout.")
    except Exception as e:
        print(f"Gagal logout: {e}")

# Main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        if os.path.exists(COOKIE_PATH):
            print("Memuat ulang sesi menggunakan cookies...")
            
            # Refresh halaman untuk memverifikasi login
            driver.refresh()
            time.sleep(5)

            # Logout untuk menguji login ulang dengan cookies
            logout_shopee(driver)

            # Login ulang dengan cookies
            print("Login ulang dengan cookies...")
            load_session(driver)
        else:
            print("Belum ada cookies, login manual diperlukan.")
            login_shopee(driver)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()
