class Matches:
    def __init__(self):
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)
        
    def __iter__(self):
        return iter(self.matches)
    
    def count_matches_played(self, team):
        count = 0
        for match in self.matches:
            if match.teams["home"] == team or match.teams["away"] == team:
                count += 1
        return count
    
    def get_teams(self):
        teams = []
        for match in self.matches:
            home_team = match.teams["home"]
            away_team = match.teams["away"]
        if home_team not in teams:
            teams.append(home_team)
        if away_team not in teams:
            teams.append(away_team)
        return teams

    def print_all_matches(self):
        print("All Matches:")
        for match in self.matches:
            match.print_match_details()
            print("=======================")

class Match:
    def __init__(self, data):
        self.teams = data["teams"]
        self.home_events = data["home_events"]
        self.away_events = data["away_events"]

    def print_match_details(self):
        print("Match Details:")
        print("Home Team:", self.teams["home"])
        print("Away Team:", self.teams["away"])
        print("\nHome Team Events:")
        for event in self.home_events:
            self.print_event(event)
        print("\nAway Team Events:")
        for event in self.away_events:
            self.print_event(event)
        print("\nHome goals: " + str(self.count_events(self.teams["home"], "score")))
        print("\nAway goals: " + str(self.count_events(self.teams["away"], "score")))
            
    def count_events(self, team, p_event):
        e = 0 #cantidad de eventos
        if team == self.teams["home"]:
            events = self.home_events
        if team == self.teams["away"]:
            events = self.away_events
    
        for event in events:
            if event["event"] == p_event:
                e += 1

        return e

    @staticmethod
    def print_event(event):
        print("Event:", event["event"])
        print("Time:", event["time"])
        print("Player:", event["player"])
        print("----------------------")

