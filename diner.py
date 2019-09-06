import requests
from bs4 import BeautifulSoup


def main():
    url_pret_a_diner = "https://55-amsterdam.sohappy.work/?e=zro.cr&crid=3&id=1968"

    # Get started
    res = requests.get("https://55-amsterdam.sohappy.work/?e=zr&id=1968")
    soup_home = make_soup(res)
    print("Got home:", soup_home.title.string)

    # Logout
    res_logout = requests.post('https://55-amsterdam.sohappy.work/',
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

    # Login
    res_login = requests.post('https://55-amsterdam.sohappy.work/',
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
    print(res_login.content)
    exit(0)

    # Get menu
    res = requests.get(url_pret_a_diner, cookies={
        'ICMD': '1',
        'CFID': '13969531',
        'CFTOKEN': 'e8e07c262782e019-DFE03B46-E9C4-D226-59262876C18EDFB1',
        'JSESSIONID': '933B6AAFCA056FBA03FDCF4835140620.Helium_instance_2',
    })
    soup_diner = make_soup(res)
    print(soup_diner.prettify())


def make_soup(res):
    return BeautifulSoup(res.content, 'html.parser')


if __name__ == "__main__":
    main()
