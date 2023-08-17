import re
from datetime import datetime

class Utils:

    @staticmethod
    def get_current_month_year():
        now = datetime.now()
        return now.strftime('%m/%Y')

    @staticmethod
    def extract_date_from_string(text):
        # Usamos uma expressão regular para encontrar a data no formato mm/aaaa dentro da string
        match = re.search(r'(\d{2})/(\d{4})', text)
        if match:
            month, year = match.groups()
            return {'ano': int(year), 'mes': int(month)}
        else:
            return None
