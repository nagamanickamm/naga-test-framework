import configparser
import csv
import os
from pathlib import Path
import shutil


class FileUtils:

    def remove_directory_tree(path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def search_config_file(file_location, section, key):
        """Read config file from specific file location and search for section and key"""
        config = FileUtils.get_config(file_location)
        return config.get(section, key)

    def get_config(file_location):
        """Read config file from specific file location"""
        config = configparser.ConfigParser()
        config.read(file_location)
        return config

    def read_file(file_name):
        """Read file from given path(file_name) and return content as string"""
        fd = open(file_name, encoding='utf-8-sig')
        file = fd.read()
        fd.close()
        return file

    def get_path_current_file(root, file=__file__):
        """Get Current path file relative to the given file

        Args:
            root (_type_): root
            file (_type_, optional): current file object should be __file__. Defaults to __file__.

        Returns:
            str: path
        """
        return str(Path(os.path.dirname(file)).absolute()).split(root)[0]

    def get_scenario_in_csv(key, txt_to_find, file_path):
        """
        return row in a csv file for the identified text 
        
        Args:
            key (str): column name/header to search
            txt_to_find (str): text to search within column
            file_path (str): path to csv file

        Returns:
            dictionary: row of searched column/ searched result
        """
        file = open(file_path, encoding='utf-8-sig', newline='')
        csv_file = csv.DictReader(file)
        found_dict = {}
        for each_row in csv_file:
            if each_row[key] == txt_to_find:
                found_dict = each_row
                del found_dict[key]
                break
        return found_dict