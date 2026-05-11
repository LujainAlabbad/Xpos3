"""
Marshmallow schemas for scan operations
"""
from marshmallow import Schema, fields

class ScanSchema(Schema):
    id = fields.Int()
    filename = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    completed_at = fields.DateTime()
    severity_summary = fields.Dict()