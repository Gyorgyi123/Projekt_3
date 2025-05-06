## Description

This Python script is designed to scrape election results from the Czech Statistical Office's election website (`volby.cz`), specifically for parliamentary elections in 2017.

Given a URL for a specific territorial unit (e.g., a region or a district), the script will:
1.  Identify all municipalities within that unit.
2.  For each municipality, navigate to its detailed results page.
3.  Extract key election data:
    *   Municipality Code (Kód obce)
    *   Municipality Name (Jméno obce)
    *   Registered Voters (Voliči v seznamu)
    *   Issued Envelopes (Vydané obálky)
    *   Valid Votes (Platné hlasy)
    *   Votes for each political party.
4.  Compile all this data and save it into a single CSV file, with each political party's votes presented in separate columns.

## Requirements

To run this script, you'll need **Python 3** (specifically, Python 3.6 or newer is recommended for `venv` and f-string support, though the core logic might work on slightly older Python 3 versions). This project was written in Python version according `.python-version` file.

It's highly recommended to use a virtual environment to manage project-specific dependencies.

1.  **Navigate to your project directory:**
    Open your terminal or command prompt and go to the directory where `main.py` is located:

2.  **Create the virtual environment:**
    If you have Python 3, you can use the built-in `venv` module. Run the following command (you can replace `venv` with your preferred environment name, like `.env` or `myenv`):
    ```bash
    python -m venv venv
    ```
    This will create a new folder named `venv` (or your chosen name) in your project directory.

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
    Your terminal prompt should change to indicate that the virtual environment is active (e.g., it might show `(venv)` at the beginning of the prompt).


2.  **Install the dependencies:**
      It's recommended to manage the project's dependencies using a `requirements.txt` file.
    
    After setting up and activating your virtual environment (see section below), you can install all required packages by running:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Deactivating the virtual environment:**
    When you're done working on the project, you can deactivate the environment by simply typing:
    ```bash
    deactivate
    ```
    You'll need to reactivate it (step 3) whenever you want to work on this project again.

## How to Run

The script is executed from the command line and requires two arguments:

1.  **URL:** The URL of the election results page for the territorial unit you want to scrape. This should be a link from `https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ` that lists municipalities.
2.  **Output File Name:** The name for the CSV file where the results will be saved (e.g., `vysledky_okresu_brno.csv`).

**Command Syntax:**

```bash
python main.py <url_region> <file_name.csv>
```

**Example:**

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206" "vysledky_jihomoravsky_kraj_okres_vyskov.csv"
```

## Output CSV Structure

The generated CSV file will have the following columns:

*   `Kód obce`
*   `Jméno obce`
*   `Voliči v seznamu`
*   `Vydané obálky`
*   `Platné hlasy`
*   And then, one column for each political party found across all scraped municipalities, containing the number of votes that party received in the respective municipality. If a party did not receive votes or was not listed in a particular municipality, its vote count will be "0".

The CSV file will use a semicolon (`;`) as a delimiter and will be encoded in `utf-8-sig` for better compatibility, especially with Microsoft Excel.

## Sample CSV Output

Here's a brief example of what the `output_file.csv` might contain:

```csv
Kód obce;Jméno obce;Voliči v seznamu;Vydané obálky;Platné hlasy;ANO 2011;Česká pirátská strana;Demokratický blok;Komunistická str.Čech a Moravy;Občanská demokratická strana;Svoboda a př.dem.-T.Okamura
583387;Adamov;3907;2490;2463;700;360;0;250;300;280
583395;Bedřichov;245;199;199;40;35;0;15;25;30
583409;Bílovice nad Svitavou;3086;2338;2323;500;550;0;100;350;250
583417;Blansko;16678;10785;10677;3000;1500;0;1200;1800;1000
583425;Březina (dříve okres Blansko);870;660;655;180;100;0;50;90;70
```


## Script Logic Overview

1.  **Input Validation:** Checks if the correct number of arguments are provided, if the URL seems valid, and if the output filename ends with `.csv`.
2.  **Fetch Initial Page:** Downloads the HTML for the provided regional/district URL.
3.  **Extract Municipality Links:** Parses the initial page to find links to the detailed results pages for all individual municipalities listed.
4.  **Scrape Each Municipality:** For each municipality link:
    *   Downloads and parses its specific results page.
    *   Extracts the general election statistics (voters, envelopes, valid votes).
    *   Extracts the names of all political parties and their corresponding vote counts.
5.  **Prepare Data for CSV:**
    *   Determines a complete list of all unique political parties to serve as column headers.
    *   Transforms the scraped data for each town into a flat structure, ensuring each party has a column.
6.  **Write to CSV:** Writes the headers and all the processed data rows to the specified output CSV file.

## Project Structure

The project is organized as follows:

```
Projekt_3/
├── .python-version       # Specifies the Python version for the project (optional, used by tools like pyenv)
├── main.py               # The main Python script for scraping election data
├── README.md             # This file, providing information about the project
├── requirements.txt      # Lists the Python dependencies for the project
├── venv/                 # Virtual environment directory (if created, typically excluded from version control)
└── *.csv                 # Output CSV files generated by the script (e.g., vysledky_okresu_vyskov.csv)
```

## Author:
 Györgyi Fucseková Posztósová

