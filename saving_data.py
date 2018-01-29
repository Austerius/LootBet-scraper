import lootbet_scraper
import csv
import os


""" This script will save scraped data from web site "Loot.bet" to .csv file 'file_name'.
    Use your own parameters of 'delimiter' and 'quoting' or delete them for standard output. 
"""
data = lootbet_scraper.crawl_site()
file_name = "esport_events.csv"  # you can use your own filename|location here
# use "a" instead of "w" to append data to existing file if needed
with open(file_name, "w", newline="") as csvfile:
    file_empty = os.stat(file_name).st_size == 0
    field_names = ['game', 'date', 'player1', 'odds1', 'player2', 'odds2']  # dictionary keys
    writer = csv.DictWriter(csvfile, field_names, delimiter=';', quoting=csv.QUOTE_ALL)
    if file_empty:
        writer.writeheader()  # write header only once
    for page in data:
        for game in page:
            writer.writerow(game)
    print("Data saved to {}".format(file_name))