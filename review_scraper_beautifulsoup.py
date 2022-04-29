import lxml
import requests
from bs4 import BeautifulSoup as sp
from random import randint
from time import sleep


# Send Get Request:
html = requests.get('https://www.tripadvisor.com.tr/SmartDeals-g297962-Antalya_Turkish_Mediterranean_Coast-Hotel-Deals.html')
#access = html.status_code
bs_hotels = sp(html.content, 'lxml')

#get hotel links
links = []
for review in bs_hotels.findAll('a', {'class': 'review_count'}):
    review_link = 'https://www.tripadvisor.in' + review['href']  # https://www.tripadvisor.com.tr for Turkish reviews
    review_link = review_link[:(review_link.find('Reviews') + 7)] + '-or{}' + review_link[(review_link.find('Reviews') + 7):] # for dinamic link
    print(review_link)
    links.append(review_link)

# Scrape Reviews:
reviews = []
hotel_num = 0
for link in links:
    review_num = 0
    hotel_num += 1
    #page_index = [5, 10, 15, 20, 25] for dinamic link
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    html2 = requests.get(link)  #link.format(i for i in page_index), headers=headers
    #print(html2)
    sleep(randint(1, 5))

    bs_reviews = sp(html2.content, 'lxml')
    for r in bs_reviews.findAll('q'):
        review_num += 1
        reviews.append(r.span.text.strip())
        print(f"hotel: {hotel_num} review:{review_num} -> {r.span.text.strip()}\n")





    
