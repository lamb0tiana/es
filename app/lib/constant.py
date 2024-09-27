from enum import Enum

riesterDBColumns = ["nom", "prenom", "email", "tel_mobile", "tel_fixe", "tel_bureau", "nom_contact_pro",
                    "prenom_contact_pro",
                    "email_contact_pro", "tel_mobile_contact_pro", "tel_bureau_contact_pro"]

riesterAPJMatchingColumns = ['Nom utilisateur', 'Prénom utilisateur', 'Email utilisateur', 'Tél. domicile utilisateur',
                             'Tél. professionnel utilisateur', 'Tél. portable utilisateur']

riesterVOJMatchingColumns = ["Nom client", "Prénom client", "Tél. domicile client", "Tél. professionnel client",
                             "Tél. portable client",
                             "Email client"]

riesterVNJMatchingColumns = ['Nom client', "Prénom client", "Tél. domicile client", "Tél. professionnel client",
                             "Tél. portable client",
                             "Email client"]

requiredMatchingFields = ['Nom utilisateur', 'Prénom utilisateur', 'Nom client', 'Prénom client']

#
# Mapping insertion table
#
mappingDbFields = {
    "nom": ['Nom utilisateur', 'Nom client', 'Nom utilisateur'],
    "prenom": ['Prénom  utilisateur', 'Prénom client', 'Prénom utilisateur'],
    "email": ['Email utilisateur', 'Email client'],
    "tel_mobile": ['Tél. portable utilisateur', 'Tél. portable client'],
    "tel_fixe": ['Tél. domicile client', 'Tél. domicile utilisateur'],
    "tel_bureau": ['Tél. professionnel utilisateur', 'Tél. professionnel client'],
    "code_postal": ["Code postal utilisateur", "Code postal client"],
    "compte_affaire": ['Nom Affaire']
}

class QueryBehavior(Enum):
    ALL_MATCHES = 0  # all occurences must match eg +NOM+PRNOM+EMAIL+TEL
    MAIN_MATCHES_OTHER_MATCHES_ONE = 1 #+NOM+PRENOM +(EMAIL|TEL)
    ONLY_MAIN_MATCH = 2  # nom+prenom must match, others are optionals : eg +NOM+PRENOM EMAIL TEL
    SOME_MAIN_MATCH = 3  # either nom or prenom should match and either one user's info +(NOM|PRENOM) +(EMAIL|TEL)
