from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import sys
import shlex

""" Script for scraping e-sport betting information from website https://loot.bet/ (for educational purposes).
    (Here You can find some examples of using css selectors and selenium webdriver to obtain information
    from dynamic generated web pages).
    Before running this script, you'll need to install next packets: selenium(with geckodriver if on Windows), 
    bs4 and Firefox web browser.
    After importing this script into your own code - use 'crawl_site()' function to start scraping. Obtained 
    information will return as list of lists of dictionaries, where dictionary represent information 
    about single game event, inner list - game events from one site page, outer list - all events.
    Here is example:
    [[{'game': name of the game, 'date': date of the event, 'player1': name of the first participant,
     'player2': second participant's name, 'odds1': bet rates on 1st player, 'odds2': bet rates on 2nd player},
     {another game information}, 
     ........
     ],
     [{}, {}, {}, ....]
     ........
    ]  
    You can run this script from the command line using parameter 'show' to print scraped data into terminal 
    window(also parameter 'help' available).    
"""


# https://github.com/Austerius
def parse_page(source_code, show):
    bs = BeautifulSoup(source_code, "html.parser")
    # getting block which contains all game events from a single page
    events_block = bs.select("section.tournaments div.match.ng-scope")
    current_time = datetime.datetime.utcnow()
    parsed_info = []  # we saving parsed info into this list
    # getting timezone
    timezone = bs.select_one("nav.navbar.navbar-fixed-top.navbar-top-bar.ng-scope li.dropdown a span.timezone.ng-binding")
    timezone = (timezone.get_text()).strip()
    site_time = timezone.split(" ")[2]  # here we have site time in string format
    site_hour, site_minutes = site_time.split(":")
    # Getting difference in minutes between current utc time and time, provided by site
    delta_time = (current_time.hour*60 + current_time.minute) - (int(site_hour)*60 + int(site_minutes))

    # Parsing every single event
    for event in events_block:
        date_string = event.select_one("div.flex-container.flex-item.left-side span.datetime.flex-container.ng-binding")
        date_string = (date_string.get_text()).strip()  # date of the event(need to be converted to UTC)

        # time-date shenanigans:
        temp_date = datetime.datetime.strptime(date_string, "%b %d, %H:%M")
        month = temp_date.month
        day = temp_date.day
        hour = temp_date.hour
        minute = temp_date.minute
        if (current_time.month == 12) and (month < 12):  # it's ok, since we don't scrape events from the past
            year = current_time.year + 1
        else:
            year = current_time.year
        # converting date_string to UTC time
        event_date = datetime.datetime(year=year, month=month, day=day, hour=hour,
                                       minute=minute)
        if delta_time <= 0:
            event_date_utc = event_date - datetime.timedelta(minutes=delta_time)
        else:
            event_date_utc = event_date + datetime.timedelta(minutes=delta_time)

        if current_time > event_date_utc:
            continue  # don't scrape events, closed for betting

        player1 = event.select_one("div.flex-container.flex-item.left-side div.market-line-team.text-right span")
        player1 = (player1.get_text()).strip()
        odds1 = event.select_one("div.market-line-odds.flex-container.middle-side span.market-line-odd.odd-team-one")
        odds1 = float((odds1.get_text()).strip())
        odds2 = event.select_one("div.market-line-odds.flex-container.middle-side span.market-line-odd.odd-team-two")
        odds2 = float((odds2.get_text()).strip())
        player2 = event.select_one("div.flex-item.flex-container.right-side div.market-line-team.text-left span")
        player2 = (player2.get_text()).strip()
        # this one returns a list of classes, and we need 3rd element from that list(which will be name of the game)
        game = event.select_one("div.flex-container.flex-item.left-side div.market-line-sport-icon.hidden-sm-custom span")["class"]
        game = game[2]
        temp_dict = {"game": game, "date": event_date_utc, "player1": player1,
                     "player2": player2, "odds1": odds1, "odds2": odds2}
        parsed_info.append(temp_dict)

        if show:
            print(game)
            print(event_date_utc)
            print("{0}  {1}:{2}  {3}".format(player1, odds1, odds2, player2))
            print("-"*40)

    return parsed_info


def crawl_site(sleeptime=2, show=False):
    link = "https://loot.bet/sport/esports"
    data = []  # returning list
    browser = webdriver.Firefox()
    try:
        browser.get(link)
        time.sleep(sleeptime)
        info = browser.find_element_by_xpath("//*")
        # getting outerHTML code for parsing with BeautifulSoup
        source_code = info.get_attribute("outerHTML").encode('utf-8')
        # parsing 1st page:
        data.append(parse_page(source_code, show=show))
        # here we finding all pages with tournaments info
        pages = browser.find_elements_by_css_selector("div.ng-scope section.tournaments nav li")
        if len(pages) > 1:  # if we have more then 1 page - download and parse next page
            for i in range(1, len(pages)):
                # going to the next page
                pages[i].find_element_by_css_selector("a").click()
                time.sleep(sleeptime)
                info = browser.find_element_by_xpath("//*")
                # getting outerHTML code for parsing with BeautifulSoup
                source_code = info.get_attribute("outerHTML").encode('utf-8')
                # parsing #N page
                data.append(parse_page(source_code, show=show))
    finally:
        browser.quit()

    return data


if __name__ == "__main__":
    show = False
    try:
        command = shlex.quote(sys.argv[1])
        if command.lower() == "show":
            show = True
        if command.lower() == "help":
            print("Keywords:")
            print("show - print scrapped data")
            print("help - print info about available commands")
            sys.exit(0)
    except IndexError:
        pass
    crawl_site(show=show)
