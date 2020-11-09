from marshmallow import Schema, fields, ValidationError, validates, validates_schema, post_load, RAISE

from app.api.base.serializer_mixins import TimeAuditSchema
from .models import AdminUser, ClientUser


class UserBaseSchema(Schema):
    email = fields.Email(required=True)
    is_active = fields.Boolean()
    password = fields.Str(required=True, load_only=True)


class AdminUserSchema(TimeAuditSchema, UserBaseSchema):
    id = fields.Integer(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    designation = fields.Str()


class AdminUserCreateSchema(AdminUserSchema):
    class Meta:
        unknown = RAISE

    confirm_password = fields.Str(required=True, load_only=True)

    @validates("email")
    def validate_email(self, value):
        if ClientUser.query.filter_by(email=value).first():
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
        return AdminUser(**data)


class AdminUserUpdateBySelfSchema(Schema):
    class Meta:
        unknown = RAISE

    first_name = fields.Str()
    last_name = fields.Str()
    designation = fields.Str()


class AdminUserUpdateByAdminSchema(AdminUserUpdateBySelfSchema):
    is_active = fields.Boolean()


class ClientUserSchema(TimeAuditSchema, UserBaseSchema):
    id = fields.UUID(dump_only=True)
    organization = fields.Str()
    is_active = fields.Boolean(dump_only=True)
    client_token = fields.Nested("ClientTokenSchema", dump_only=True)


class ClientUserCreateSchema(ClientUserSchema):
    class Meta:
        unknown = RAISE

    confirm_password = fields.Str(required=True, load_only=True)

    @validates("email")
    def validate_email(self, value):
        if ClientUser.query.filter_by(email=value).first():
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
        return ClientUser(**data)


class ClientUserUpdateBySelfSchema(Schema):
    class Meta:
        unknown = RAISE

    organization = fields.Str()


class ClientUserUpdateByAdminSchema(ClientUserUpdateBySelfSchema):
    is_active = fields.Boolean()


class ClientTokenSchema(TimeAuditSchema, Schema):
    id = fields.Integer(dump_only=True)
    revoked = fields.Boolean()
    jti = fields.Str(dump_only=True)
