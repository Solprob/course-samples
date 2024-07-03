from odoo import fields, models, api


class ClassRoom(models.Model):
    _name = "student.class.room"
    _description = "Classroom"

    name = fields.Char(string="Name", required=True)


class SubjectGeneric(models.Model):
    _name = "subject.generic"

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Name", required=False)


# Materia o Clase
class SubjectStudent(models.Model):
    _name = "subject.student"
    _description = "Subject"

    subject_generic_id = fields.Many2one("subject.generic")
    name = fields.Char(string="Name", related="subject_generic_id.name")
    teacher_id = fields.Many2one("res.partner", string="Teacher")
    evaluation_type_ids = fields.Many2many(
        "evaluation.type",
        string="Evaluation Types",
        help="Evaluation types for the subject",
    )
    evaluation_ids = fields.One2many(
        "subject.evaluation", "subject_id", string="Evaluations"
    )
    final_note = fields.Float(
        string="Final Note", compute="_compute_final_grade", store=True
    )

    @api.depends("evaluation_ids")
    def _compute_final_grade(self):
        for record in self:
            total_score = sum(
                int(evaluation.note) for evaluation in record.evaluation_ids
            )
            total_evaluations = len(record.evaluation_ids)
            record.final_note = (
                total_score / total_evaluations if total_evaluations > 0 else 0
            )

    student_id = fields.Many2one("sample.student", string="Student", ondelete="cascade")


class Evaluation(models.Model):
    _name = "subject.evaluation"
    _description = "Evaluation"

    name = fields.Char(string="Name", required=True)
    subject_id = fields.Many2one(
        "subject.student", string="Subject", ondelete="cascade"
    )
    evaluation_type_id = fields.Many2one(
        "evaluation.type",
        help="Evaluation types",
    )
    grade = fields.Integer(string="Grade", required=True)
    note = fields.Selection(
        string="Note",
        selection=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
        ],
        required=False,
    )

    test_file = fields.Binary("PDF TEST")
    teacher_sign = fields.Binary()


class EvaluationType(models.Model):
    _name = "evaluation.type"
    _description = "Evaluation Type"

    name = fields.Char(string="Name", required=True)
