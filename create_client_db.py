from face_analyzer import models
from datetime import date

from pathlib import Path
import os


clients = [
    {
        "name": "Angelina_Jolie",
        "date_of_birth": date(1975, 6, 4),
        "VIP": False,
        "is_allowed_in": True,
        "comments": "Wow so pwetty",
        "total_entry_tickets_bought": 12,
        "creation_date": date(2019, 9, 9)
    },
    {
        "name": "Chris_Hemsworth",
        "date_of_birth": date(1983, 8, 11),
        "VIP": False,
        "is_allowed_in": False,
        "comments": "THOOOOOR!!! Isn't allowed in anymore because he breaks everything.",
        "total_entry_tickets_bought": 35,
        "creation_date": date(2017, 5, 25)
    },
    {
        "name": "Elon_Musk",
        "date_of_birth": date(1971, 6, 28),
        "VIP": True,
        "is_allowed_in": True,
        "comments": "$$$$$$$",
        "total_entry_tickets_bought": 3,
        "creation_date": date(2021, 6, 23),
    },
    {
        "name": "George_Clooney",
        "date_of_birth": date(1961, 5, 6),
        "VIP": True,
        "is_allowed_in": True,
        "comments": "Haven't I seen this guy somewhere...",
        "total_entry_tickets_bought": 75,
        "creation_date": date(2016, 12, 2),
    },
    {
        "name": "Jack_Dorsey",
        "date_of_birth": date(1976, 11, 19),
        "VIP": False,
        "is_allowed_in": False,
        "comments": "some random tech dude",
        "total_entry_tickets_bought": 1,
        "creation_date": date(2019, 7, 16),
    },
    {
        "name": "Jeff_Bezos",
        "date_of_birth": date(1964, 1, 12),
        "VIP": True,
        "is_allowed_in": True,
        "comments": "Just let him in.",
        "total_entry_tickets_bought": 0,
        "creation_date": date(1921, 1, 1),
    },
    {
        "name": "Jennifer_Aniston",
        "date_of_birth": date(1969, 1, 11),
        "VIP": False,
        "is_allowed_in": False,
        "comments": "barfs everywhere",
        "total_entry_tickets_bought": 16,
        "creation_date": date(1983, 8, 11),
    },
    {
        "name": "Jeremy_Renner",
        "date_of_birth": date(1971, 1, 7),
        "VIP": False,
        "is_allowed_in": True,
        "comments": "Really chill fellow",
        "total_entry_tickets_bought": 25,
        "creation_date": date(2018, 4, 5),
    },
    {
        "name": "Katy_Perry",
        "date_of_birth": date(1984, 10, 25),
        "VIP": True,
        "is_allowed_in": True,
        "comments": "I kissed a girl and I liked it ...",
        "total_entry_tickets_bought": 57,
        "creation_date": date(1983, 8, 11),
    },
    {
        "name": "Leonardo_Dicaprio",
        "date_of_birth": date(1974, 11, 11),
        "VIP": False,
        "is_allowed_in": True,
        "comments": "Me: I will add you to this database. Leo: *zoom in* you will?",
        "total_entry_tickets_bought": 30,
        "creation_date": date(1983, 8, 11),
    },
    {
        "name": "Mark_Zuckerberg",
        "date_of_birth": date(1984, 5, 14),
        "VIP": True,
        "is_allowed_in": False,
        "comments": "We don't take too kindly to robots 'round these parts...",
        "total_entry_tickets_bought": 0,
        "creation_date": date(2008, 9, 29),
    },
    {
        "name": "Matt_Damon",
        "date_of_birth": date(1970, 10, 8),
        "VIP": False,
        "is_allowed_in": True,
        "comments": "I liked this guy in Interstellar",
        "total_entry_tickets_bought": 85,
        "creation_date": date(2010, 2, 10),
    },
    {
        "name": "Robert_Downey_Jr",
        "date_of_birth": date(1965, 4, 4),
        "VIP": True,
        "is_allowed_in": True,
        "comments": "IRON MAAAAAAN!!!!!",
        "total_entry_tickets_bought": 41,
        "creation_date": date(2017, 8, 20),
    },
    {
        "name": "Scarlett_Johansson",
        "date_of_birth": date(1984, 11, 22),
        "VIP": False,
        "is_allowed_in": True,
        "comments": "BOOBA",
        "total_entry_tickets_bought": 13,
        "creation_date": date(2020, 10, 5),
    }
]

for client in clients:
    new_client = models.ClientDB()
    new_client.client_name = client["name"]
    new_client.date_of_birth = client["date_of_birth"]
    new_client.VIP = client["VIP"]
    new_client.is_allowed_in = client["is_allowed_in"]
    new_client.comments = client["comments"]
    new_client.total_entry_tickets_bought = client["total_entry_tickets_bought"]
    new_client.creation_date = client["creation_date"]
    new_client.save()
