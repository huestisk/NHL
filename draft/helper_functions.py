import random
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element

def getRoot():
    header_dict = {
        "xmlns:xmcda": "http://www.decision-deck.org/2009/XMCDA-2.0.0",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }
    root = ET.Element("xmcda:XMCDA", header_dict)
    root.text = "\n\n\t"
    return root


def getID(num: int) -> str:
    id_str = str(num)
    while len(id_str) < 4:
        id_str = '0' + id_str
    return id_str


def create_alternatives_xml(players, filename):
    root = getRoot()
    doc = ET.SubElement(root, "alternatives", {
                        "mcdaConcept": "NHL Draft Picks"})
    doc.text = "\n\t\t"
    doc.tail = "\n\n"
    # Add players as alternatives
    id = 0
    for player in players:
        id += 1
        tmp_dict = {
            "id": getID(id),
            "name": player
        }
        line = ET.SubElement(doc, "alternative", tmp_dict)
        line.tail = "\n\t\t"
    else:
        line.tail = "\n\t"

    tree = ET.ElementTree(root)
    tree.write(filename)


def create_criteria_xml(criteria, filename):
	root = getRoot()
	doc = ET.SubElement(root, "criteria")
	doc.text = "\n\t\t"
	doc.tail = "\n\n"

	for crit in criteria:
		tmp_dict = {
			"id": crit,
			"name": criteria[crit]
		}
		line = ET.SubElement(doc, "criterion", tmp_dict)
		line.text = "\n\t\t\t"
		line.tail = "\n\t\t"

		scale = ET.SubElement(line, "scale")
		scale.text = "\n\t\t\t\t"
		scale.tail = "\n\t\t"

		quant = ET.SubElement(scale, "quantitative")
		quant.text = "\n\t\t\t\t\t"
		quant.tail = "\n\t\t\t"

		pDir = ET.SubElement(quant, "preferenceDirection")

		# We want few penalties and older players
		if crit == "penalty_mins" or crit == "date_of_birth":
			pDir.text = "min"
		else:
			pDir.text = "max"

		pDir.tail = "\n\t\t\t\t"

	tree = ET.ElementTree(root)
	tree.write(filename)



### Performance

def get_performance(data, crit: str) -> int:
    out = 0

    if crit == "goals_per_game" and data['position'] != 'G' and data['gp'] not in ['-', '', '0']:
        out = 5 *int(data['g']) / int(data['gp'])

    elif crit == "assists_per_game" and data['position'] != 'G' and data['gp'] not in ['-', '', '0']:
        out = 5 * int(data['a']) / int(data['gp'])

    elif crit == "points_per_game" and data['position'] != 'G' and data['gp'] not in ['-', '', '0']:
        out = 2.5 * (int(data['g']) + int(data['a'])) / int(data['gp'])

    elif crit == "penalty_mins" and data['pim'] != '-' and data['pim'] != '':
        out = int(data['pim']) / 7

    elif crit == "date_of_birth":
        out = (int(data['birth-year']) - 2001) * 12 + int(data['birth-month'])

    elif crit == "height":
        out = (int(data['height']) - 170) / 5

    elif crit == "weight":
        out = (int(data['weight']) - 70) / 5

    return min(5, max(1, int(out)))


def create_performances_xml(players, criteria, filename):
	root = getRoot()
	doc = ET.SubElement(root, "performanceTable")
	doc.text = "\n\t\t"
	doc.tail = "\n"

	id = 0
	for player in players.values():

		altPerf = ET.SubElement(doc, "alternativePerformances")
		altPerf.text = "\n\t\t\t"
		altPerf.tail = "\n\n\t\t"

		id += 1
		alt = ET.SubElement(altPerf, "alternativeID")
		alt.text = getID(id)
		alt.tail = "\n\t\t\t"

		# Compute performances
		for crit in criteria:
			perf = ET.SubElement(altPerf, "performance")
			perf.text = "\n\t\t\t\t"
			perf.tail = "\n\t\t\t"

			critID = ET.SubElement(perf, "criterionID")
			critID.text = crit
			critID.tail = "\n\t\t\t\t"

			val = ET.SubElement(perf, "value")
			val.text = "\n\t\t\t\t\t"
			val.tail = "\n\t\t\t"

			real = ET.SubElement(val, "real")
			result = get_performance(player, crit)
			real.text = str(result)
			real.tail = "\n\t\t\t\t"
		
		else:
			perf.tail = "\n\t\t"

	else:
		altPerf.tail = "\n\n\t"

	tree = ET.ElementTree(root)
	tree.write(filename)


### Preferences

MAX_PREF_LEN = 4


def yes_or_no(question):
    reply = str(input(question + ' (y/N): ')).lower().strip()
    if len(reply) > 0 and reply[0] == 'y':
        return True
    else:
        False


def get_preferences(players: list, type_: str) -> list:
    if type_ == "strong":
        type_text = "better than"
    elif type_ == "weak":
        type_text = "slightly better than"
    elif type_ == "indif":
        type_text = "as good as"
    else:
        raise Exception("Invalid relation type.")

    i = 0
    prefs = []
    num_players = len(players)
    while len(prefs) < MAX_PREF_LEN-1 and i < num_players:
        i += 1
        id_1 = random.randint(1, num_players)
        id_2 = random.randint(1, num_players)
        
        if id_1 == id_2:       # TODO: check for repeated questions
            i -= 1
            continue

        if yes_or_no(f"Is {players[id_1-1]} {type_text} {players[id_2-1]}?"):
            prefs.append((getID(id_1), getID(id_2)))
        
    return prefs


def write_pairs(pairs: list, parent: Element):
    # TODO: Get preferences first in GUI
    for pair in pairs:
        p = ET.SubElement(parent, "pair")
        p.text = "\n\t\t\t\t"
        p.tail = "\n\t\t\t"

        init = ET.SubElement(p, "initial")
        init.text = "\n\t\t\t\t\t"
        init.tail = "\n\t\t\t\t"

        alt1 = ET.SubElement(init, "alternativeID")
        alt1.text = str(pair[0])
        alt1.tail = "\n\t\t\t\t"

        term = ET.SubElement(p, "terminal")
        term.text = "\n\t\t\t\t\t"
        term.tail = "\n\t\t\t"

        alt2 = ET.SubElement(term, "alternativeID")
        alt2.text = str(pair[1])
        alt2.tail = "\n\t\t\t\t"
    else:
        p.tail = "\n\t\t"


def create_preferences_xml(players, filename):
    root = getRoot()
    # Get & write 3 types of relations
    for relation in ["strong", "weak", "indif"]:
        doc = ET.SubElement(root, "alternativesComparisons")
        doc.text = "\n\t\t"
        doc.tail = "\n\n\t"

        type_ = ET.SubElement(doc, "comparisonType")
        type_.text = relation
        type_.tail = "\n\t\t"

        pairs = ET.SubElement(doc, "pairs")
        pairs.text = "\n\t\t\t"
        pairs.tail = "\n\t"

        preferences = get_preferences(list(players.keys()), relation)
        write_pairs(preferences, pairs)
    else:
        doc.tail = "\n\n"


    tree = ET.ElementTree(root)
    tree.write(filename)


