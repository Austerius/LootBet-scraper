# LootBet-scraper
<h3>lootbet_scraper.py</h3>
<p>Script for scraping e-sport betting information from website https://loot.bet/ (for educational purposes).
    (Here You can find some examples of using css selectors and selenium webdriver to obtain information
    from dynamic generated web pages).</p>
   <p> Before running this script, you'll need to <b>install</b> next packets: selenium(with geckodriver if on Windows), 
    bs4 and Firefox web browser.</p>
    <p>After importing this script into your own code - use '<i>crawl_site()</i>' function to start scraping. Obtained 
    information will return as list of lists of dictionaries, where dictionary represent information 
    about single game event, inner list - game events from one site page, outer list - all events.
    Here is example:</p>
    [[{'<i>game</i>': name of the game, '<i>date</i>': date of the event, '<i>player1</i>': name of the first participant,</br>
     '<i>player2</i>': second participant's name, '<i>odds1</i>': bet rates on 1st player, '<i>odds2</i>': bet rates on 2nd player},</br>
     {another game information},</br> 
     ........</br>
     ],</br>
     [{}, {}, {}, ....]</br>
     ........</br>
    ]</br>  
    <p>You can run this script from the <b>command line</b> using parameter '<i>show</i>' to print scraped data into terminal 
    window(also parameter '<i>help</i>' available).</p> 
<h3>saving_data.py</h3>
<p>This script will save scraped data by "<i>lootbet_scraper.py</i>" from web site "<i>Loot.bet</i>" to .csv file '<i>file_name</i>'.
    Use your own parameters of '<i>delimiter</i>' and '<i>quoting</i>' or delete them for standard output.</p> 
<h3>lootbet.py</h3>
<p>Scrapy spider for scraping bet information on esport events from '<i>loot.bet</i>' website(for educational purposes)</p>
    <p>This script using <b>Selenium</b> to parse dynamic generated content.</p>  
    <p>Before running spider - <b>install</b> '<i>scrapy</i>' packets (also <i>Selenium</i> and <i>Firefox browser</i>). 
    On Windows machine you will need to have appropriate C++ SDK (check Twisted documentation) and geckodriver.</p>
    <p>Put this script into '<i>spiders</i>' folder of your scrapy project and run command(from project directory):</br>
    '<i>scrapy crawl lootbet</i>'</p>
    <p>Returning dictionary:</br>
    { '<i>game</i>': name of the game,</br>
      '<i>date</i>': date, he the game will be played,</br>
      '<i>player1</i>': first participant's name,</br>
      '<i>odds1</i>': bet rate on first participant,</br>
      '<i>player2</i>': second participant's name,</br>
      '<i>odds2</i>': bet rate on second participant</br>  
    }</br></p>  
