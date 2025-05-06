"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Györgyi Fucseková Posztósová
email: posztosgyorgyi@seznam.cz
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys


def check_arguments():
    """Validates the number of command-line arguments."""
    if len(sys.argv) != 3:
        print("Please enter 2 arguments!")
        print("python main.py <url_region> <file_name.csv>")
        sys.exit(1)
    input_url = sys.argv[1]
    output_file = sys.argv[2]
    return input_url, output_file

def check_input_url(input_url, base_url):
    """Checks if the provided URL is part of the election results website.

    Args:
        input_url (str): url of selected municipality to scrape
        base_url (str): url of election results for all municipalities
    """
    if not base_url in input_url:
        print("Invalid region url. Please check.")
        sys.exit(1)
    print("The entered url was checked.")

def check_input_file_name (output_file):
    """Checks if the output file name has the right file name extension."""
    if not output_file.lower().endswith(".csv"):
        print("Invalid file name. The file must be a csv file.")
        sys.exit(1)
    print("The output file was checked.")

def check_inputs (base_url):
    """A wrapper function to call all the input validation functions."""
    input_url, output_file = check_arguments()
    check_input_url(input_url, base_url) 
    check_input_file_name(output_file)
    return input_url, output_file

def response_from_server (url):
    """Checkes if the server is available for scraping and if yes, parses url using Beautiful soup."""
    response = requests.get(url)
    if response.status_code != 200:
        print("The server is not responding.")
        sys.exit(1)
    return BeautifulSoup(response.text, "html.parser")

def get_town_links (soup, base_url):
    """Extracts the links to all individual town result page for scraping."""
    town_links = []
    tables = soup.find_all("table")
    for table in tables:
        links = table.find_all("a", href = True)
        town_links.extend(links)
    all_hrefs = [link["href"] for link in town_links]
    hrefs_311 = [href for href in all_hrefs if "ps311" in href]
    hrefs_311 = list(set(hrefs_311)) #remove duplicates
    full_town_links = [base_url + href for href in hrefs_311]
    return full_town_links
   
def scraping_municipality_url(input_url, base_url):
    """Scrapes the initial municipality list page."""
    soup: BeautifulSoup = response_from_server(input_url)
    print("Scraping of municipality url started.")
    full_town_links = get_town_links (soup, base_url)
    print(f"There is {len(full_town_links)} towns to extract.")
    return full_town_links

def extract_town_data(full_town_links):
    all_town_data = []
    for link in full_town_links:
        town_soup: BeautifulSoup = response_from_server(link)
        
        code = link.replace("https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=", "")
        town_code = code[:6]
        
        name = town_soup.find_all("h3")
        town_name = name[2].text.replace("Obec: ", "").strip()
        
        voters = town_soup.find("td", class_ = "cislo", headers = "sa2").text
        
        envelopes = town_soup.find("td", class_ = "cislo", headers = "sa3").text
        
        votes = town_soup.find("td", class_ = "cislo", headers = "sa6").text
        
        list_of_party_names = []
        party_names = town_soup.find_all("td", class_ = "overflow_name")
        for party in party_names:
            list_of_party_names.append(party.text)
        
        votes_for_parties = []
        valid_votes = town_soup.find_all("td", class_ = "cislo", headers = ["t1sa2 t1sb3", "t2sa2 t2sb3"])
        for vote in valid_votes:
            votes_for_parties.append(vote.text)
        
        party_data = dict(zip(list_of_party_names, votes_for_parties))



        town_data = {
        "Kód obce" : town_code,
        "Jméno obce" : town_name,
        "Voliči v seznamu" : voters,
        "Vydané obálky" : envelopes,
        "Platné hlasy" : votes,
        "Strany" : party_data
        }  

        all_town_data.append(town_data)
    return all_town_data

def prepare_header(all_town_data):
    """Determine fieldnames as combination of base fieldnames and unique party names, which will be used as column headers.."""
    base_fieldnames = [key for key in all_town_data[0].keys() if key != "Strany"]
    
    all_party_names = set()
    for town_data_item in all_town_data:
        if "Strany" in town_data_item and isinstance(town_data_item["Strany"], dict):
            all_party_names.update(town_data_item["Strany"].keys())

    sorted_party_names = sorted(list(all_party_names))
    full_fieldnames = base_fieldnames + sorted_party_names

    return full_fieldnames, base_fieldnames, sorted_party_names

def prepare_data_to_write(all_town_data, base_fieldnames, sorted_party_names):  
    """Prepare data for writing: transform each town's data into a flat dictionary."""
    rows_to_write = []
    for town_data_item in all_town_data:
        row = {}
        for field in base_fieldnames:
            row[field] = town_data_item.get(field, "")
        
        party_votes = town_data_item.get("Strany", {})
        for party_name in sorted_party_names:
            row[party_name] = party_votes.get(party_name, "0")
        rows_to_write.append(row)
    return rows_to_write

def write_to_csv(output_file, all_town_data):
    """Writes the extracted data to a CSV file, with political parties as separate columns."""
    if not all_town_data:
        print("No data to write. CSV file will not be created.")
        sys.exit(1)

    full_fieldnames, base_fieldnames, sorted_party_names = prepare_header(all_town_data)
    rows_to_write = prepare_data_to_write (all_town_data, base_fieldnames, sorted_party_names)

    with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter = ";",fieldnames = full_fieldnames)
        writer.writeheader()
        writer.writerows(rows_to_write)
        print("The url scraping is done. File was created.")
  
def main(base_url):
    input_url, output_file = check_inputs (base_url)
    full_town_links = scraping_municipality_url(input_url, base_url)
    all_town_data = extract_town_data(full_town_links)
    write_to_csv(output_file, all_town_data)


if __name__ == "__main__":
    main("https://www.volby.cz/pls/ps2017nss/")