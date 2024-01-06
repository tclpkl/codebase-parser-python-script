class SearchResultRow:
    """
    Class to store a singular row of a saerch result
    Stores the following fields of information:
        1. Component Name
        2. Component Owner
        3. File Path
        4. File Name
        5. Codebase link to file
        6. Codebase link to details about file ownership
    """

    def __init__(self, component_name, component_owner, file_path, file_name, file_link, file_ownership_link):
        if component_name == "":
            component_name = "N/A"
        if component_owner == "":
            component_owner = "N/A"
        self.__component_name = component_name
        self.__component_owner = component_owner
        self.__file_path = file_path
        self.__file_name = file_name
        self.__file_link = "Codebase Link" + file_link
        self.__file_ownership_link = file_ownership_link

    def __str__(self):
        """Easy to read string representation printed to terminal"""
        s = ""
        s += "\tComponent Name: " + self.__component_name + "\n"
        s += "\tComponent Owner: " + self.__component_owner + "\n"
        s += "\tFile Path: " + self.__file_path + "\n"
        s += "\tFile Name: " + self.__file_name + "\n"
        s += "\tFile Link: " + self.__file_link + "\n"
        s += "\tFile Ownership: " + self.__file_ownership_link + "\n"
        return s

    def get_comma_separated_for_csv(self):
        """Returns string with all fields of information separated by commas and no space. Used to write to csv and pasting into Excel"""
        s = ""
        s += self.__component_name + ","
        s += self.__component_owner + ","
        s += self.__file_path + ","
        s += self.__file_name + ","
        s += self.__file_link + ","
        s += self.__file_ownership_link + ","
        return s

    def get_component_name(self):
        return self.__component_name

    def get_component_owner(self):
        return self.__component_owner

    def get_file_name(self):
        return self.__file_name

    def get_file_path(self):
        return self.__file_path

    def get_file_link(self):
        return self.__file_link

    def get_file_ownership(self):
        return self.__file_ownership_link
