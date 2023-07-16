from Rules import Rules
from Matches import Matches, Match

import json
class Results:
    def __init__(self, matches, rules):
        self.matches = matches
        self.rules = rules

    def calculate_points(self):
        results = {}
        for match in self.matches:
            home_team = match.teams["home"]
            away_team = match.teams["away"]
            home_goals = self.count_goals(home_team, match)
            away_goals = self.count_goals(away_team, match)
            home_points = self.calculate_match_points(home_team, match)
            away_points = self.calculate_match_points(away_team, match)
            home_bonus_points = self.calculate_bonus_points(home_team, match)
            away_bonus_points = self.calculate_bonus_points(away_team, match)
            
            # Sumar los goles, los puntos y los puntos de bonificación al equipo existente
            if home_team in results:
                results[home_team]["goals"] += home_goals
                results[home_team]["points"] += home_points
                results[home_team]["bonus_points"] += home_bonus_points
                results[home_team]["matches"] += 1
            else:
                results[home_team] = {
                    "team": home_team,
                    "points": home_points,
                    "bonus_points": home_bonus_points,
                    "matches": 1,
                    "goals": home_goals
                }

            if away_team in results:
                results[away_team]["goals"] += away_goals
                results[away_team]["points"] += away_points
                results[away_team]["bonus_points"] += away_bonus_points
                results[away_team]["matches"] += 1
            else:
                results[away_team] = {
                    "team": away_team,
                    "points": away_points,
                    "bonus_points": away_bonus_points,
                    "matches": 1,
                    "goals": away_goals
                }

        results_json = json.dumps(list(results.values()))
        return results_json
                    
    #   Recibe un equipo y un partido y retorna los puntos obtenidos por ese partido
    def calculate_match_points(self, team, match):
        team_goals = self.count_goals(team, match)
        if team == match.teams["home"]:
            other_team_goals = self.count_goals(match.teams["away"], match)
        else:
            other_team_goals = self.count_goals(match.teams["home"], match)
        
        if team_goals > other_team_goals:
            #Victoria
            return self.rules.get_win_points()
        if team_goals < other_team_goals:
            #derrota
            return self.rules.get_lose_points()
        if team_goals == other_team_goals:
            #empate
            return self.rules.get_draw_points()
    
    #   Esta funcion recibe un equipo y un partido y retorna los goles que marco el equipo, teniendo en cuenta los valores 
    #   de cada gol segun las reglas
    def count_goals(self, team, match):
        goals = 0
        if team == match.teams["home"]:
            events = match.home_events
        if team == match.teams["away"]:
            events = match.away_events
    
        for event in events:
            if event["event"] == "score":
                goals += self.goal_value(event)

        return goals

    #   Esta funcion recibe el nombre de un equipo y un partido en el que aparece, y devuelve todos los bonus points obtenidos
    #   por el equipo en el partido
    def calculate_bonus_points(self, team, match):
        bonus_points = 0
        at_least_condition = False
        if team == match.teams["home"]:
            events = match.home_events
        if team == match.teams["away"]:
            events = match.away_events
            
        for rule in self.rules:
            for event in events:
                if event["event"] == rule.event:
                    if rule.type == "side":
                        if rule.condition["at_least"] <= match.count_events(team, event["event"]):
                            at_least_condition = True
                    if rule.type == "single":
                        if "after_time" in rule.condition:
                            if self.compare_time(rule.condition["after_time"], event["time"]) > 0:
                                bonus_points += 1
                        if "distance" in rule.condition and "obs" in event:
                            if self.compare_distance(rule.condition["distance"], event["obs"]["distance"]) > 0:
                                bonus_points += 1

        if at_least_condition:
            bonus_points += 1
        return bonus_points
    
    
    #   Esta funcion recibe un evento "score" y devuelve el valor del gol
    def goal_value(self, event):
        goal_value = 1
        
        for rule in self.rules:
            if rule.type == "particular":
                if rule.event == "score" and "obs" in event:
                    if type(event["obs"]) is not str: # se asume que, a diferencia del archivo brasil_sweden.json, los campos de "obs" 
                                                      # vendran con formato key->value y no string.
                        if set(rule.condition.keys()) == set(event["obs"].keys()):
                            if self.check_conditions(rule, event):
                                goal_value *= float(rule.value_factor[1:])
        return goal_value


    #   Esta funcion recibe una regla de tipo "particular" y un evento, cuyos campos de "condition" y "obs" son de la misma estructura
    #   y devuelve "true" si las condiciones de las reglas se cumplen en el evento, de lo contrario, false
    def check_conditions(self, rule, event):
        if "player" in rule.condition:
            if rule.condition["player"] != event["obs"]["player"]:
                return False
        if "distance" in rule.condition:
            if self.compare_distance(rule.condition["distance"], event["obs"]["distance"]) < 0:
                return False
        if "after_time" in rule.condition:
            if self.compare_time(rule.condition["after_time"], event["time"]) < 0:
                return False
        return True
         
                            
    #   Esta funcion compara distancias, tomando como primer parametro la distancia de referencia de una regla, por ejemplo: "+25m"
    #   y como segundo parametro la distancia a evaluar, en caso de que el segundo parametro se encuentre en el intervalo de la regla
    #   devuelve 1, caso contrario -1
    def compare_distance(self, reference, distance):
        distance = int(distance[:-1])
        if reference[0] == "-":
            reference_value = int(reference[1:-1])
            if distance >= 0 and distance <= reference_value:
                return 1
            else:
                return -1
        else:
            if reference[0] == "+":
                reference_value = int(reference[1:-1])
                if distance >= reference_value:
                    return 1
                else:
                    return -1
    
    #   Esta funcion recibe como parametro el tiempo a partir del que una regla entra en vigencia y el tiempo en el que ocurre un evento
    #   si el evento ocurre despues del tiempo estimado por la regla, retorna 1, caso contrario -1
    #   (tiene en cuenta que si el tiempo de la regla es de tipo tiempo extra "45 + 0", el evento tambien tiene que ocurrir en tiempo extra) 
    def compare_time(self, rule_time, event_time):
        if "+" not in event_time and "+" in rule_time:
            #si la regla es tiempo extra y el evento no, descarto automaticamente
            return -1
        else:
            #si la regla es tiempo normal, evaluo teniendo en cuenta que el evento pudo ser en tiempo extra
            return self.compare_extra_time(rule_time, event_time)
        
    #   Esta funcion complementa a "compare_time" y compara dos tiempos que pueden o no ser extra, si el primer parametro ocurre primero retorna 1,
    #   caso contrario -1
    def compare_extra_time(self, rule_time, event_time):
        if "+" not in rule_time:
            rule_time += " +0"
        if "+" not in event_time:
            event_time += " +0"
        
        minutes1, added_min1 = map(int, rule_time.split("+"))
        minutes2, added_min2 = map(int, event_time.split("+"))
        
        minutes1 += added_min1
        minutes2 += added_min2

        if minutes1 < minutes2:
            return 1
        else:
            return -1
