import re


class RegEx:

    def is_date(text, format="%Y-%m-%d"):
        '''Returns match if text is date or false if not found'''

        match = False
        
        match(format):
            case "%Y-%m-%dT%H:%M:%S.%f":
                match = re.match(r'^\d{4}(\-\d{2}){2}[Tt]\d{2}(:\d{2}){2}\.\d+[a-z]?$', text)
            case "%Y-%m-%dT%H:%M:%S+":
                match = re.match(r'^\d{4}(\-\d{2}){2}[Tt]\d{2}(:\d{2}){2}([0-9a-z.]+)?$', text)
            case "%Y-%m-%d":
                match = re.match(r'^\d{4}(\-\d{2}){2}', text)
            case _:
                match = re.match(r'^\d{4}(\-\d{2}){2}.*', text)
        return match

    def is_float(text):
        '''Returns match if text is float or false if not found'''
        match = re.match(r'[0-9]+\.[0-9]+$', text)
        return match

    def is_number(text):
        '''Returns match if text is number or false if not found'''
        match = re.match(r'^[0-9]+$', text)
        return match

    def is_alphanumeric(text):
        """Returns match if text is alpha numeric or false if not found

        Args:
            text (str): some string to verify

        Returns:
            _type_: returns match
        """
        '''Returns match if text is alpha numeric or false if not found'''
        match = re.match(r'^[a-zA-Z0-9]+$', text)
        return match

    def get_number_from_text(text):
        """Get Number from given text

        Args:
            text (str): ex: "My age is 20" returns 20
        """
        return re.match(r'\d+', text)
