from odoo import fields, models, api


class SampleStudent(models.Model):
    _name = 'sample.student'
    _description = 'Sample Student'

    name = fields.Char()
    sex = fields.Selection(
        string='Sex',
        selection=[('fem', 'fem'),
                   ('masc', 'masc'), ],
        required=False, )
    birthday = fields.Date(required=False)
    age = fields.Integer(
        required=False)
    weight = fields.Float(
        required=False)
    height = fields.Float(
        required=False)
