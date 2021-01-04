# Udf for Validate mails with regular expresion

import re

def get_mail(text):
    try:
        return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text.lower())[0]
    except:
        return ''