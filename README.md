# LootBet-scraper
<p>"<i>lootbet_scraper.py</i>" - Script for scraping e-sport betting information from website https://loot.bet/ (for educational purposes).
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
