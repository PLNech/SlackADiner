import requests
from bs4 import BeautifulSoup

str_date = "06-09-2019"  # TODO: Dynamic
url_new_order_get = "https://55-amsterdam.sohappy.work/?e=zr&id=1968"
url_new_order_post = "https://55-amsterdam.sohappy.work/?e=zro&id=1968"
url_start_order = "https://55-amsterdam.sohappy.work/?e=zro.start&d=%s&id=1968" % str_date
url_menu = "https://55-amsterdam.sohappy.work/?e=zro.cr&crid=3&id=1968"


def main():
    print(get_meals())


def get_meals():
    with requests.Session() as session:
        reset_session(session)
        start_new_command(session)

        res = session.get(url_menu)  # Get menu
        soup_diner = make_soup(res)

        meals = [meal.get_text().strip() for meal in soup_diner.find_all("div", {"class": "product-box-content"})]
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
                              headers={
                                  'User-Agent': 'SlackADiner Bot',
                                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                  'Accept-Language': 'en-US,en;q=0.5',
                                  'Referer': 'https://55-amsterdam.sohappy.work/',
                                  'Content-Type': 'application/x-www-form-urlencoded',
                                  'Connection': 'keep-alive',
                                  'Upgrade-Insecure-Requests': '1',
                              },
                              params=(('e', 'user.logout'),),
                              cookies={
                                  'ICMD': '1',
                                  'CFID': '13969531',
                                  'CFTOKEN': 'e8e07c262782e019-DFE03B46-E9C4-D226-59262876C18EDFB1',
                                  'JSESSIONID': '933B6AAFCA056FBA03FDCF4835140620.Helium_instance_2',
                              })
    soup_logout = make_soup(res_logout)
    text = soup_logout.find("h1", {"class": "h2"}).get_text()
    if "Connectez-vous" in text:
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
