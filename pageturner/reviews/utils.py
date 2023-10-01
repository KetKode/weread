




























# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# import time
# import random
# from bs4 import BeautifulSoup
#
#
# random_sleep = [2, 3, 4, 5]
# TITLE = "Meet me at the lake"
#
# # create a webdriver instance
# driver = webdriver.Chrome()
# driver.get("https://www.google.com/")
#
# # open the website
# driver.get("https://www.goodreads.com/")
# time.sleep(2)
#
# book_lists = driver.find_element(By.XPATH, '//*[@id="listsTeaserBox"]/p/a')
# book_lists.click()
# time.sleep(3)
#
# close_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button')
# close_button.click()
# time.sleep(4)
#
# best_books_list = driver.find_element(By.XPATH, '//*[@id="bodycontainer"]/div[3]/div[1]/div[1]/div[4]/div[3]/div[2]/div/div[1]/a[1]')
# best_books_list.click()
# time.sleep(2)
#
# # all elements on the page
# # book_title = driver.find_elements(By.CLASS_NAME, "bookTitle")
# # author = driver.find_elements(By.CLASS_NAME, "authorName")
# # rating = driver.find_elements(By.CLASS_NAME, "minirating")
# # time.sleep(3)
#
# book_item = driver.find_element(By.CLASS_NAME, "bookTitle")
# book_item.click()
# time.sleep(5)
#
# # show_more_details = driver.find_element(By.LINK_TEXT, "Show more")
# # show_more_details.click()
# # print("success")
# # time.sleep(2)
#
# title = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='title']")
# print("success")
# publication_date = driver.find_element(By.CSS_SELECTOR, "div.dataItem[itemprop='datePublished']")
# author = driver.find_element(By.CSS_SELECTOR, "a[itemprop='author']")
# summary = driver.find_element(By.CSS_SELECTOR, "div#description span[itemprop='description']")
# isbn = driver.find_element(By.CSS_SELECTOR, "div.infoBoxRowItem[itemprop='isbn']")
# cover = driver.find_element(By.CSS_SELECTOR, "img.bookCover")
#
# books_dict = []
# book_info = {
#     "title": title.text,
#     "author": author.text,
#     "publication_date": publication_date.text,
#     "isbn": isbn.text,
#     "summary": summary.text,
#     "cover": cover.get_attribute("src")
#     }
# books_dict.append(book_info)
#
#
# print(books_dict)
#
#
#
# #     cover = driver.find_element(By.CLASS_NAME, "BookCover")
# #     genres = driver.find_element(By.CLASS_NAME, "BookPageMetadataSection__genres")
# #
# #     book_info.append(i)
# #
# # print(book_info)
#
#
#
#
#
#
# # for book in range(len(best_books_list_100))[:3]:
# #     book_title = driver.find_element(By.ID, "bookTitle")
# #     book_title.click()
# #     time.sleep(5)
# #     author = driver.find_element(By.CLASS_NAME, "ContributorLink__name")
# #     rating = driver.find_element(By.CLASS_NAME, "RatingStatistics__rating")
# #     cover = driver.find_element(By.CLASS_NAME, "ResponsiveImage")
# #     pages = driver.find_element(By.CLASS_NAME, "FeaturedDetails")
# #     genres = driver.find_element(By.CLASS_NAME, "BookPageMetadataSection__genres")
# #     # show_more = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[1]/div[2]/div[4]/div/div[2]/div/button/span[2]/i/svg/path')
# #     # summary = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[1]/div[2]/div[4]/div/div[1]/div/div/span')
# #     #
#
#
# # books_dict = []
# #
# # for book in range(len(best_books_list))[:3]:
# #     book_info = {
# #         "title": book_title[book].text,
# #         "author": author[book].text,
# #         "rating": rating[book].text,
# #         "cover": cover[book].get_attribute("src"),
# #         # "summary": summary[book].text,
# #         "pages": pages[book].text,
# #         "genres": genres[book].text,
# #         }
# #     books_dict.append(book_info)
# #
# #
# # print(books_dict)
#





