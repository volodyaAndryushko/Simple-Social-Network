from marshmallow import fields, validate, Schema


class UserAuthSchema(Schema):
    email = fields.Str(required=True, validate=validate.Length(max=100))
    password = fields.Str(required=True, validate=validate.Length(max=30))


user_auth_schema = UserAuthSchema()
