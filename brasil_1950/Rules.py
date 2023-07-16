class Rules:
    def __init__(self, json_data):
        self.rules = []
        
        for rule_data in json_data:
            rule = Rule(rule_data)
            self.rules.append(rule)
            
    def __iter__(self):
        return iter(self.rules)
            
    def get_win_points(self):
        for rule in self.rules:
            if rule.type == "match":
                if rule.event == "win":
                    return rule.points
        return 3 #valor por defecto
                    
    def get_lose_points(self):
        for rule in self.rules:
            if rule.type == "match":
                if rule.event == "lose":
                    return rule.points
        return 0 #valor por defecto
                
    def get_draw_points(self):
        for rule in self.rules:
            if rule.type == "match":
                if rule.event == "draw":
                    return rule.points
        return 1 #valor por defecto

    def print_rules_details(self):
        print("Rules Details:")
        for rule in self.rules:
            rule.print_rule_details()
            print()

class Rule:
    def __init__(self, data):
        self.name = data["name"]
        self.type = data["type"]
        self.event = data["event"]
        self.points = data.get("points", None)
        self.condition = data.get("condition", None)
        self.bonus_points = data.get("bonus_points", None)
        self.value_factor = data.get("value_factor", None)

    def print_rule_details(self):
        print("Rule Details:")
        print("Name:", self.name)
        print("Type:", self.type)
        print("Event:", self.event)
        if self.condition:
            print("Condition:", self.condition)
        if self.bonus_points:
            print("Bonus Points:", self.bonus_points)
        if self.value_factor:
            print("Value Factor:", self.value_factor)
        print("----------------------")

