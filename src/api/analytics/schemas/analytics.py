from marshmallow import fields, Schema

from src.constants import DATE_FORMAT


class AnalyticsSchema(Schema):
    date_from = fields.Date(format=DATE_FORMAT, allow_none=True)
    date_to = fields.Date(format=DATE_FORMAT, allow_none=True)


analytics_schema = AnalyticsSchema()
