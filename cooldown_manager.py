from datetime import datetime, timedelta
import json


class CooldownManager:
    def __init__(self):
        self.no_cd = None

    def check(self, email):
        """Searches for provided email in local database to see if account has likes to spend"""
        try:
            with open('cooldown.json', mode='r') as cd_file:
                try:
                    data = json.load(cd_file)
                    data = data[email]['date'].split('.')[0]
                    formatted_date = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                    self.no_cd = formatted_date + timedelta(hours=12)
                    if self.no_cd < datetime.now():
                        return True
                    else:
                        return False
                except AttributeError:
                    return False

        except FileNotFoundError:
            return False
