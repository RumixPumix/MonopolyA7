import random

fields = {}
players = {}
jail = {}
jail_money = 0

upgrade_tiers = {
    "0": [10, 30, 90, 160, 250], #Valentine
    "1": [20, 60, 180, 320, 450], #BlackWater
    "2": [30, 90, 270, 400, 550], #Malinovka, Himmelsdorf
    "3": [40, 100, 390, 450, 600], #Stalingrad
    "4": [50, 150, 450, 625, 750], #Overworld, Nether
    "5": [60, 180, 500, 700, 900], #The End
    "6": [70, 200, 550, 750, 950], #The Island, Fjordur
    "7": [80, 220, 600, 800, 1000], #The Center
    "8": [90, 250, 700, 875, 1050], #Helgen, Sovngarde
    "9": [100, 300, 750, 925, 1100], #High Hrothgar
    "10": [110, 330, 800, 975, 1150], #Light Containment, Heavy Containment
    "11": [120, 360, 850, 1025, 1200], #Surface
    "12": [130, 390, 900, 1100, 1275], #Coastline, Oregon
    "13": [150, 450, 1000, 1200, 1400], #Lair
    "14": [175, 500, 1100, 1300, 1500], #Summoners Rift
    "15": [200, 600, 1400, 1700, 2000] #Howling Abyss
}

kaj_sad_karte = {
    "card1": {
        "description": "buco je smislil masterplan da te iscupa iz zatvora",
        "penalty": None,
        "bonus": None,
        "move": None,
        "jail": False
    },
    "card2": {
        "description": "zajebo si brojanje plati 50 kuna kaznu",
        "penalty": 50,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card3": {
        "description": "plati rumi hosting za stranicu 50 kuna",
        "penalty": 50,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card4": {
        "description": "bolestan si, psihijatarski racun je 100 kuna",
        "penalty": 100,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card5": {
        "description": "council je odlucio da dobijas 25 kuna",
        "penalty": None,
        "bonus": 25,
        "move": None,
        "jail": None
    },
    "card6": {
        "description": "prodal si svoj iron account, uzmi 50 kuna",
        "penalty": None,
        "bonus": 50,
        "move": None,
        "jail": None
    },
    "card7": {
        "description": "idi na start",
        "penalty": None,
        "bonus": None,
        "move": "start",
        "jail": None
    },
    "card8": {
        "description": "edo je mislil da si zena, kupil ti je skin od 100 kuna",
        "penalty": 100,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card9": {
        "description": "edo je darezljiv, uzmi 200 kuna",
        "penalty": None,
        "bonus": 200,
        "move": None,
        "jail": None
    },
    "card10": {
        "description": "grdi si, uzmi si 10 kuna za utjehu",
        "penalty": None,
        "bonus": 10,
        "move": None,
        "jail": None
    },
    "card11": {
        "description": "plati kuce i hotele, 40 i 115 po komadu",
        "penalty": "house: 40, hotel: 115",
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card12": {
        "description": "naknada za igranje liga, ako si igro lig na mainu, uzmi 100 kuna",
        "penalty": None,
        "bonus": 100,
        "move": None,
        "jail": None
    }
}

pomilovanje_karte = {
    "card1": {
        "description": "kazna za razbijeni monitor, 25 kuna",
        "penalty": 25,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card2": {
        "description": "dodi do starta",
        "penalty": None,
        "bonus": None,
        "move": "start",
        "jail": None
    },
    "card3": {
        "description": "idi u natrag 3 parcele",
        "penalty": None,
        "bonus": None,
        "move": -3,
        "jail": None
    },
    "card4": {
        "description": "sjebal si game drugima, duzan si svakome 50 kuna",
        "penalty": "each player: 50",
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card5": {
        "description": "servis kuce i hotela, kuca 25, hotel 100",
        "penalty": "house: 25, hotel: 100",
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card6": {
        "description": "banka ti daje 50 kuna",
        "penalty": None,
        "bonus": 50,
        "move": None,
        "jail": None
    },
    "card7": {
        "description": "kazna 25 kuna jer si zena",
        "penalty": 25,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card8": {
        "description": "edo je otiso umjesto tebe, mores van",
        "penalty": None,
        "bonus": None,
        "move": None,
        "jail": "out"
    },
    "card9": {
        "description": "idi do oregona ako predes start uzmi 200 kuna",
        "penalty": None,
        "bonus": 200,
        "move": "oregon",
        "jail": None
    },
    "card10": {
        "description": "idi do najblizeg naglaska, ako ga neko posjeduje, plati duplo",
        "penalty": "double rent if owned",
        "bonus": None,
        "move": "nearest dialect",
        "jail": None
    },
    "card11": {
        "description": "ak nisi zena, placas 50 kuna",
        "penalty": 50,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card12": {
        "description": "ak si zena placas 25 kuna",
        "penalty": 25,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card13": {
        "description": "sa edom si trazil maloljetnice ides u zatvor",
        "penalty": None,
        "bonus": None,
        "move": None,
        "jail": "in"
    },
    "card14": {
        "description": "kazna za razbijeni monitor, 25 kuna",
        "penalty": 25,
        "bonus": None,
        "move": None,
        "jail": None
    },
    "card15": {
        "description": "edo je otiso umjesto tebe, mores van",
        "penalty": None,
        "bonus": None,
        "move": None,
        "jail": "out"
    },
    "card16": {
        "description": "idi do fjordura ako predes start uzmi 200 kuna",
        "penalty": None,
        "bonus": 200,
        "move": "fjordur",
        "jail": None
    },
    "card17": {
        "description": "idi do najblizeg naglaska, ako ga neko posjeduje plati duplo",
        "penalty": "double rent if owned",
        "bonus": None,
        "move": "nearest dialect",
        "jail": None
    },
    "card18": {
        "description": "idi do najblizeg naglaska, ako ga netko posjeduje plati duplo",
        "penalty": "double rent if owned",
        "bonus": None,
        "move": "nearest dialect",
        "jail": None
    },
    "card19": {
        "description": "idi do najblizeg narjecja",
        "penalty": None,
        "bonus": None,
        "move": "nearest dialect",
        "jail": None
    },
    "card20": {
        "description": "winal si game, umjesto +29, evo ti 150 kuna",
        "penalty": None,
        "bonus": 150,
        "move": None,
        "jail": None
    }
}


def vuci_kaj_sad():
    return random.choice(list(kaj_sad_karte.values()))

def vuci_pomilovanje():
    return random.choice(list(pomilovanje_karte.values()))

def dice_roll():
    return random.randint(1, 6), random.randint(1, 6)

def load_special_fields():
    special_fields = {
        'igraj': {'name': 'Igrajj', 'bonus': 200, "type": "special"},
        'zatvor': {'name': 'Zatvor', 'penalty': 0, "type": "special"},
        'zaza': {'name': 'Free Zaza', "type": "special"},
        'id_u_zatvor': {'name': 'Edo Time', 'penalty': 20, "type": "special"}
    }
    return special_fields

def load_tax():
    tax = {
        "tax1": {"name": "Porez Bajoo", "amount": 200, "type": "tax"},
        "tax2": {"name": "HDZ Porez", "amount": 100, "type": "tax"},
    }
    return tax

def load_cards():
    cards = {
        "kaj_sad": {
            "name": "Kaj Sad?",
            "description": "Vuces kartu pa kaj bude, bude.",
            "type": "card"
        },
        "pomilovanje": {
            "name": "Pomilovanje",
            "description": "Nesto ces izvuc uglavnom",
            "type": "card"
        }
    }
    return cards

def load_dialets():
    dialets = {
        "d1": {"name": "Kajkavski naglasak", "price": 50, "rent": 2, "owner": None, "type": "dialect"},
        "d2": {"name": "Cakavski naglasak", "price": 50, "rent": 2, "owner": None, "type": "dialect"},
        "d3": {"name": "Stokavski naglasak", "price": 50, "rent": 2, "owner": None, "type": "dialect"},
        "d4": {"name": "Stakavski naglasak", "price": 50, "rent": 2, "owner": None, "type": "dialect"},
    }
    return dialets

def load_businesses():
    businesses = {
        "bs1": {"name": "Strujic", "price": 150, "rent": 4, "type": "business", "owner": None},
        "bs2": {"name": "Monster Industrija", "price": 150, "rent": 4, "type": "business", "owner": None},
    }
    return businesses

def load_fields():
    cities = {
        "br1": {"name": "Valentine", "price": 60, "rent": 2, "owner": None, "type": "city", "properties": 0, "property_cost": 50, "tier":"0"},
        "br2": {"name": "BlackWater", "price": 60, "rent": 4, "owner": None, "type": "city", "properties": 0, "property_cost": 50, "tier":"1"},
        "cy1": {"name": "Malinovka", "price": 100, "rent": 6, "owner": None, "type": "city", "properties": 0, "property_cost": 50, "tier":"2"},
        "cy2": {"name": "Himmelsdorf", "price": 100, "rent": 6, "owner": None, "type": "city", "properties": 0, "property_cost": 50, "tier":"2"},
        "cy3": {"name": "Stalingrad", "price": 120, "rent": 8, "owner": None, "type": "city", "properties": 0, "property_cost": 50, "tier":"3"},
        "pi1": {"name": "Overworld", "price": 140, "rent": 10, "owner": None, "type": "city", "properties": 0, "property_cost": 100, "tier":"4"},
        "pi2": {"name": "Nether", "price": 140, "rent": 10, "owner": None, "type": "city", "properties": 0, "property_cost": 100, "tier":"4"},
        "pi3": {"name": "The End", "price": 160, "rent": 12, "owner": None, "type": "city", "properties": 0, "property_cost": 100, "tier":"5"},
        "or1": {"name": "The Island", "price": 180, "rent": 14, "owner": None, "type": "city", "properties": 0, "property_cost": 100, "tier":"6"},
        "or2": {"name": "Fjordur", "price": 180, "rent": 14, "owner": None, "type": "city", "properties": 0, "property_cost": 100, "tier":"6"},
        "or3": {"name": "The Center", "price": 200, "rent": 16, "owner": None, "type": "city", "properties": 0, "property_cost": 100, "tier":"7"},
        "re1": {"name": "Helgen", "price": 220, "rent": 18, "owner": None, "type": "city", "properties": 0, "property_cost": 150, "tier":"8"},
        "re2": {"name": "Sovngarde", "price": 220, "rent": 18, "owner": None, "type": "city", "properties": 0, "property_cost": 150, "tier":"8"},
        "re3": {"name": "High Hrothgar", "price": 240, "rent": 20, "owner": None, "type": "city", "properties": 0, "property_cost": 150, "tier":"9"},
        "ye1": {"name": "Light Containment", "price": 260, "rent": 22, "owner": None, "type": "city", "properties": 0, "property_cost": 150, "tier":"10"},
        "ye2": {"name": "Heavy Containment", "price": 260, "rent": 22, "owner": None, "type": "city", "properties": 0, "property_cost": 150, "tier":"10"},
        "ye3": {"name": "Surface", "price": 280, "rent": 24, "owner": None, "type": "city", "properties": 0, "property_cost": 150, "tier":"11"},
        "gr1": {"name": "Coastline", "price": 300, "rent": 26, "owner": None, "type": "city", "properties": 0, "property_cost": 200, "tier":"12"},
        "gr2": {"name": "Oregon", "price": 300, "rent": 26, "owner": None, "type": "city", "properties": 0, "property_cost": 200, "tier":"12"},
        "gr3": {"name": "Lair", "price": 320, "rent": 28, "owner": None, "type": "city", "properties": 0, "property_cost": 200, "tier":"13"},
        "bl1": {"name": "Summoners Rift", "price": 350, "rent": 35, "owner": None, "type": "city", "properties": 0, "property_cost": 200, "tier":"14"},
        "bl2": {"name": "Howling Abyss", "price": 400, "rent": 50, "owner": None, "type": "city", "properties": 0, "property_cost": 200, "tier":"15"},
    }
    return cities

def load_monopoly_map(special_fields, dialets, businesses, cities, cards, tax):
    monopoly_map = {
        "1": special_fields["igraj"],
        "2": cities["br1"],
        "3": cards["pomilovanje"],
        "4": cities["br2"],
        "5": tax["tax1"],
        "6": dialets["d1"],
        "7": cities["cy1"],
        "8": cards["kaj_sad"],
        "9": cities["cy2"],
        "10": cities["cy3"],
        "11": special_fields["zatvor"],
        "12": cities["pi1"],
        "13": businesses["bs1"],
        "14": cities["pi2"],
        "15": cities["pi3"],
        "16": dialets["d2"],
        "17": cities["or1"],
        "18": cards["pomilovanje"],
        "19": cities["or2"],
        "20": cities["or3"],
        "21": special_fields["zaza"],
        "22": cities["re1"],
        "23": cards["kaj_sad"],
        "24": cities["re2"],
        "25": cities["re3"],
        "26": dialets["d3"],
        "27": cities["ye1"],
        "28": cities["ye2"],
        "29": businesses["bs2"],
        "30": cities["ye3"],
        "31": special_fields["id_u_zatvor"],
        "32": cities["gr1"],
        "33": cities["gr2"],
        "34": cards["pomilovanje"],
        "35": cities["gr3"],
        "36": dialets["d4"],
        "37": cards["kaj_sad"],
        "38": cities["bl1"],
        "39": tax["tax2"],
        "40": cities["bl2"],
    }
    return monopoly_map

def load_jail():
    global jail
    jail = {
        "jail1": {"name": "Zatvor", "penalty": 50, "type": "jail"},
        "jail2": {"name": "Zatvor", "penalty": 100, "type": "jail"},
    }
    return jail

def check_jail(player_name):
    global players
    global jail
    global jail_money

    # Find the player index by name
    player_index = None
    for index, player in players.items():
        if player['name'] == player_name:
            player_index = index
            break

    if player_index is None:
        print(f"Player {player_name} not found.")
        return False

    if player_name in jail:
        jail[player_name]['turn'] += 1
        if jail[player_name]['turn'] >= 3:
            print(f"{player_name} is released from jail.")
            players[player_index]['position'] = 10  # Or wherever they were supposed to go after jail
            jail.pop(player_name)
            return False
        print(f"{player_name} is in jail (turn {jail[player_name]['turn']}/2).")
        print(f"Do you want to pay the penalty of 20kn? (yes/no)")
        choice = input().strip().lower()
        if choice == 'yes':
            players[player_index]['money'] -= 20
            jail_money += 20
            print(f"{player_name} paid the penalty and is released from jail.")
            players[player_index]['position'] = 10
        return True
    return False

def jail_player(player, field_penalty):
    global players
    global jail_money

    if players[player]['card'] > 0:
        players[player]['card'] -= 1
        print(f"{player} used a get out of jail free card.")
        return True

    if players[player]['money'] < field_penalty:
        print("You don't have enough money to pay the penalty.")
        players[player]['position'] = 10  # Jail position
        jail[players[player]['player_name']] = {'turn': 0}
        return False
    
    print(f"{player} is in jail. You need to pay {field_penalty} to get out.")
    choice = input("Do you want to pay the penalty? (yes/no): ").strip().lower()
    if choice != 'yes':
        print("You chose not to pay the penalty. You are in jail.")
        players[player]['position'] = 10  # Jail position
        jail[players[player]['player_name']] = {'turn': 0}
        return False
    
    players[player]['money'] -= field_penalty
    jail_money += field_penalty
    print(f"{player} paid the penalty and is released from jail.")
    players[player]['position'] = 10
    return True

def load_players():
    global players
    print("Input player names, separated by commas:")
    player_names = input().split(",")
    for i, name in enumerate(player_names):
        players[i] = {"name": name.strip(), "position": 0, "money": 1500, "cards":0}

def transfer_money(player_from, player_to, amount):
    global players
    # Find the player indexes from their names
    player_from_index = None
    player_to_index = None
    for index, player in players.items():
        if player['name'] == player_from:
            player_from_index = index
        if player['name'] == player_to:
            player_to_index = index

    if player_from_index is None or player_to_index is None:
        print("Invalid player names.")
        return False

    if player_from == player_to:
        print("Cannot transfer money to yourself.")
        return False
    if amount <= 0:
        print("Amount must be positive.")
        return False
    if amount > players[player_from_index]['money']:
        print(f"{player_from} does not have enough money to transfer.")
        return False
    
    players[player_from_index]['money'] -= amount
    players[player_to_index]['money'] += amount
    print(f"{player_from} transferred {amount} to {player_to}.")
    return True

def handle_card_land(field_info, player):
    global players
    if field_info['name'] == 'Kaj Sad?':
        card = vuci_kaj_sad()
        print(f"You drew a card: {card['description']}")
        if card['penalty'] is not None:
            if player['money'] < card['penalty']:
                print("You don't have enough money to pay the penalty.")
                return False, card['penalty']
            player['money'] -= card['penalty']
            print(f"You paid {card['penalty']} penalty.")
        if card['bonus'] is not None:
            player['money'] += card['bonus']
            print(f"You received {card['bonus']} bonus.")
        if card['move'] is not None:
            if card['move'] == 'start':
                player['position'] = 0
                print("You moved to start.")
            elif card['move'] == 'nearest dialect':
                #TODO implement nearest dialect move
                pass
            elif isinstance(card['move'], int):
                pass
        if card['jail'] is not None:
            if card['jail'] == 'in':
                jail_player(player['name'])
                print(f"You are sent to jail.")
            elif card['jail'] == 'out':
                #TODO implement get out of jail free card
                player['cards'] += 1 
                print("You get a free get out of jail card.")
    elif field_info['name'] == 'Pomilovanje':
        card = vuci_pomilovanje()
        print(f"You drew a card: {card['description']}")
        if card['penalty'] is not None:
            if player['money'] < card['penalty']:
                print("You don't have enough money to pay the penalty.")
                return False, card['penalty']
            player['money'] -= card['penalty']
            print(f"You paid {card['penalty']} penalty.")
        if card['bonus'] is not None:
            player['money'] += card['bonus']
            print(f"You received {card['bonus']} bonus.")
        if card['move'] is not None:
            if card['move'] == 'start':
                player['position'] = 0
                print("You moved to start.")
            elif card['move'] == 'nearest dialect':
                #TODO implement nearest dialect move
                pass
            elif isinstance(card['move'], int):
                player['position'] += card['move']
                print(f"You moved {card['move']} spaces.")
        if card['jail'] == 'in':
            jail_player(player['name'])
            print(f"You are sent to jail.")
        elif card['jail'] == 'out':
            #TODO implement get out of jail free card
            player['cards'] += 1
            print("You get a free get out of jail card.")
    return True

def handle_special_field(field_info, player):
    global jail_money
    if field_info['name'] == 'Igrajj':
        pass
    elif field_info['name'] == 'Zatvor':
        pass
    elif field_info['name'] == 'Edo Time':
        return jail_player(player, field_info['penalty'])
    elif field_info['name'] == 'Free Zaza':
        player['money'] += jail_money
        print(f"You received {jail_money} from the bank.")
        jail_money = 0
    return True

def handle_tax(field_info, player):
    if player['money'] < field_info['amount']:
        print("You don't have enough money to pay the tax.")
        return False, field_info['amount']
    player['money'] -= field_info['amount']
    print(f"You paid {field_info['amount']} in taxes.")
    return True

def handle_dialect(field_info, player):
    if field_info["owner"] is None:
        if player['money'] < field_info['price']:
            print("You don't have enough money to buy this dialect.")
            return True
        print(f"You can buy {field_info['name']} for {field_info['price']}.")
        choice = input("Do you want to buy it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("You chose not to buy the dialect.")
            return True
        player['money'] -= field_info['price']
        field_info["owner"] = player["name"]
        print(f"You bought {field_info['name']} for {field_info['price']}")
    else:
        if field_info["owner"] == player["name"]:
            print("You already own this dialect.")
            return True
        #TODO  ----VALJDA RADI??--- prvobitno promjenit kolicinu rente bazno, zatim implementat da se provjeri koliko biznisa posjeduje da se renta povecava.
        rent = field_info['rent']
        if player['money'] < rent:
            print("You don't have enough money to pay the rent.")
            return False, field_info['rent']
        transfer_money(player["name"], field_info["owner"], rent)
        return True

def handle_business(field_info, player, dice_rolled):
    if field_info["owner"] is None:
        if player['money'] < field_info['price']:
            print("You don't have enough money to buy this property.")
            return True
        print(f"You can buy {field_info['name']} for {field_info['price']}.")
        choice = input("Do you want to buy it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("You chose not to buy the property.")
            return True
        player['money'] -= field_info['price']
        field_info["owner"] = player["name"]
        print(f"You bought {field_info['name']} for {field_info['price']}")
        return True
    else:
        if field_info["owner"] == player["name"]:
            print("You already own this property.")
            return True
        rent = field_info['rent'] * dice_rolled
        if player['money'] < rent:
            print("You don't have enough money to pay the rent.")
            return False, rent
        transfer_money(player["name"], field_info["owner"], rent)
        print(f"You paid {rent} rent to {field_info['owner']}")
        return True

def handle_city(field_info, player, monopoly_map, field_key):
    if field_info["owner"] is None:
        if player['money'] < field_info['price']:
            print("You don't have enough money to buy this property.")
            return True
        print(f"You can buy {field_info['name']} for {field_info['price']}.")
        choice = input("Do you want to buy it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("You chose not to buy the property.")
            return True
        player['money'] -= field_info['price']
        field_info["owner"] = player["name"]
        print(f"You bought {field_info['name']} for {field_info['price']}")
        return True
    else:
        if field_info["owner"] == player["name"]:
            print("You already own this property.")
            prefix = field_key[:2]  # how you define the prefix depends on your map

            #TODO DEBUG THIS ITS NOT WORKING CORRECTLY!
            for key, value in monopoly_map.items():
                if key.startswith(prefix):
                    if value.get("owner") != player["name"]:
                        return False
                    
            print(f"This property has {field_info['properties']} properties.")
            if field_info['properties'] < 5:
                upgrade_cost = field_info['property_cost']
                if player['money'] < upgrade_cost:
                    print("You don't have enough money to upgrade this property.")
                    return True
                choice = input(f"Do you want to upgrade this property for {upgrade_cost}? (yes/no): ").strip().lower()
                if choice == 'yes':
                    player['money'] -= upgrade_cost
                    field_info['properties'] += 1
                    print(f"You upgraded {field_info['name']} to {field_info['properties']} properties.")
            else:
                print("This property has a hotel!")
            return True
        if field_info["properties"] > 0:
            rent = upgrade_tiers[field_info['tier']][field_info['properties']]
        else:
            rent = field_info['rent']
        if player['money'] < rent:
            print("You don't have enough money to pay the rent.")
            return False, rent
        transfer_money(player["name"], field_info["owner"], rent)
        print(f"You paid {rent} rent to {field_info['owner']}")
        return True

def handle_no_money(player, owed, monpoly_map):
    global players
    if player['money'] < owed:
        print(f"{player['name']} is bankrupt!")
        #TODO implement bankruptcy logic here
        return False
    return True

def start_game(monopoly_map):
    global players
    load_players()
    current_player = 0
    while True:
        print(f"{players[current_player]['name']}'s turn.")
        print(f"Current position: {players[current_player]['position']}")
        print(f"Current balance: {players[current_player]['money']}kn")
        input("Press Enter to roll the dice.")
        old_position = players[current_player]['position']
        roll1, roll2 = dice_roll()
        roll = roll1 + roll2

        if check_jail(players[current_player]['name']):
            print(f"{players[current_player]['name']} is in jail.")
            if roll1 == roll2:
                print(f"{players[current_player]['name']} rolled doubles and is released from jail.")
                players[current_player]['position'] = 10
            else:
                current_player = (current_player + 1) % len(players)
                continue

        print(f"You rolled a {roll}.")
        players[current_player]['position'] = (players[current_player]['position'] + roll) % len(monopoly_map)
        field_index = players[current_player]['position']
        field_info = monopoly_map[str(field_index + 1)]
        field_key = str(field_index + 1)
        
        new_position = players[current_player]['position']
        if old_position > new_position:
            print(f"You passed start! You receive 200.")
            players[current_player]['money'] += 200

        print(f"You landed on {field_info['name']}")
        if field_info['type'] == 'special':
            result = handle_special_field(field_info, players[current_player])
        elif field_info['type'] == 'tax':
            result = handle_tax(field_info, players[current_player])
        elif field_info['type'] == 'dialect':
            result = handle_dialect(field_info, players[current_player])
        elif field_info['type'] == 'business':
            result = handle_business(field_info, players[current_player], roll)
        elif field_info['type'] == 'city':
            result = handle_city(field_info, players[current_player], monopoly_map, field_key)
        elif field_info['type'] == 'card':
            result = handle_card_land(field_info, players[current_player])
        else:
            print("Unknown field type.")

        if isinstance(result, tuple):
            status = result[0]
            penalty = result[1]
            if not status:
                print(f"You don't have enough money to pay the penalty of {penalty}.")
                if not handle_no_money(players[current_player], penalty, monopoly_map):
                    players.pop(current_player)
                    print(f"{players[current_player]['name']} is bankrupt!")
                continue

        # Handle field actions here (buy, pay rent, etc.)
        print(f"Your current balance: {players[current_player]['money']}")
        print("Press Enter to end your turn.")
        input()
        current_player = (current_player + 1) % len(players)


def main():
    # Load all game components
    special_fields = load_special_fields()
    tax = load_tax()
    cards = load_cards()
    dialets = load_dialets()
    businesses = load_businesses()
    cities = load_fields()

    # Create the monopoly map
    monopoly_map = load_monopoly_map(special_fields, dialets, businesses, cities, cards, tax)

    # Example of how to access a field
    start_game(monopoly_map)
    

if __name__ == "__main__":
    main()