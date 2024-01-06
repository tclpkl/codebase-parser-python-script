from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from helper_classes import search_result_row
from selenium.webdriver.chrome.options import Options
import os
import getpass

class CodebaseParser:
    """Class storing various helper function for parsing Codebase"""

    file_options_reactID_map = {}
    """
    A hashmap where each key, value pair is a file type mapped to its id tag on Codebase, used for selecting/deselecting file types to search. The keys are the exact strings of the file type options on Codebase (eg. "C/C++").
    """
    cluster_options_reactID_map = {}
    """
    A hashmap where each key, value pair is a cluster name mapped to its id tag on Codebase, used for choosing a cluster to search. The keys are the exact strings of the cluster names on Codebase (eg. "C/C++").
    """

    @staticmethod
    def perform_search(search_term, files_to_search, run_in_background, basic_search, cluster):
        """"
        User-friendly, easy function call to perform all the necessary actions for a search using other helper functions in this class.

        :param search_term: The search term the user wants to search.
        :param files_to_search: A set of file types to restrict the search results to. Must be exact strings of the file types on Codebase.
        :param run_in_background: A boolean determining whether to run the script in the background or with a visible browser interface.
        :param basic_search: A boolean determining whether to perform a basic search or an all characters search
        :param cluster: A string indicating which cluster to search from on Codebase. Must be exact string on Codebase.
        :return: Returns nothing. Results from a search are outputted into a .csv file in /search_results_CSV directory.
        """

        # Creating driver to run in background
        driver = CodebaseParser._get_driver(run_in_background)
        # SSO
        CodebaseParser._loginSSO(driver)
        # Perform the search
        CodebaseParser._query(driver, search_term, files_to_search, basic_search, cluster)
        # Parse search results
        search_results = CodebaseParser._parse_search_results(driver)
        for search_result in search_results:
            print(search_result)
        # Exporting to txt file
        CodebaseParser._export_to_csv(search_term, files_to_search, search_results, cluster)

    @staticmethod
    def _get_driver(run_in_background):
        """"
        Get a Chrome driver that has authenticated Single-sign On if required.

        :param run_in_background: Boolean determining whether to run in the background or have a visible browser pop up during execution.
        :return: Returns a Chrome driver that has already bypassed Single-sign On.
        """
        chrome_options = Options()
        if run_in_background:
            chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
        # Waits 5 seconds on a page before giving up finding element
        driver.implicitly_wait(5)

        CodebaseParser._loginSSO(driver)

        return driver

    @staticmethod
    def _loginSSO(driver):
        """"
        Authenticate Single-sign On if necessary

        :param driver: The driver we want to perform Single-sign On.
        :param username: User-inputted username, only needed if SSO is required.
        :param password: User-inputted password, only needed if SSO is required.
        :return: Returns nothing. Passed-in driver will have passed Single-sign On.
        """

        # Codebase page to trigger SSO
        Codebase_page = "Codebase"
        # Acccessing login
        driver.get(Codebase_page)
        # Asserting right page
        if "Codebase in driver.title:
            # Filling in username and password field with user-inputted username and password
            print("Accessing Codebase from a device/network requiring Single-sign On. Please enter your username and password.")
            driver.find_element(By.NAME, "pf.username").send_keys(input("Enter your username: "))
            driver.find_element(By.NAME, "pf.pass").send_keys(getpass.getpass("Password: "))
            # Submitting
            driver.find_element(By.NAME, "pf.ok").submit()

            if "Codebase" not in driver.title:
                # Error with Single-sign on
                print("There was an error with Single-sign On. Likely incorrect username/password, or multi-factor authentication is needed, which this script does not yet support.")
                exit()


    @staticmethod
    def _query(driver, search_term, file_types, basic_search, cluster):
        """"
        Sets the attributes of the search query. Selects the specific file types, enters search phrase into search bar, presses search button.

        :param driver: The driver we are performing the query on.
        :param search_term: Search term to input into search bar.
        :param file_types: File types we want to search through.
        :param basic_search: Boolean indicating to select basic search or all characters search.
        :param cluster: A string indicating which cluster to search from on Codebase. Must be exact string on Codebase.
        :return: Returns nothing. Inputs the fields into the search and presses search button on Codebase on driver.
        """
        # Open menu for selecting file types
        driver.find_element(By.ID, "soTrigger").click()
        driver.find_element(By.ID, "so-ftg-selector").click()
        # Clearing selection
        driver.find_element(By.ID, CodebaseParser.file_options_reactID_map["Select none"]).click()
        # Selecting all file types we want to search
        for file in file_types:
            # Checking vaild file type
            if file not in CodebaseParser.file_options_reactID_map:
                print("Invalid file type")
                exit()
            driver.find_element(By.ID, CodebaseParser.file_options_reactID_map[file]).click()
        # Inputting search term into search bar
        driver.find_element(By.ID, "search-text").send_keys(search_term)

        # Toggling all characters search depending on parameter
        if not basic_search:
            driver.find_element(By.ID, "All-Characters").click()

        # Checking valid cluster
        if cluster not in CodebaseParser.cluster_options_reactID_map:
            print("Invalid cluster. Exiting.")
            exit()
        # Selecting cluster to search
        driver.find_element(By.ID, "cluster-selector").click()
        driver.find_element(By.ID, CodebaseParser.cluster_options_reactID_map[cluster]).click()

        # Pressing search button
        driver.find_element(By.ID, "searchBtn").submit()


    @staticmethod
    def _parse_search_results(driver):
        """"
        Parses through all search results, storing each result as an object of the SearchResultRow class.

        :param driver: A driver to a Codebase results page.
        :return: A list of SearchResultRow objects
        """

        # Finding number of results and checking it is less than 10k
        num_results = driver.find_element(By.ID, "results-header").find_element(By.CLASS_NAME,
                                                                               "table-header-ht.summary").text
        num_results = int("".join([c for c in num_results if c.isdigit()]))
        if num_results > 10000:
            print("Over 10,000 results. Please refine your search for less results1")
            exit()

        # Storing all search results
        search_results = []
        # Changing to 500 results per row
        select = Select(
            driver.find_element(By.CLASS_NAME, "select-wrap.-pageSizeOptions").find_element(By.TAG_NAME, "select"))
        select.select_by_visible_text("500 rows")
        # Finding number of total pages
        num_pages = int(driver.find_element(By.CLASS_NAME, "-totalPages").text)
        # Iterating through each page
        for curr_page in range(1, num_pages + 1):
            res = CodebaseParser._parse_page(driver, (curr_page, num_pages))
            search_results.extend(res)
            print("----Finished page " + str(curr_page) + "----\n")
            # Go to next page
            try:
                driver.find_element(By.CLASS_NAME, "-next").find_element(By.TAG_NAME, "button").click()
            except:
                break

        return search_results

    @staticmethod
    def _parse_page(driver, page_num):
        """"
        Parses through ONE page of search results, storing each result as an object of the SearchResultRow class.

        :param driver: Driver ona Codebase page of search results
        :param page_num: A tuple with the current page and the total number of pages (eg. (1, 3) indicates page 1 out of 3).
        :return: A list of SearchResultRow objects from the current Codebase page.
        """

        # Getting HTML of page
        table_html = driver.find_element(By.CLASS_NAME, "rt-tbody").get_attribute("innerHTML")
        soup = BeautifulSoup(table_html, "html.parser")
        # Storing search results of page
        page_results = []
        # Parsing each row
        search_results_rows = soup.find_all("div", class_="rt-tr-group")
        # Keeping track of number of rows parsed
        num_rows_parsed = 0
        for row_raw_data in search_results_rows:
            # Incrementing number of rows parsed
            num_rows_parsed += 1
            # Parsing for component name, component owner, full file path, file name, file link, ownership link
            row_result = CodebaseParser._parse_row_raw_data(driver, row_raw_data)
            if not row_result:
                break
            component_name, component_owner, file_path, file_name, file_link, file_ownership_link = row_result
            # Append to pageResults
            single_row_result = search_result_row.SearchResultRow(component_name, component_owner, file_path, file_name, file_link, file_ownership_link)
            page_results.append(single_row_result)
            # Printing every 10 results parsed
            if num_rows_parsed % 10 == 0:
                print("\tFinished parsing " + str(num_rows_parsed) + " rows in page " + str(page_num[0]) + " out of " + str(
                    page_num[1]))
        # Indicating last few rows were parsed in last page
        if page_num[0] == page_num[1] and num_rows_parsed % 10 != 0:
            print("\tFinished parsing " + str(num_rows_parsed) + " rows in page " + str(page_num[0]) + " out of " + str(
                page_num[1]))


        return page_results

    @staticmethod
    def _parse_row_raw_data(driver, row_raw_data):
        """"
        For a search result row, parse its raw HTML for relevant information, follow the ownership link to get component name and component owner.

        :param driver: The driver with the original Codebase results. This function will create a new tab, access the ownership link on this new tab to parse for relevant information, then close the tab and return to the original results page.
        :param row_raw_data: The raw HTML of a search result row to parse information from.
        :return: Returns the relevant fields of information from a search result - Component Name, Component Owner, File Path, File Name, File Link, File Ownership Link
        """

        cells = row_raw_data.find_all("div", class_="rt-td")
        try:
            # Path to file
            file_path = cells[1].get_text().strip()
            # Filename
            file_name = cells[2].get_text().strip()
            # Links to filepath and ownership
            links = row_raw_data.find_all("a")
            file_link = links[0].get("href")
            file_ownership_link = links[2].get("href")
        except:
            return None

        # Creating a new tab on driver to parse through file ownership link and changing wait time 
        original_tab = driver.window_handles[0]
        driver.switch_to.new_window("tab")
        driver.implicitly_wait(0)
        # Parsing link to fileOwnership for componentName and componentOwner
        driver.get(file_ownership_link)
        assert "Files And Directories List" in driver.title
        component_name, component_owner = "", ""
        if len(driver.find_elements(By.CSS_SELECTOR, "td.component")) > 0:
            component_name = driver.find_element(By.CSS_SELECTOR, "td.component").text
        if len(driver.find_elements(By.CSS_SELECTOR, "td.topContributor")) > 0:
            component_owner = driver.find_element(By.CSS_SELECTOR, "td.topContributor").find_element(
                By.TAG_NAME, "a").text
        # Returning to original tab after finishing parsing ownership link
        driver.close()
        driver.switch_to.window(original_tab)
        driver.implicitly_wait(10)

        return [component_name, component_owner, file_path, file_name, file_link, file_ownership_link]

    @staticmethod
    def _export_to_csv(search_term, files_to_search, search_results, cluster):
        """"
        A helper function to export all search results into a CSV file in the /search_results_CSV directory. Filename is "SEARCHPHRASE__Codebase_results.csv" where "SEARCHPHRASE" is the search phrase with all spaces/dashes replaced by underscores.

        :param search_term: The search term that was used for current search.
        :param files_to_search: File types that were searched through
        :param serach_results: The list of SearchResultRow objects to output into the CSV file.
        :param cluster: A string indicating which cluster to search from on Codebase. Must be exact string on Codebase.
        :return: Returns nothing. Outputs CSV file into /search_results_CSV directory.
        """

        # Editing search term to be valid file name
        search_term_to_filename = ""
        for c in search_term:
            if c.isalnum():
                search_term_to_filename += c
        # Directory of CSVs
        csv_directory = "search_results_CSV"
        # Putting results into text file
        output_file_name = os.path.join(csv_directory, search_term_to_filename + "_Codebase_results.csv")
        output = open(output_file_name, "w")
        # Outputting search term used and files types searched through in CSV file
        output.write("Search Term: " + search_term + "\n")
        output.write("Files searched:")
        for fileType in files_to_search:
            output.write(" " + fileType)
        output.write("\n")
        # Outputting cluster searched
        output.write("Cluster searched: " + cluster)
        # Outputting information parsed from each search result
        output.write("Component Name, Component Owner, Full File Path, File Name, File Link, Ownership Link\n\n")
        for search_result in search_results:
            output.write(search_result.get_comma_separated_for_csv())
            output.write(search_term)
            output.write("\n")
