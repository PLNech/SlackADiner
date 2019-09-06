import googletrans
import requests
from bs4 import BeautifulSoup
from datetime import date

str_date = date.today().strftime("%d-%m-%Y")
url_base = "https://55-amsterdam.sohappy.work/?id=1968"
url_new_order_get = url_base + "&e=zr"
url_new_order_post = url_base + "&e=zro"
url_start_order = url_base + "&e=zro.start&d=%s" % str_date
url_menu = url_base + "&e=zro.cr&crid=3"


def main():
    print("Meal:", get_meal())


def get_meal():
    translator = googletrans.Translator()
    with requests.Session() as session:
        reset_session(session)
        start_new_command(session)

        res = session.get(url_menu)  # Get menu
        soup_diner = make_soup(res)

        meal_diner_select = soup_diner.find("select", {"class": "js-item-quantity"})
        quantity = int(meal_diner_select.find_all("option")[-1].get_text())
        meal_diner_div = meal_diner_select.parent.parent.parent
        meal_diner = meal_diner_div.find("h3").get_text().strip()
    return meal_diner, translator.translate(meal_diner).text, quantity


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
                              headers={
                                  'User-Agent': 'SlackADiner Bot',
                                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                  'Accept-Language': 'en-US,en;q=0.5',
                                  'Referer': 'https://55-amsterdam.sohappy.work/',
                                  'Content-Type': 'application/x-www-form-urlencoded',
                                  'Connection': 'keep-alive',
                                  'Upgrade-Insecure-Requests': '1',
                              },
                              params=(('e', 'user.logout'),), )
    soup_logout = make_soup(res_logout)
    if "Connectez-vous" in soup_logout.find("h1", {"class": "h2"}).get_text():
        print("Logout successful.")
    else:
        print("Failed to logout!?")
        exit(-1)


def login(session):
    res_login = session.post('https://55-amsterdam.sohappy.work/',
                             headers={
                                 'User-Agent': 'SlackADiner Bot',
                                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                 'Accept-Language': 'en-US,en;q=0.5',
                                 'Referer': 'https://55-amsterdam.sohappy.work/',
                                 'Content-Type': 'application/x-www-form-urlencoded',
                                 'Connection': 'keep-alive',
                                 'Upgrade-Insecure-Requests': '1',
                             },
                             params=(('e', 'main.connect'),),
                             data={
                                 'loginOrMail': 'pln+bot@algolia.com',
                                 'pwd': 'free4bot@SH',
                                 'isStayConnected': ''
                             })
    soup_login = make_soup(res_login)
    text = soup_login.find("div", {"class": "header-account-menu"}).find("span", {"class": "picto-label"}).get_text()
    if "Déconnexion" in text:
        print("Login successful.")
    else:
        print("Failed to login!?")
        exit(-1)


def make_soup(res):
    return BeautifulSoup(res.content, 'html.parser')


if __name__ == "__main__":
    main()
