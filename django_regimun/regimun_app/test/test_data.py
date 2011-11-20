# Test data
conferences = ['TestMUN 1','TestMUN 2','TestMUN 3']
user_none = {'username' : 'none1', 'password' : 'none123'}
user_staff = {'username': 'staff1', 'password': 'staff123'}

# Schools / sponsors
sponsor1 = {'username': 'sponsor1','password': 'sponsor123'}
sponsor2 = {'username': 'sponsor2','password': 'sponsor345'}
sponsor3 = {'username': 'sponsor3','password': 'sponsor678'}
sponsor4 = {'username': 'sponsor4','password': 'sponsor345'}
sponsor5 = {'username': 'sponsor5','password': 'sponsor678'}
sponsor6 = {'username': 'sponsor6','password': 'sponsor123'}
sponsor7 = {'username': 'sponsor7','password': 'sponsor345'}
sponsor8 = {'username': 'sponsor8','password': 'sponsor678'}
schools = ['School 1', 'School 2', 'School 3', 'School 4']
users_sponsors = [sponsor1, sponsor2, sponsor3, sponsor4, sponsor5, sponsor6, sponsor7, sponsor8]
users_sponsors_by_conference = {'TestMUN 1' : [sponsor1, sponsor2, sponsor3],
                                'TestMUN 2' : [sponsor1, sponsor4, sponsor5],
                                'TestMUN 3' : [sponsor6, sponsor7, sponsor8]} 
schools_by_conference = {'TestMUN 1' : ['School 1', 'School 2'],
                         'TestMUN 2' : ['School 1', 'School 3'],
                         'TestMUN 3' : ['School 1', 'School 4']}
users_sponsors_by_school = {'School 1' : [sponsor1, sponsor6],
                            'School 2' : [sponsor2, sponsor3],
                            'School 3' : [sponsor4, sponsor5],
                            'School 4' : [sponsor7, sponsor8]}

# Secretariat
secretariat1 = {'username': 'secretariat1','password': 'secretariat123'}
secretariat2 = {'username': 'secretariat2','password': 'secretariat456'}
secretariat_by_conference = {'TestMUN 1' : secretariat1,
                             'TestMUN 2' : secretariat1,
                             'TestMUN 3' : secretariat2} 