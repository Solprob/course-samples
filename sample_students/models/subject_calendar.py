from odoo import fields, models, api


class SubjectCalendar(models.Model):
    _name = "subject.calendar"
    _description = "Calendario de examenes"

    name = fields.Char()
    subject_generic_id = fields.Many2one("subject.generic")
    date_start = fields.Datetime(string="Comienza", required=False)
    date_stop = fields.Datetime(string="Finaliza", required=False)
