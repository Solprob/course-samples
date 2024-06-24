from datetime import datetime, date

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
    weight = fields.Float(
        required=False)
    height = fields.Float(
        required=False)
    is_external = fields.Boolean(
        string='Is external?',
        default=False,
        required=False)
    father_id = fields.Many2one('res.partner', string='Father')
    mother_id = fields.Many2one('res.partner', string='Mother')
    subject_ids = fields.One2many('subject', 'student_id', string='Subjects')
    room_id = fields.Many2one('student.class.room', string='Classroom')

    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                today = date.today()
                # Calculate the age
                age = today.year - record.birthday.year - (
                            (today.month, today.day) < (record.birthday.month, record.birthday.day))
                record.age = age
            else:
                record.age = 0  # Set age to 0 if no birthday is provided

