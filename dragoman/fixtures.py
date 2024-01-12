countries = [
    {"pk": 1, "name": "Kazakhstan", "code": "KZ"},
    {"pk": 2, "name": "Thailand", "code": "TH"},
    {"pk": 3, "name": "Portugal", "code": "PT"},
    {"pk": 4, "name": "Spain", "code": "ES"},
    {"pk": 5, "name": "The Netherlands", "code": "NL"},
]

cities = [
    {"pk": 1, "name": "Almaty", "population": 1777000, "country": 1},
    {"pk": 2, "name": "Bangkok", "population": 11234000, "country": 2},
    {"pk": 3, "name": "Lisbon", "population": 504718, "country": 3},
    {"pk": 4, "name": "Madrid", "population": 3223000, "country": 4},
    {"pk": 5, "name": "Madrid", "population": 821752, "country": 5},
]

regions = [{"pk": 1, "name": "East", "countries": [1, 2]}, {"pk": 2, "name": "West", "countries": [3, 4, 5]}]

translation = {
    "field://test_django_project/tcountry/1/name": {"ru": "Казахстан", "en": "Kazakhstan"},
    "field://test_django_project/tcountry/2/name": {"ru": "Таиланд", "en": "Thailand"},
    "field://test_django_project/tcountry/3/name": {"ru": "Португалия", "en": "Portugal"},
    "field://test_django_project/tcountry/4/name": {"ru": "Испания", "en": "Spain"},
    "field://test_django_project/tcountry/5/name": {"ru": "Нидерланды", "en": "The Netherlands"},
}
