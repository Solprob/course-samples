{
    'name': 'Students',
    'version': '1.0',
    'summary': 'To register data about students',
    'category': 'School',
    'author': 'Solprob-Digital',
    'license': 'OPL-1',
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sample_student_views.xml',
        'views/student_class.xml',
        'views/subject_calendar_views.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False
}
