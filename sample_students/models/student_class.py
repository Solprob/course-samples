from odoo import fields, models, api


class ClassRoom(models.Model):
    _name = "student.class.room"
    _description = "Classroom"

    name = fields.Char(string="Name", required=True)


# Materia o Clase
class Subject(models.Model):
    _name = "subject"
    _description = "Subject"

    name = fields.Char(string="Name", required=True)
    teacher_id = fields.Many2one("res.partner", string="Teacher")
    evaluation_type_ids = fields.Many2many(
        "evaluation.type",
        string="Evaluation Types",
        help="Evaluation types for the subject",
    )
    evaluation_ids = fields.One2many("evaluation", "subject_id", string="Evaluations")
    final_note = fields.Float(
        string="Final Grade", compute="_compute_final_grade", store=True
    )

    @api.depends("evaluation_ids")
    def _compute_final_grade(self):
        for record in self:
            total_score = sum(evaluation.note for evaluation in record.evaluation_ids)
            total_evaluations = len(record.evaluation_ids)
            record.final_note = (
                total_score / total_evaluations if total_evaluations > 0 else 0
            )

    student_id = fields.Many2one("sample.student", string="Student", ondelete="cascade")


class Evaluation(models.Model):
    _name = "evaluation"
    _description = "Evaluation"

    name = fields.Char(string="Name", required=True)
    subject_id = fields.Many2one("subject", string="Subject", ondelete="cascade")
    grade = fields.Integer(string="Grade", required=True)
    note = fields.Float(string="Note", required=True)


class EvaluationType(models.Model):
    _name = "evaluation.type"
    _description = "Evaluation Type"

    name = fields.Char(string="Name", required=True)
