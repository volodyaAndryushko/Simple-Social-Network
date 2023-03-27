from datetime import datetime, date
import json

from src.constants import DATETIME_FORMAT, DATE_FORMAT


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime(DATETIME_FORMAT)
        if isinstance(o, date):
            return o.strftime(DATE_FORMAT)
        return json.JSONEncoder.default(self, o)
