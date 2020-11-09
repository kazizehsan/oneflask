from marshmallow import fields


class TimeAuditSchema(object):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)