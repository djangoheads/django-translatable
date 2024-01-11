countries = [
    {"pk": 1, "name": "Kazakhstan", "code": "KZ"},
    {"pk": 2, "name": "Thailand", "code": "TH"},
    {"pk": 3, "name": "Portugal", "code": "PT"},
    {"pk": 4, "name": "Spain", "code": "ES"},
    {"pk": 5, "name": "The Netherlands", "code": "NL"},
]

regions = [{"pk": 1, "name": "East", "countries": [1, 2]}, {"pk": 2, "name": "West", "countries": [3, 4, 5]}]

translation = {
    "field://test_django_project/tcountry/1/name": {"straight": "Казахстан", "back": "Kazakhstan"},
    "field://test_django_project/tcountry/2/name": {"straight": "Таиланд", "back": "Thailand"},
    "field://test_django_project/tcountry/3/name": {"straight": "Португалия", "back": "Portugal"},
    "field://test_django_project/tcountry/4/name": {"straight": "Испания", "back": "Spain"},
    "field://test_django_project/tcountry/5/name": {"straight": "Нидерланды", "back": "The Netherlands"},
}
