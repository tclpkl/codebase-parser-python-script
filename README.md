# Codebase Parser
Developed by Timothy Lin

## CodeBase Parser Script
This repository contains a Python script that automates searching on a private codebase website and parsing the search results using Selenium and BeautifulSoup. The script was motivated by a need to parse through large numbers of results when searching for various cryptographic algorithms in the codebase; however, it can be efficient for general use as well. 

There are two ways to use the script. The first is as a CLI tool (and is restricted to one search & all file types & selected cluster), and the other is by modifying the "FOR_USE_advanced_codebase_tool.py" file (and supports multiple searches & select file types & selected cluster). For both, the search results are parsed and stored in a CSV file under the folder "/search_results_CSV". Please read the Usage section for more details!

## Setup
Installing Python3 and Google Chrome is required to run this script. A user then needs to setup the environment for the folder and install the relevant packages.

In the root directory of this repository, run the following:

```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage
**Method 1: Command-line Interface** <br />
The first method is convenient to use on the command line, but only allows one search at a time and searches all file types. The user is able to choose the cluster to search.
```bash
source env/bin/activate # must be run every time you start up a new shell window
python3 -m codebase_tool --search_phrase search_phrase --basic/--all-chars --invisible/--visible --cluster
```
* `-s` or `--search_phrase`: The search phrase to use for the search. To include spaces, please wrap the phrase in quotation marks.
* `-b/-a` or `--basic/--all-chars`: A toggle to either perform a basic search or an all characters search.
* `-i/-v` or `--invisible/--visible`: A toggle to run script in the background or have a pop-up browser showing script actions.
* `-c` or `--cluster`: The cluster we want to search. Must be exact string of cluster name as on codebase website, and should be enclosed in quotations if name contains whitespace.

The output will be stored in a CSV file under the folder "/search_results_CSV". For more help when using the CLI version of the tool, please run `python3 -m codesearch_tool --help' for clarification!

**Method 2: Using the "FOR_USE_advanced_codebase_tool.py" File** <br />
The second method allows searching multiple phrases at once, and also allows restricting results to specific file types. The user is able to choose the cluster to search. In "FOR_USE_advanced_codebase_tool.py", modify the following variables to use the script:
* search_phrases: The list of search phrases to search on the codebase website.
* basic_search: Whether the user would like to perform a basic search or an all characters search.
* files_to_search: The set of file types we want to search through on the codebase.
    * These filetypes must be the exact strings as found on the codebase.
* cluster: The cluster we want to search on the codebase.
    * The cluster name must be the exact string as found on the codebase.
* run_in_background: Whether the user would like the script to run in the background or have a visible browser interface.
    * Runs in background when set to True
    * Visible browser pops up when set to False
In the root directory of this repository, run the following:
```bash
source env/bin/activate # must be run every time you start up a new shell window
python3 -m FOR_USE_advanced_codebase_tool
```
The output will be stored in a CSV file under the folder "/search_results_CSV". For more details, the commenting in the file "FOR_USE_advanced_codebase_tool" provides the specifics on how to modify the variables in the file.

**Notes*
* Under regular network conditions, the script takes approximately 3:30 to 4:00 minutes to parse through 100 search results. Whenever the script finishes parsing a phrase, it will export the results into a CSV file under the folder "/search_results_CSV" with the filename "searchphrase_codebase_results.csv". 
* The terminal will indicate the progress of the script. There will be print statements indicating how many results have been parsed and when a search phrase is finished being parsed.

## Output
The folder "/search_results_CSV" will contain the outputted CSV files for all searches. The CSV files are formatted to contain the following information about each search result in a comma-separated manner:
- Component Name, Component Owner, Full File Path, File Name, File Link, Ownership Link

## Implementation Notes
The script uses [Selenium](https://selenium-python.readthedocs.io/index.html) to open a Chrome driver for the duration of the script. The chome driver is then used to navigate to the codebase page and all subsequent pages visited. As we go through the pages of the search results, [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is used to parse through the HTML code of the pages to find the relevant information we need about each result.

## Code Review
Please feel free to leave any comments/concerns!
