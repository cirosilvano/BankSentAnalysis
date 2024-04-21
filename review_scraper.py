# This program scrapes trustpilot.com for reviews of banks in italian

import requests
import json
from bs4 import BeautifulSoup

ratings_path = "ratings.json"
reviews_path = "reviews.json"

url_base = "https://it.trustpilot.com/review/"

reviewcard_class = "styles_reviewCardInner__EwDq2"
paragraph_class = "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
imgreview_prefix = "https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-"
max_pages = 100

review_texts = []
review_ratings = []

companies = [
    "www.widiba.it",
    "www.flowe.com",
    "ing.it",
    "www.credem.it",
    "bancagenerali.it",
    "iblbanca.it"
]

for j in range(len(companies)):

    url = url_base + companies[j]

    for i in range(max_pages):
        print("iteration",i)
        req_url = url+f"?page={i+1}"
        page = requests.get(req_url)
        parsed_page = BeautifulSoup(page.content, "html.parser")
        
        # check if we hit a page out of bounds, in this case we're redirected
        # to the first page and we want to break
        if i>1 and page.url == url: 
            break
        
        review_cards = parsed_page.find_all(class_=reviewcard_class)
        
        for card in review_cards:
            review_par = card.find("p", class_=paragraph_class)
            if(review_par != None):
                review_text = review_par.text.strip()
                star_img = card.find("img", src=lambda s: s and s.startswith(imgreview_prefix))
                star_rating = int(star_img["src"].split("stars-")[-1][0])
                review_texts.append(review_text)
                review_ratings.append(star_rating)

with open(ratings_path, "w") as file:
    json.dump(review_ratings, file)

with open(reviews_path, "w") as file:
    json.dump(review_texts, file)
