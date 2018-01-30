import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import time
import datetime

""" Scrapy spider for scraping bet information on esport events from 'loot.bet' website(for educational purposes)
    This script using Selenium to parse dynamic generated content.  
    Before running spider - install 'scrapy' packets (also Selenium and Firefox browser). 
    On Windows machine you will need to have appropriate C++ SDK (check Twisted documentation) and geckodriver.
    Put this script into 'spiders' folder of your scrapy project and run command(from project directory):
    'scrapy crawl lootbet'
    Returning dictionary:
    { 'game': name of the game,
      'date': date, he the game will be played,
      'player1': first participant's name,
      'odds1': bet rate on first participant,
      'player2': second participant's name,
      'odds2': bet rate on second participant  
    }  
"""


# https://github.com/Austerius
class LootBet(scrapy.Spider):
    name = "lootbet"
    allowed_domains = ['loot.bet']
    start_urls = ['https://loot.bet/sport/esports']

    def __init__(self):
        super().__init__()
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.close()

    def parse(self, response):
        # opening our url ith Firefox driver
        self.driver.get(response.url)
        sleeptime = 3
        time.sleep(sleeptime)
        # here we finding all pages with tournaments info
        pages = self.driver.find_elements_by_css_selector("div.ng-scope section.tournaments nav li")
        i = 1
        while i <= len(pages):  # parsing information from each dynamic page
            time.sleep(sleeptime)
            # getting text version of outer.html
            source = Selector(text=self.driver.page_source)
            date_string = source.css("section.tournaments  span.datetime.flex-container.ng-binding::text").extract()

            player1_string = source.css("section.tournaments div.market-line-team.text-right span::text").extract()
            # for some reason odds1::text return 3 empty strings(separate list object) and one with data for each span block
            odds1_string = source.css("section.tournaments  span.market-line-odd.odd-team-one::text").extract()
            # clearing list 'odds1_string' from empty strings
            temp_list = []
            for odd in odds1_string:
                if odd.strip() == '':
                    continue
                temp_list.append(float(odd.strip()))
            odds1_string = temp_list

            player2_string = source.css("section.tournaments div.market-line-team.text-left span::text").extract()
            odds2_string = source.css("section.tournaments  span.market-line-odd.odd-team-two::text").extract()
            temp_list = []
            for odd in odds2_string:
                if odd.strip() == '':
                    continue
                temp_list.append(float(odd.strip()))
            odds2_string = temp_list
            # extracting name of class which contain name of the game
            game_string = source.css("div.market-line-sport-icon.hidden-sm-custom span").xpath('@class').extract()

            current_time = datetime.datetime.utcnow()
            # getting current site time
            site_time = source.css("span.timezone.ng-binding::text").extract_first()
            site_time = site_time.strip()
            site_time = site_time.split(" ")[2]
            site_hour, site_minutes = site_time.split(":")
            # Getting difference in minutes between current utc time and time, provided by site
            delta_time = (current_time.hour*60 + current_time.minute) - (int(site_hour)*60 + int(site_minutes))

            for game, date, player1, odds1, player2, odds2 in zip(game_string, date_string, player1_string, odds1_string, player2_string, odds2_string):
                # getting right value/name of the game from class-name string
                game = game.split(' ')[2]

                # time conversion
                temp_date = datetime.datetime.strptime(date.strip(), "%b %d, %H:%M")
                month = temp_date.month
                day = temp_date.day
                hour = temp_date.hour
                minute = temp_date.minute
                if (current_time.month == 12) and (month < 12):  # it's ok, since we don't scrape events from the past
                    year = current_time.year + 1
                else:
                    year = current_time.year
                # converting date to UTC time
                event_date = datetime.datetime(year=year, month=month, day=day, hour=hour,
                                               minute=minute)

                event_date_utc = event_date + datetime.timedelta(minutes=delta_time)

                if current_time > event_date_utc:
                    continue  # don't scrape events, closed for betting

                yield {'game': game,
                       'date': event_date_utc,
                       'player1': player1.strip(),
                       'odds1': odds1,
                       'player2': player2.strip(),
                       'odds2': odds2,
                       }

            # next page:
            try:
                pages[i].find_element_by_css_selector("a").click()
                time.sleep(sleeptime)
                i += 1
            except:
                break
