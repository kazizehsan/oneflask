from marshmallow import Schema, fields, ValidationError, validates, validates_schema, post_load, RAISE

from app.api.base.serializer_mixins import TimeAuditSchema
from .models import User


class UserResponseSchema(TimeAuditSchema, Schema):
    id = fields.UUID(dump_only=True)
    email = fields.Email(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    designation = fields.Str(dump_only=True)
    organization = fields.Str(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
    api_token = fields.Nested("APITokenSchema", dump_only=True)


class UserCreateBySelfSchema(Schema):
    class Meta:
        unknown = RAISE

    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm_password = fields.Str(required=True, load_only=True)
    first_name = fields.Str()
    last_name = fields.Str()

    @validates("email")
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('User with this email already exists')

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        errors = {}
        if data["password"] != data["confirm_password"]:
            errors["confirm_password"] = ["passwords did not match"]
        if errors:
            raise ValidationError(errors)

    @post_load
    def make_instance(self, data, **kwargs):
        del data["confirm_password"]
        return User(**data)


class UserCreateByAdminSchema(Schema):
    class Meta:
        unknown = RAISE

    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm_password = fields.Str(required=True, load_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    designation = fields.Str()
    organization = fields.Str()
    is_active = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)

    @validates("email")
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('User with this email already exists')

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        errors = {}
        if data["password"] != data["confirm_password"]:
            errors["confirm_password"] = ["passwords did not match"]
        if errors:
            raise ValidationError(errors)

    @post_load
    def make_instance(self, data, **kwargs):
        del data["confirm_password"]
        return User(**data)


class UserUpdateBySelfSchema(Schema):
    class Meta:
        unknown = RAISE

    first_name = fields.Str()
    last_name = fields.Str()
    designation = fields.Str()
    organization = fields.Str()


class UserUpdateByAdminSchema(UserUpdateBySelfSchema):
    is_active = fields.Boolean()


class APITokenSchema(TimeAuditSchema, Schema):
    id = fields.Integer(dump_only=True)
    revoked = fields.Boolean()
    jti = fields.Str(dump_only=True)
