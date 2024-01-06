from helper_classes import codebase_parser

def main():
    """
    This is the main function we call to use the script. Outputs CSV files stored in /search_results_CSV.
    Modify the following variables to use the script:
        1.search_phrases: The list of search phrases to search on the codebase.
        2. basic_search: Whether the user would like to perform a basic search or an all characters search.
        3. files_to_search: The set of file types we want to search through on the codebase.
            a. These filetypes must be the exact strings as found on the codebase
        4. cluster: The cluster we want to search on the codebase.
            a. The cluster name must be the exact string as found on the codebase.
        5. run_in_background: Whether the user would like the script to run in the background or have a visible browser interface.
            a. Runs in background when set to True
            b. Visible browser pops up when set to False
     """

    # TO MODIFY
    # ------------------------------------------------------------------------
    search_phrases = [
        "example1",
        "example2"
    ]
    basic_search  = False
    files_to_search = {"Go", "C", "C#", "C++", "C/C++ Header", "Java", "JavaScript"}
    cluster = "Cluster1"
    run_in_background = True
    # ------------------------------------------------------------------------

    # Searches through all inputted search phrases
    for phrase in search_phrases:
        codebase_parser.CodebaseParser.perform_search(phrase, files_to_search, run_in_background, basic_search, cluster)
        print("\nFINISHED PARSING", phrase, "\n")

if __name__ == "__main__":
    main()




