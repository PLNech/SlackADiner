#! /usr/bin/env python

import os
import re
from datetime import date

import googletrans
import requests
from bs4 import BeautifulSoup

from didyoumean3.didyoumean import did_you_mean

str_date = date.today().strftime("%d-%m-%Y")
url_base = "https://55-amsterdam.sohappy.work/?id=1968"
url_new_order_get = url_base + "&e=zr"
url_new_order_post = url_base + "&e=zro"
url_start_order = url_base + "&e=zro.start&d=%s" % str_date
url_menu = url_base + "&e=zro.cr&crid=3"


def main():
    print("Meals:", get_meals())


def with_missing_accents(meal_name: str):
    accented_words = ["sauté", "braisé", "grillé", "doré", "flambé", "glacé", "poché"]
    accented_words += [word + "e" for word in accented_words]
    accented_words += [word + "s" for word in accented_words]

    print("words: ", accented_words)

    for word in accented_words:
        unaccented_word = word.replace("é", "e")
        match = re.search(r"\b%s\b" % re.escape(unaccented_word), meal_name)
        if match is not None:
            meal_name = meal_name.replace(unaccented_word, word)
            print("Replacing ", word)
    return meal_name


def get_meals():
    meals = []
    translator = googletrans.Translator()

    with requests.Session() as session:
        reset_session(session)
        start_new_command(session)

        res = session.get(url_menu)  # Get menu
        soup_diner = make_soup(res)

        meal_diner_selects = soup_diner.find_all("select", {"class": "js-item-quantity"})

        for meal_select in meal_diner_selects:
            quantity = int(meal_select.find_all("option")[-1].get_text())
            meal_diner_div = meal_select.parent.parent.parent
            meal_diner = meal_diner_div.find("h3").get_text().strip()
            meal_diner = with_missing_accents(meal_diner)
            try:
                spellcheck = did_you_mean(meal_diner)
                if spellcheck.lower() != meal_diner.lower():
                    meal_diner = spellcheck
            except Exception as e:
                print("Spellcheck failed:", e)
            print("Found available meal:", meal_diner)
            meals.append((meal_diner, translator.translate(meal_diner).text, quantity))
    return meals


def start_new_command(session):
    # Start new command
    session.get(url_new_order_get)
    session.post(url_new_order_post)
    session.post(url_start_order)


def reset_session(session):
    # Reset session
    logout(session)
    login(session)


def logout(session):
    res_logout = session.post('https://55-amsterdam.sohappy.work/',
                              params=(('e', 'user.logout'),), )
    soup_logout = make_soup(res_logout)
    if "Connectez-vous" in soup_logout.find("h1", {"class": "h2"}).get_text():
        print("Logout successful.")
    else:
        print("Failed to logout!?")
        exit(-1)


def login(session):
    res_login = session.post('https://55-amsterdam.sohappy.work/',
                             params=(('e', 'main.connect'),),
                             data={
                                 'loginOrMail': os.environ["SOHAPPY_USERNAME"],
                                 'pwd': os.environ["SOHAPPY_PASSWORD"],
                                 'isStayConnected': ''
                             })
    soup_login = make_soup(res_login)
    text = soup_login.find("div", {"class": "header-account-menu"}).find("span",
                                                                         {"class": "picto-label"}).get_text()
    if "Déconnexion" in text:
        print("Login successful.")
    else:
        print("Failed to login!?")
        exit(-1)


def make_soup(res):
    return BeautifulSoup(res.content, 'html.parser')


if __name__ == "__main__":
    main()
