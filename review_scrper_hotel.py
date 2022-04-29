import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup as sp
from selenium.webdriver import DesiredCapabilities
import sqlite3

class ds_bot:
        def __init__(self):

                hotel_link = "https://www.tripadvisor.in/Hotel_Review-g298658-d737330-Reviews-Parkim_Ayaz_Hotel-Bodrum_City_Bodrum_District_Mugla_Province_Turkish_Aegean_Coast.html#REVIEWS"
                self.review_range = 8


                self.reviews = []
                self.review_num = 0

                # selenium configurations ------------------------------------------------
                caps = DesiredCapabilities().CHROME
                # caps["pageLoadStrategy"] = "none"
                caps["pageLoadStrategy"] = "eager"
                self.bot = webdriver.Chrome(desired_capabilities=caps)
                mobile_emulation = {
                        "userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/83.0.1025.133 Mobile Safari/535.19'}
                # options.add_experimental_option("mobileEmulation", mobile_emulation)

                self.bot.get(hotel_link)
                self.bot.set_window_size(1500, 1000)
                time.sleep(10)

                self.conn = sqlite3.connect("database.db")
                self.c = self.conn.cursor()


                self.initial_phase()
                time.sleep(5)
                self.get_reviews(mode=0)
                self.change_filter()
                self.get_reviews(mode=1)
                self.database_commit()


        def initial_phase(self):
                self.bot.find_element_by_xpath(
                        '//*[@id="component_14"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[5]/label').click()
                print("reviews filtered (negative)")

                time.sleep(5)
                html_code = self.bot.page_source
                bs_hotels = sp(html_code, 'html.parser')
                for r in bs_hotels.findAll('q'):
                        self.review_num += 1
                        dummy_text = r.span.text.strip()
                        print(f"review:{self.review_num} -> {dummy_text}\n")
                        self.c.execute("INSERT INTO Training_Dataset (review, value) VALUES(?,?)",
                                       (dummy_text, 0))


        def get_reviews(self, mode):
                for i in range(1, self.review_range):

                        #self.bot.find_element_by_css_selector('.ui_button nav next primary ').click()
                        self.bot.find_element_by_css_selector('[class="ui_button nav next primary "]').click()
                        time.sleep(5)
                        #self.bot.find_element_by_xpath('//*[@id="component_14"]/div/div[3]/div[8]/div/a[1]').click()
                        print("next button clicked")
                        time.sleep(1)
                        print("next page = true")
                        bs_hotels = sp(self.bot.page_source, 'html.parser')
                        #time.sleep(5)
                        for r in bs_hotels.findAll('q'):
                                self.review_num += 1
                                # reviews.append(r.span.text.strip())
                                dummy_text = r.span.text.strip()
                                print(f"review:{self.review_num} -> {dummy_text}\n")
                                self.c.execute("INSERT INTO Training_Dataset (review, value) VALUES(?,?)",
                                               (dummy_text, mode))


        def change_filter(self):
                self.bot.find_element_by_xpath(
                        '//*[@id="component_14"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[1]/label').click()
                time.sleep(1)
                self.bot.find_element_by_xpath(
                        '//*[@id="component_14"]/div/div[3]/div[1]/div[1]/div[1]/ul/li[5]/label').click()
                print("reviews filtered (positive)")
                time.sleep(5)
                bs_hotels = sp(self.bot.page_source, 'html.parser')

                for r in bs_hotels.findAll('q'):
                        self.review_num += 1
                        # reviews.append(r.span.text.strip())
                        dummy_text = r.span.text.strip()
                        print(f"review:{self.review_num} -> {dummy_text}\n")
                        self.c.execute("INSERT INTO Training_Dataset (review, value) VALUES(?,?)",
                                       (dummy_text, 1))

        def database_commit(self):
                answer = input("Are you sure to commit new data?")
                if(answer == "y"):
                        self.conn.commit()
                        self.conn.close()
                if (answer == "n"):
                        self.conn.rollback()
                        self.conn.close()


run = ds_bot()








#c.execute("insert into jobs (job_title, job_category,company_name, job_description, required_qualifications, responsibilities, location, view, applicants_num)"
                #" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (entry_list))




