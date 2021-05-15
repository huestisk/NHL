import pickle
import xml.etree.cElementTree as ET


def getID(num: int) -> str:
    id_str = str(num)
    while len(id_str) < 4:
        id_str = '0' + id_str
    return id_str

with open("draft/players.pkl", 'rb') as f:
    players = pickle.load(f)

def get_performance(player: str, crit: str):
	data = players[player]

	if crit == "goals_per_game":
		if data['position'] == 'G' or data['gp'] in ['-', '', '0']:
			return 0
		else:
			return round(int(data['g']) / int(data['gp']), 3)
	elif crit == "assists_per_game":
		if data['position'] == 'G' or data['gp'] in ['-', '', '0']:
			return 0
		else:
			return round(int(data['a']) / int(data['gp']), 3)
	elif crit == "points_per_game":
		if data['position'] == 'G' or data['gp'] in ['-', '', '0']:
			return 0
		else:
			return round((int(data['g']) + int(data['a'])) / int(data['gp']), 3)
	elif crit == "penalty_mins":
		return int(data['pim']) if data['pim'] != '-' and data['pim'] != '' else 0
	elif crit == "date_of_birth":
		return (int(data['birth-year']) - 2000) * 12 + int(data['birth-month'])
	elif crit == "height":
		return int(data['height'])
	elif crit == "weight":
		return int(data['weight'])
	else:
		raise Exception("Invalid Criteria.")

criteria = {
	"goals_per_game": "Total goals divided by the number of games.",
	"assists_per_game": "Total assists divided by the number of games.",
	"points_per_game": "Total goals and assists divided by the number of games.",
	"penalty_mins": "Player penatly minutes (season)",
	"date_of_birth": "Month + 12 * Years Since 2000",
	"height": "Height in cm",
	"weight": "Weight in kg",
	# "position": "Player's position: Defense, Forward, Center, Right/Left Wing, Goaltender.",
	# "shoots": "Left/Right stick curve",
}

header_dict = {
    "xmlns:xmcda": "http://www.decision-deck.org/2009/XMCDA-2.0.0",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
}

### Create alternatives.xml
root = ET.Element("xmcda:XMCDA", header_dict)
root.text = "\n\n\t"
doc = ET.SubElement(root, "alternatives", {"mcdaConcept": "NHL Draft Picks"})
doc.text = "\n\t\t"
doc.tail = "\n\n"

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
tree.write("alternatives.xml")


### Create Criteria
root = ET.Element("xmcda:XMCDA", header_dict)
root.text = "\n\n\t"
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
tree.write("criteria.xml")


### Make performaces 
root = ET.Element("xmcda:XMCDA", header_dict)
root.text = "\n\n\t"
doc = ET.SubElement(root, "performanceTable")
doc.text = "\n\t\t"
doc.tail = "\n"

id = 0
for player in players:

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
tree.write("performances.xml")
