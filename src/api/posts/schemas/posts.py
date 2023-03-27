from marshmallow import fields, validate, Schema


class PostSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(max=60))
    content = fields.Str()


post_schema = PostSchema()
