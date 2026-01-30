## Project Members: Jacob Sagers, Zola Racklin, and Samara Shaz
## Code Description: The following code below includes a webscraper to scrape rankings from our first rankings 
## website, a crawler to go through its pages, and the unfinished code to crawl our second rankings data.
## AI USE: AI was used to help decipher coding error messages and to determine which line the problem was occuring in.

# import necessary libraries
from bs4 import BeautifulSoup as bs 
import requests 
import pandas as pd
import re

## import the shanghai rankings URLs by subarea ranking
polisci_rank = "https://www.shanghairanking.com/rankings/gras/2024/AS0504"
sosc_rank = "https://www.shanghairanking.com/rankings/gras/2024/AS0505"
econ_rank = "https://www.shanghairanking.com/rankings/gras/2024/AS0501"


def rankings_scraper(shanghai_rank_url, filename):
    '''
    Docstring for rankings_scraper
    
    Inputs:
    shanghai_rank_url: a url that links to the Shanghai University website page to be scraped.
    filname: the desired filename for the csv file represented as a string.

    Output: 
    a csv file containing the list of dictionaries
    '''
    ## maybe add a sleep timer
    header = { "User-Agent" : "Practice Scraper for educational project @jsagers@uchicago.edu" } 
    shanghai_response = requests.get(shanghai_rank_url, headers = header)
    #check the requests code
    print("Our response code is:", shanghai_response.status_code)

    ## turn the response into text and parse it with the bs library
    soup = bs(shanghai_response.text, "html.parser")
    print(soup.prettify())

    ##create a list to store dictionaries
    univ_lst = []
    rows = soup.find_all("tr")

    #within the rows for the larger frame, find the nam and ranking.
    for row in rows:
        number = row.find("div", {"class": "ranking"})
        name = row.find("span", {"class": "univ-name"})

        #check to make sure the row is not empty, then strip
        if number and name:
            rank = number.get_text(strip=True)
            univ = name.get_text(strip=True)

            #append each unique dictionary to the overall list using name and ranking as the key value pair with titles for the csv
            univ_lst.append({"University": univ, "Ranking": rank})

    #change into a dataframe
    df = pd.DataFrame(univ_lst)
    print(df)
    #export to csv
    df.to_csv(filename, index=False)

    return univ_lst

rankings_scraper(polisci_rank, "poli_sci_rankings.csv")
rankings_scraper(sosc_rank, "sosc_rankings.csv")
rankings_scraper(econ_rank, "econ_rankings.csv")


def rankings_crawler(starting_url, limiting_url):
    '''
    A function to crawl the Shanghai Rankings' multiple pages.
    
    Input:
    starting_url:
    limiting_url:

    Outputs: 
    a list of url links to crawl
    '''




# set up user-agent for wikipedia
header = { "User-Agent" : "demo wiki crawler for teaching UChicago youremail@uchicago.edu" } 

# list of urls for the crawler to visit, start with one to keep things simple
urls_to_visit = ['https://cy.wikisource.org/wiki/Hafan']

# to store the URLs and their page text if in Welsh
results = []          

# to track URLs already visited to avoid revisiting, in PA1 you must use a "queue" for efficiency
already_visited = []   

# counter to keep track of how many URLs have been already visited
i = 1 

# loop as long as there are URLs in urls_to_visit and counter is under 10
# this limits the crawler to processing at most 10 urls (try to test this code with different integers)
while urls_to_visit and i < 10:
    
    # take the first url 
    u = urls_to_visit.pop(0)
    print(f"Processing: {i}, URL: {u}")
    
    # skip if url has been already processed
    if u in already_visited:
        continue
        
    # mark this url as processed and update counter to keep track
    already_visited.append(u)  
    i += 1

    # send request to the url, check if it is a valid url, skip if not
    try:
        r = requests.get(u, headers=header, timeout=5)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error with URL {u}: {e}")
        continue

    # parse the url page and extract the text
    soup = bs(r.text, "html.parser")
    page_text = soup.get_text()

    # check if the page is in Welsh with util function, if so store the url and its text in results
    if welsh(u, page_text):
        print("This page is in Welsh!")
        results.append([u, page_text]) 
        
        # and extract more urls from the Welsh page 
        links = soup.find_all('a', href = True) 
        for link in links:
            link_url = link.get('href')
            
            # ensure that only new links are added to the queue of urls to visit
            if link_url not in already_visited and link_url not in urls_to_visit:
                urls_to_visit.append(link_url)

print(f"\nTotal unique URLs processed: {len(already_visited)}")
print(f"Total pages written in Welsh we stored: {len(results)}")
print(f"Total remaining URLs in queue to process: {len(urls_to_visit)}")