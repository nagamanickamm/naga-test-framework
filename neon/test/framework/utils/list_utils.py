class ListUtils:

    def contains_partial_text(list_item: list, text_to_find: str):
        """Find and return all the items in the list if contains partial text

        Args:
            list_item (_type_): list to look for
            text_to_find (_type_): partial text to find

        Returns:
            list: List of matching items
        """
        return [item for item in list_item if text_to_find in item]

    def is_any_present(in_text: str, list_to_search: list):
        """Find if atleast one of the item in the list is found in the given text

        Args:
            in_text (str): orginal text
            list_to_search (list): list item to find inside the text

        Returns:
            bool: True if any one of item in list found within the string, else False
        """
        return any(y in in_text for y in list_to_search)

    def is_all_present(in_text: str, list_to_search: list):
        """Find if all of the item in the list is found in the given text

        Args:
            in_text (str): orginal text
            list_to_search (list): list item to find inside the text

        Returns:
            bool: True if all item in list found within the string, else False
        """
        return all(y in in_text for y in list_to_search)