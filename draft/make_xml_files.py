import sys
import pathlib
import pickle
from itertools import islice

sys.path.append(pathlib.Path(__file__).parent.absolute())
from helper_functions import *


LIMIT_NUM_PLAYERS = 32

base = "/home/kevin/diviz_workspace/NHL_Draft/"
alternatives_file = base + "alternatives.xml"
criteria_file = base + "criteria.xml"
performance_file = base + "performances.xml"
preference_file = base + "preferences.xml"


def take(n, iterable):
	return list(islice(iterable, n))

with open("draft/players.pkl", 'rb') as f:
    players = pickle.load(f)

players = take(LIMIT_NUM_PLAYERS, players.items())
players = [player for player in players 
    if player[1]['position'] != "G" and player[1]['position'] != "D"]
players = dict(players)

criteria = {
    "goals_per_game": "Total goals divided by the number of games.",
    "assists_per_game": "Total assists divided by the number of games.",
    "points_per_game": "Total goals and assists divided by the number of games.",
    "penalty_mins": "Player penatly minutes (season)",
    # "date_of_birth": "Month + 12 * Years Since 2000",
    "height": "Height in cm",
    "weight": "Weight in kg",
    # "position": "Player's position: Defense, Forward, Center, Right/Left Wing, Goaltender.",
    # "shoots": "Left/Right stick curve",
}


# Create alternatives.xml
create_alternatives_xml(players, alternatives_file)


# Create criteria.xml
create_criteria_xml(criteria, criteria_file)


# Create performaces.xml
create_performances_xml(players, criteria, performance_file)


# Create preferences.xml
create_preferences_xml(players, preference_file)


