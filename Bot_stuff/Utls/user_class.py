from .bot_init import *
class User_class():
    def __init__(self, user_name, user_data):
        self.user_name = user_name
        self.user_data = user_data
    
    def save_to_points(self):
        all_data = open_file(points_P)

        all_data[self.user_name] = self.user_data

        save_file(points_P,all_data)

    def check(self):
        expected_values = {
            "points": 0,
            "inventory":[],
            "win_streak_rps": 0,
            "helm_on": False,
            "has_voted": False,
            "voted_for": None,
            "votes": 0,
            "titles": [],
            "lir_data": 0,
            "catch cooldown": 0,
            "has_used_day_thing": [False, False, False] 
        }
        
        for key,value in expected_values.items():
            if key not in self.user_data:
                self.user_data[key] = value

        self.save_to_points()

    def modify(self, key, value):
        if key not in self.user_data:
            raise Exception("That key does not exist in the user")
        if type(self.user_data[key]) != type(value):
            raise Exception("User type in value does not match user's key:value")
        
        self.user_data[key] = value

        self.save_to_points()
    def append_inventory(self, item):
        self.user_data["inventory"].append(item)
        self.save_to_points()
    def remove_inventory(self,item):
        if item not in self.user_data["inventory"]:
            raise Exception("That is not a value in that user's inventory")
        self.user_data["inventory"].remove(item)

        self.save_to_points()
    def add_arb(self, key, add_amount):
        if not isinstance(add_amount,int):
            raise Exception("Can not put a non int value into the points feild")
        if key not in self.user_data:
            raise Exception("That key does not exist in the user")
        self.user_data[key] += add_amount
        
        self.save_to_points()
    def get(self,key):
        if key not in self.user_data:
            raise Exception("That key does not exist in user data")
        return self.user_data[key]

    def add_points(self, points):
        if not isinstance(points,int):
            raise Exception("Can not put a non int value into the points feild")

        if points < 0:
            if (self.get("points") + points) < 0:
                return True 

        self.user_data["points"] += points
         
        self.save_to_points()
