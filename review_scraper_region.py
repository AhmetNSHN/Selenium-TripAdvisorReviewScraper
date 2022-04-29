import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as sp
from selenium.webdriver import DesiredCapabilities
import sqlite3


class ds_bot:
    def __init__(self):

        # Send Get Request:
        html = requests.get(
            'https://www.tripadvisor.in/Hotels-g298033-Marmaris_Marmaris_District_Mugla_Province_Turkish_Aegean_Coast-Hotels.html')
        # access = html.status_code
        bs_hotels = sp(html.content, 'lxml')

        # get hotel links
        hotel_links = []
        for review in bs_hotels.findAll('a', {'class': 'review_count'}):
            review_link = 'https://www.tripadvisor.in' + review[
                'href']  # https://www.tripadvisor.com.tr for Turkish reviews
            review_link = review_link[:(review_link.find('Reviews') + 7)] + '-or{}' + review_link[(review_link.find(
                'Reviews') + 7):]  # for dinamic link
            print(review_link)
            hotel_links.append(review_link)

        # self.reviews = []
        self.review_num = 0
        self.review_page_counter = 0
        self.review_page_counter_reverse = 0
        self.previous_review_text = ""

        # selenium configurations ------------------------------------------------
        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "none"
        caps["pageLoadStrategy"] = "eager"
        self.bot = webdriver.Chrome(desired_capabilities=caps)
        mobile_emulation = {
            "userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/83.0.1025.133 Mobile Safari/535.19'}
        # options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.bot.set_window_size(1500, 1000)

        for hotel_link in hotel_links:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT link FROM hotel_links Where link = ?", (hotel_link,))
            check = result.fetchone()
            if check:
                print("this hotel reviews was scraped before")
                continue

            self.bot.get(hotel_link)
            discard = input("do you want to discard this hotel?")
            if discard == "y":
                self.c.execute("INSERT INTO hotel_links (link) VALUES (?)",(hotel_link,))
                continue
            time.sleep(15)
            try:
                self.set_filter()

            except:
                print("an error occured press n to continue")
                self.database_commit(hotel_link)
                continue

            self.get_reviews(mode=0)

            try:
                self.change_filter()
            except:
                print("an error occured press n to continue")
                self.database_commit(hotel_link)
                continue

            self.get_reviews(mode=1)
            self.database_commit(hotel_link)
            self.review_page_counter_reverse = 0
            self.review_page_counter = 0

    def get_reviews(self, mode):
        i = 0

        next_page = True
        while (next_page == True):
            if (mode == 1):
                self.review_page_counter_reverse += 1
                if (self.review_page_counter < self.review_page_counter_reverse):
                    break


            if (mode == 0):
                self.review_page_counter += 1

            time.sleep(7)

            bs_hotels = sp(self.bot.page_source, 'html.parser')
            first_item = True
            restart = True
            while restart:
                for r in bs_hotels.findAll('q'):
                    dummy_text = r.span.text.strip()
                    if first_item:
                        if self.previous_review_text == dummy_text:
                           print("page is not refreshed")
                           time.sleep(2)
                           continue
                        else:
                            restart = False

                    self.review_num += 1
                    # reviews.append(r.span.text.strip())

                    self.c.execute("INSERT INTO Training_Dataset (review, value) VALUES(?,?)",
                                   (dummy_text, mode))
                    print(f"review:{self.review_num} -> {dummy_text}\n")
                    if first_item:
                       self.previous_review_text = dummy_text
                       first_item = False

                if self.bot.find_elements_by_css_selector('[class="ui_button nav next primary disabled"]'):
                    next_page = False
                elif self.bot.find_elements_by_css_selector('[class="ui_button nav next primary "]'):
                    self.bot.find_element_by_css_selector('[class="ui_button nav next primary "]').click()
                    print("next button clicked")
                else:
                    print("no negative review for this hotel or only one page")
                    break

    def set_filter(self):
        self.bot.find_element_by_xpath(
            '//*[@id="component_15"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[4]/label').click()
        time.sleep(1)
        self.bot.find_element_by_xpath(
            '//*[@id="component_15"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[5]/label').click()
        print("reviews filtered (Negative)")
        time.sleep(5)

    def change_filter(self):
        self.bot.find_element_by_xpath(
            '//*[@id="component_15"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[1]/label').click()
        time.sleep(1)
        self.bot.find_element_by_xpath(
            '//*[@id="component_15"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[4]/label').click()
        time.sleep(1)
        self.bot.find_element_by_xpath(
            '//*[@id="component_15"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[5]/label').click()
        print("reviews filtered (Positive)")
        time.sleep(5)

    def database_commit(self, hotel_link):
        answer = input("Are you sure to commit new data?")
        if (answer == "y"):
            self.c.execute("INSERT INTO hotel_links (link) VALUES (?)",(hotel_link,))
            self.conn.commit()
            self.conn.close()
        if (answer == "n"):
            self.conn.rollback()
            self.conn.close()

run = ds_bot()


