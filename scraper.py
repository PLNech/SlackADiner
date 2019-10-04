#! /usr/bin/env python

import os
import re
from datetime import date

import googletrans
import requests
from bs4 import BeautifulSoup

from didyoumean3.didyoumean import did_you_mean
from menu import Diner, Menu

id_lunch = 930
id_diner = 1968
str_date = date.today().strftime("%d-%m-%Y")
url_base = "https://55-amsterdam.sohappy.work/?id=%i"
url_diner = url_base % id_diner
url_new_order_get = url_diner + "&e=zr"
url_new_order_post = url_diner + "&e=zro"

url_start_order = url_diner + "&e=zro.start&d=%s" % str_date
url_diner_menu = url_new_order_post + ".cr"
url_diner_meals = url_diner_menu + "&crid=3"
url_diner_desserts = url_diner_menu + "&crid=7"

url_lunch = url_base % id_lunch + "&e=zr"


def main():
    print(get_lunch())


def with_missing_accents(course_name: str):
    accented_words = ["sauté", "braisé", "grillé", "doré", "flambé", "glacé", "poché", "haché", "caramelisé"]
    accented_words += [word + "e" for word in accented_words]
    accented_words += [word + "s" for word in accented_words]

    for word in accented_words:
        unaccented_word = word.replace("é", "e")
        match = re.search(r"\b%s\b" % re.escape(unaccented_word), course_name)
        if match is not None:
            course_name = course_name.replace(unaccented_word, word)
    return course_name


def get_lunch() -> Menu:
    menu = Menu()
    translator = googletrans.Translator()
    with requests.Session() as session:
        reset_session(session)

        res = session.get(url_lunch)
        soup_lunch = make_soup(res)
        today = soup_lunch.find("div", {'data-is-today': True})
        composantes = today.find_all("div", {"class": "composante-recette"})
        for composante in composantes:
            category = composante.find("h3", {"class": "recette-title"}).get_text()
            items = composante.find_all("li", {"class": "recette-item"})
            for item in items:
                dish = item.get_text().strip()
                try:
                    spellcheck = did_you_mean(dish)
                    if spellcheck.lower() != dish.lower():
                        dish = spellcheck
                except Exception as e:
                    print("Spellcheck failed:", e)
                print("Found available dish:", dish)
                menu[category].append((dish, translator.translate(dish, src="fr").text, None))
    return menu


def get_diner() -> Diner:
    menu = Diner()
    translator = googletrans.Translator()

    with requests.Session() as session:
        reset_session(session)
        start_new_command(session)

        for category, url in [("plats", url_diner_meals), ("desserts", url_diner_desserts)]:
            print("Looking for %s..." % category)

            res = session.get(url)  # Get menu
            soup_diner = make_soup(res)

            dish_diner_selects = soup_diner.find_all("select", {"class": "js-item-quantity"})

            for dish_select in dish_diner_selects:
                quantity = int(dish_select.find_all("option")[-1].get_text())
                dish_diner_div = dish_select.parent.parent.parent
                dish_diner = dish_diner_div.find("h3").get_text().strip()
                dish_diner = with_missing_accents(dish_diner)
                try:
                    spellcheck = did_you_mean(dish_diner)
                    if spellcheck.lower() != dish_diner.lower():
                        dish_diner = spellcheck
                except Exception as e:
                    print("Spellcheck failed:", e)
                print("Found available dish:", dish_diner)
                menu[category].append((dish_diner, translator.translate(dish_diner, src="fr").text, quantity))
    return menu


def start_new_command(session):
    """ Triggers the necessary requests to see available dishes. """
    session.get(url_new_order_get)
    session.post(url_new_order_post)
    session.post(url_start_order)


def reset_session(session):
    """ Resets the current session by logging-out and in again."""
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
