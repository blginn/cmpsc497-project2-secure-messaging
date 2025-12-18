import json

class Student:
    def __init__(self, name, age, major, psu_id):
        self.name = name
        self.age = age
        self.major = major
        self.psu_id = psu_id

    def to_json(self):
        return json.dumps({
            "name": self.name,
            "age": self.age,
            "major": self.major,
            "psu_id": self.psu_id
        })
