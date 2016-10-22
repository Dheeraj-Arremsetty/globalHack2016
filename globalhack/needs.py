class Needs(object):
    NEEDS = [{ 'name': 'Shelter',         'enabled': False, 'id': 'shelter' },
             { 'name': 'Food',            'enabled': False, 'id': 'food' },
             { 'name': 'Bills',           'enabled': False, 'id': 'bills' },
             { 'name': 'Employment',      'enabled': False, 'id': 'jobs' },
             { 'name': 'Training',        'enabled': False, 'id': 'training' },
             { 'name': 'Social Services', 'enabled': False, 'id': 'social_services' }]

    @staticmethod
    def get_needs():
        return Needs.NEEDS
