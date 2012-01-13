# coding: utf-8

# Test data
conferences = [u'TéstMUN 1',u'TéstMUN 2',u'TéstMUN 3']
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
schools = [u'Schoöl 1', u'Schoöl 2', u'Schoöl 3', u'Schoöl 4']
users_sponsors = [sponsor1, sponsor2, sponsor3, sponsor4, sponsor5, sponsor6, sponsor7, sponsor8]
users_sponsors_by_conference = {u'TéstMUN 1' : [sponsor1, sponsor2, sponsor3],
                                u'TéstMUN 2' : [sponsor1, sponsor4, sponsor5],
                                u'TéstMUN 3' : [sponsor6, sponsor7, sponsor8]} 
schools_by_conference = {u'TéstMUN 1' : [u'Schoöl 1', u'Schoöl 2'],
                         u'TéstMUN 2' : [u'Schoöl 1', u'Schoöl 3'],
                         u'TéstMUN 3' : [u'Schoöl 1', u'Schoöl 4']}
users_sponsors_by_school = {u'Schoöl 1' : [sponsor1, sponsor6],
                            u'Schoöl 2' : [sponsor2, sponsor3],
                            u'Schoöl 3' : [sponsor4, sponsor5],
                            u'Schoöl 4' : [sponsor7, sponsor8]}

# Secretariat
secretariat1 = {'username': 'secretariat1','password': 'secretariat123'}
secretariat2 = {'username': 'secretariat2','password': 'secretariat456'}
secretariat3 = {'username': 'secretariat3','password': 'secretariat789'}
users_secretariat = [secretariat1, secretariat2, secretariat3]
secretariat_by_conference = {u'TéstMUN 1' : secretariat1,
                             u'TéstMUN 2' : secretariat2,
                             u'TéstMUN 3' : secretariat3} 

first_name = u" Fḭrst"
last_name = u" Lâst"

new_country_name = u"Médecins Sans Frontières"
new_committee_name = u"L'Organisation des Nations unies pour l’éducation, la science et la culture (UNESCO)"
new_country_code = 'ng'