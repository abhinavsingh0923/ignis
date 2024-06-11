from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import re

def extract_numeric_value(text):
    return float(re.sub(r'[^\d.]+', '', text))

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin):
        self.coin = coin.lower()
        self.url = f"{self.BASE_URL}{self.coin}/"
        self.driver = webdriver.Chrome()

    def scrape(self):
        self.driver.get(self.url)
        data = {"coin": self.coin, "output": {}}

        try:
            stats_block = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'section-coin-stats'))
            )

            coin_name_element = self.driver.find_element(By.CSS_SELECTOR, 'span[class="sc-d1ede7e3-0 bEFegK"]')
            coin_name = coin_name_element.text.strip()
            data['coin'] = coin_name

            price_element = self.driver.find_element(By.CSS_SELECTOR, 'span[class="sc-d1ede7e3-0 fsQm base-text"]')
            price_change_element = self.driver.find_element(By.CSS_SELECTOR, 'p[class="sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI"]')

            data['output']['price'] = float(extract_numeric_value(price_element.text))

            price_change_text = price_change_element.text
            change_sign = 1 if 'up' in price_change_text else -1
            change_value = extract_numeric_value(price_change_text)
            data['output']['price_change'] = change_sign * change_value

            data_points = []
            try:
                data_points = WebDriverWait(stats_block, 10).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, 'flexBetween'))
                )
            except:
                print("Data points not found")

            for data_point in data_points:
                try:
                    key_element = data_point.find_element(By.CLASS_NAME, 'laHoVg')
                    value_element = data_point.find_element(By.CLASS_NAME, 'base-text')

                    key = key_element.text.strip()
                    value = extract_numeric_value(value_element.text)
                    data['output'][key.lower().replace(' ', '_')] = value
                except StaleElementReferenceException:
                    key_element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'laHoVg')))
                    value_element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'base-text')))

                    key = key_element.text.strip()
                    value = extract_numeric_value(value_element.text)
                    data['output'][key.lower().replace(' ', '_')] = value
                except:
                    continue

            try:
                main_block = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sc-d1ede7e3-0.cvkYMS.coin-info-links'))
                )

                stats_blocks = main_block.find_elements(By.CSS_SELECTOR, 'div[data-role="stats-block"]')

                for block in stats_blocks:
                    header = block.find_element(By.CSS_SELECTOR, 'div[data-role="header"] span[data-role="title"]').text
                    links = block.find_elements(By.CSS_SELECTOR, 'div[data-role="body"] a')

                    extracted_links = []
                    for link in links:
                        link_text = link.text.strip().lower()
                        link_href = link.get_attribute('href')

                        if header.lower() == 'contracts':
                            extracted_links.append({
                                "name": link_text,
                                "address": link_href.split('/')[-1]
                            })
                        elif header.lower() == 'official links':
                            extracted_links.append({
                                "name": link_text,
                                "link": link_href
                            })
                        elif header.lower() == 'socials':
                            extracted_links.append({
                                "name": link_text,
                                "url": link_href
                            })

                    if header.lower() == 'contracts':
                        data['output']['contracts'] = extracted_links
                    elif header.lower() == 'official links':
                        data['output']['official_links'] = extracted_links
                    elif header.lower() == 'socials':
                        data['output']['socials'] = extracted_links
            finally:
                self.driver.quit()

        except Exception as e:
            self.driver.quit()
            raise e

        return data
