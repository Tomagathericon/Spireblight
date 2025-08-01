from unittest import TestCase

from datetime import datetime, UTC
import json
import os

from src.save import Savefile, get_savefile, _savefile as s
from src.runs import RunParser

# TODO: make profiles work for testing

# BEGIN SETUP

# this cannot be part of a class setup, as I only want it to be done once
# technically, I *could* have it setup once each time, but there's no need to

import asyncio, src.events as events

asyncio.run(events.invoke("setup_init"))

wa = streamer = None

# this is an older save, and doesn't have all the RHP features
# this is actually good, as it lets us test for what happens when it's lacking
with open(os.path.join("test", "static", "dummy_savefile.json")) as f:
    s.update_data(json.load(f), "THE_SILENT", "false")

# this is more recent, and should have all the fields we care about
# (at least as of June 2025. we all know how these things go)

# this save and the run file that follow are from the save run, and thus should match closely
with open(os.path.join("test", "static", "save_matched.json")) as f:
    sm = Savefile(_debug=True)
    sm.update_data(json.load(f), "IRONCLAD", "false")

with open(os.path.join("test", "static", "run_matched.json")) as f:
    rm = RunParser("run_matched.json", 0, json.load(f))

with open(os.path.join("test", "static", "watcher.json")) as f:
    wa = RunParser("watcher.json", 0, json.load(f))

with open(os.path.join("test", "static", "slay_the_streamer.json")) as f:
    streamer = RunParser("slay_the_streamer.json", 2, json.load(f))

assert wa is not None and streamer is not None, "could not load test run files"

# END SETUP

_rooms_mapping = {
    "Enemy": "M",
    "Unknown (Enemy)": "m",
    "Treasure": "T",
    "Unknown (Treasure)": "t",
    "Elite": "E",
    "Unknown (Elite)": "e",
    "Unknown": "?",
    "Unknown (Bugged)": "?",
    "Unknown (Ambiguous)": "?",
    "Merchant": "$",
    "Unknown (Merchant)": "S",
    "Rest Site": "R",
    "Boss": "B",
    "Boss Chest": "C",
    "Transition into Act 4": "4",
    "Victory!": "V",
}

class _save_contents:
    relics = [
    ("Ring of the Snake", 0, "\nCards drawn: 42\nPer turn: 0.48\nPer combat: 2.00"),
    ("Happy Flower", 3, "\nEnergy gained: 26\nPer turn: 0.33\nPer combat: 1.37"),
    ("Twisted Funnel", 3, ""),
    ("Omamori", 7, "\nCharges used: 0"),
    ("Orichalcum", 9, "\nBlock gained: 168\nPer turn: 2.37\nPer combat: 9.88"),
    ("Oddly Smooth Stone", 11, ""),
    ("Astrolabe", 17, "\nCards obtained: \n- Envenom\n- Concentrate\n- Quick Slash"),
    ("Red Mask", 24, ""),
    ("Vajra", 26, ""),
    ("The Courier", 27, ""),
    ("Toolbox", 29, ""),
    ("Toy Ornithopter", 29, "\nHP healed: 10"),
    ("Art of War", 30, "\nEnergy gained: 4\nPer turn: 0.15\nPer combat: 0.67"),
    ("Girya", 31, "\nTimes lifted: 2"),
    ("Molten Egg", 31, ""),
    ("Empty Cage", 34, ""),
    ("Torii", 36, "\nDamage prevented: 0"), # lol
    ("Centennial Puzzle", 41, "\nCards drawn: 0\nPer turn: 0.00\nPer combat: 0.00"),
    ]
    rooms = [
    "M",
    "M",
    "$",
    "M",
    "?",
    "R",
    "E",
    "R",
    "T",
    "R",
    "E",
    "M",
    "m",
    "M",
    "R",
    "B",
    "C",
    "M",
    "M",
    "?",
    "?",
    "m",
    "R",
    "?",
    "R",
    "T",
    "E",
    "R",
    "$",
    "E",
    "?",
    "R",
    "B",
    "C",
    "M",
    "?",
    "S",
    "M",
    "$",
    "R",
    "E",
    "R",
    "T",
    "R",
    "?"
    ]
    current_hp = [
    58,
    54,
    54,
    47,
    47,
    47,
    35,
    35,
    35,
    35,
    18,
    18,
    18,
    18,
    18,
    18,
    50,
    40,
    40,
    40,
    70,
    61,
    61,
    56,
    56,
    56,
    54,
    54,
    54,
    51,
    46,
    46,
    19,
    57,
    56,
    56,
    56,
    56,
    56,
    56,
    32,
    32,
    32,
    32,
    32
    ]
    max_hp = [
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    60,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70,
    70
    ]
    gold = [
    360,
    379,
    1,
    14,
    14,
    14,
    46,
    46,
    101,
    101,
    132,
    151,
    164,
    183,
    183,
    262,
    262,
    240,
    255,
    255,
    255,
    271,
    271,
    304,
    304,
    327,
    355,
    355,
    12,
    37,
    157,
    157,
    232,
    232,
    252,
    252,
    103,
    117,
    54,
    54,
    85,
    85,
    85,
    85,
    85
    ]
    potions = [
    [],
    ["Cunning Potion"],
    [],
    ["Colorless Potion"],
    [],
    [],
    [],
    [],
    [],
    [],
    ["Essence of Steel"],
    ["Colorless Potion"],
    ["Distilled Chaos"],
    [],
    [],
    ["Attack Potion"],
    [],
    [],
    ["Cultist Potion"],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ["Power Potion"],
    [],
    [],
    ["Attack Potion"],
    [],
    [],
    [],
    [],
    ["Flex Potion"],
    [],
    ["Ghost in a Jar"],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ]
    potions_use = [
    [],
    [],
    [],
    [],
    [],
    [],
    ["Colorless Potion"],
    [],
    [],
    [],
    ["Cunning Potion"],
    [],
    [],
    [],
    [],
    ["Colorless Potion", "Distilled Chaos"],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ["Attack Potion"],
    [],
    [],
    ["Power Potion"],
    [],
    [],
    ["Cultist Potion"],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ]
    picked = [
    ['Deadly Poison'],
    ['Flying Knee'],
    ['Crippling Cloud'],
    ['Dagger Spray'],
    [],
    [],
    ['After Image'],
    [],
    [],
    [],
    ['Poisoned Stab'],
    [],
    ['Masterful Stab'],
    ['Calculated Gamble'],
    [],
    ['Die Die Die'],
    [],
    [],
    ['Piercing Wail'],
    [],
    [],
    [],
    [],
    ['Piercing Wail'],
    [],
    [],
    ['Expertise'],
    [],
    ['Acrobatics'],
    [],
    [],
    [],
    ['Adrenaline'],
    [],
    ['Deflect+'],
    [],
    ['Eviscerate+'],
    [],
    ['Footwork'],
    [],
    ['Backflip'],
    [],
    [],
    [],
    [],
    ]
    skipped = [ # should this include not-bought stuff? probably not...
    ['Dodge and Roll', 'Cloak and Dagger'],
    ['Piercing Wail', 'Dodge and Roll'],
    [],
    ['Flechettes', 'Masterful Stab'],
    [],
    [],
    ['Quick Slash', 'Slice'],
    [],
    [],
    [],
    ['Dagger Throw', 'Dodge and Roll'],
    ['Poisoned Stab', 'Dodge and Roll', 'All-Out Attack'],
    ['Blur', 'Footwork'],
    ['Infinite Blades', 'Bouncing Flask'],
    [],
    ['Unload', 'Grand Finale'],
    [],
    [],
    ['Eviscerate', 'Poisoned Stab'],
    [],
    [],
    ['Sneaky Strike', 'Blade Dance', 'Choke+'],
    [],
    ['Endless Agony', 'Choke'],
    [],
    [],
    ['Endless Agony', 'Flechettes'],
    [],
    [],
    ['Dagger Throw', 'Eviscerate', 'Masterful Stab+'],
    [],
    [],
    ['Grand Finale+', 'Phantasmal Killer'],
    [],
    ['Accuracy+', 'Endless Agony+'],
    [],
    [],
    [],
    [],
    [],
    ['Prepared', 'Bane+'],
    [],
    [],
    [],
    [],
    ]
    skipped_relics = [ # this run only skipped boss relics; need to check another run for other skipped relics
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ['Hovering Kite', "Slaver's Collar"],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ['Runic Dome', 'Snecko Eye'],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ]
    skipped_potions = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    ['Flex Potion'],
    [],
    [],
    ['Blessing of the Forge'],
    [],
    [],
    [],
    [],
    ]
    card_count = [
        14,
        15,
        16,
        17,
        16,
        16,
        17,
        17,
        17,
        17,
        18,
        18,
        19,
        20,
        20,
        21,
        21,
        21,
        22,
        22,
        21,
        21,
        21,
        22,
        22,
        22,
        23,
        23,
        23,
        23,
        23,
        23,
        24,
        24,
        25,
        25,
        26,
        26,
        27,
        27,
        28,
        28,
        28,
        28,
        29,
    ]
    relic_count = [
        1,
        1,
        3,
        3,
        3,
        3,
        4,
        4,
        5,
        5,
        6,
        6,
        6,
        6,
        6,
        6,
        7,
        7,
        7,
        7,
        7,
        7,
        7,
        8,
        8,
        9,
        10,
        10,
        12,
        13,
        15,
        15,
        15,
        16,
        16,
        17,
        17,
        17,
        17,
        17,
        18,
        18,
        18,
        18,
        18,
    ]
    potion_count = [
        0,
        1,
        1,
        2,
        2,
        2,
        1,
        1,
        1,
        1,
        1,
        2,
        3,
        3,
        3,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        2,
        2,
        3,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
    ]
    fights_count = [
        1,
        2,
        2,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        6,
        7,
        8,
        8,
        9,
        9,
        10,
        11,
        11,
        11,
        12,
        12,
        13,
        13,
        13,
        14,
        14,
        14,
        15,
        17,
        17,
        18,
        18,
        19,
        19,
        19,
        20,
        20,
        20,
        21,
        21,
        21,
        21,
        21,
    ]
    turns_count = [
        5,
        9,
        9,
        12,
        12,
        12,
        17,
        17,
        17,
        17,
        21,
        23,
        26,
        29,
        29,
        36,
        36,
        40,
        43,
        43,
        43,
        49,
        49,
        52,
        52,
        52,
        55,
        55,
        55,
        61,
        67,
        67,
        75,
        75,
        78,
        78,
        78,
        80,
        80,
        80,
        88,
        88,
        88,
        88,
        88,
    ]
    boss_relics = [
        ("Astrolabe", ('Hovering Kite', "Slaver's Collar")),
        ("Empty Cage", ('Runic Dome', 'Snecko Eye')),
    ]

class _matched_contents:
    relics = [
        ("Burning Blood", 0, "\nHP healed: 147"),
        ("Neow's Lament", 0, ""),
        ("Ornamental Fan", 3, "\nBlock gained: 68\nPer turn: 0.62\nPer combat: 2.72"),
        ("Vajra", 5, ""),
        ("Bottled Tornado", 6, "\nCard bottled: Feel No Pain"),
        ("Blue Candle", 8, "\nCurses exhausted: 1\nPer turn: 0.01\nPer combat: 0.05"),
        ("Whetstone", 9, "\nCards upgraded: \n- Twin Strike\n- Bash"),
        ("Horn Cleat", 11, ""),
        ("Preserved Insect", 12, "\nHP removed: 298"),
        ("Mark of Pain", 17, ""),
        ("Orichalcum", 23, "\nBlock gained: 24\nPer turn: 0.45\nPer combat: 2.00"),
        ("Happy Flower", 25, "\nEnergy gained: 16\nPer turn: 0.33\nPer combat: 1.45"),
        ("Mummified Hand", 26, "\nEnergy discounted: 43\nPer turn: 0.90\nPer combat: 3.91"),
        ("Singing Bowl", 29, "\nMax HP gained: 6"),
        ("Empty Cage", 34, ""),
        ("Prismatic Shard", 37, ""),
        ("Art of War", 40, "\nEnergy gained: 2\nPer turn: 0.12\nPer combat: 0.50"),
        ("Letter Opener", 44, "\nDamage dealt: 17\nPer turn: 1.89\nPer combat: 8.50"),
        ("Nunchaku", 46, "\nEnergy gained: 0\nPer turn: 0.00\nPer combat: 0.00"),
        ("Centennial Puzzle", 47, "\nCards drawn: 3\nPer turn: 0.75\nPer combat: 3.00"),
        ("Clockwork Souvenir", 47, ""),
    ]
    rooms = [
        "M",
        "?",
        "t",
        "M",
        "$",
        "E",
        "M",
        "E",
        "T",
        "R",
        "E",
        "?",
        "R",
        "M",
        "R",
        "B",
        "C",
        "M",
        "M",
        "M",
        "$",
        "M",
        "E",
        "R",
        "E",
        "T",
        "R",
        "?",
        "E",
        "M",
        "M",
        "R",
        "B",
        "C",
        "M",
        "S",
        "$",
        "?",
        "M",
        "E",
        "M",
        "R",
        "T",
        "E",
        "R",
        "E",
        "$",
        "M",
        "R",
    ]
    current_hp = [
        74,
        63,
        63,
        69,
        69,
        75,
        75,
        60,
        60,
        60,
        64,
        49,
        49,
        53,
        53,
        17,
        61,
        58,
        64,
        70,
        70,
        57,
        49,
        49,
        70,
        70,
        70,
        70,
        75,
        68,
        65,
        65,
        54,
        71,
        79,
        79,
        79,
        79,
        79,
        66,
        71,
        71,
        71,
        79,
        79,
        74,
        74,
        73,
        73,
    ]
    max_hp = [
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        77,
        77,
        77,
        77,
        77,
        79,
        79,
        79,
        79,
        79,
        79,
        79,
        79,
        79,
        81,
        81,
        81,
        81,
        81,
        81,
    ]
    gold = [
        111,
        186,
        266,
        284,
        26,
        58,
        75,
        109,
        109,
        109,
        134,
        189,
        189,
        200,
        200,
        276,
        276,
        288,
        307,
        320,
        171,
        189,
        218,
        218,
        244,
        244,
        244,
        444,
        477,
        490,
        503,
        503,
        582,
        582,
        593,
        493,
        332,
        332,
        352,
        377,
        397,
        397,
        422,
        456,
        456,
        483,
        61,
        77,
        77,
    ]
    potions = [
        [],
        [],
        [],
        [],
        [],
        ["Essence of Steel"],
        ["Skill Potion"],
        [],
        [],
        [],
        [],
        ["Blood Potion"],
        [],
        ["Flex Potion"],
        [],
        [],
        [],
        ["Strength Potion"],
        [],
        [],
        [],
        [],
        ["Swift Potion"],
        [],
        ["Swift Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Gambler's Brew"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Gambler's Brew"],
        [],
    ]
    potions_use = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Essence of Steel", "Skill Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Flex Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Strength Potion"],
        [],
        ["Blood Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Swift Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Swift Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    picked = [
        ["Feel No Pain"],
        [],
        [],
        ["Twin Strike"],
        ["Discovery"],
        ["Metallicize"],
        ["Battle Trance"],
        ["True Grit"],
        [],
        [],
        ["Sever Soul"],
        ["Fiend Fire"],
        [],
        ["Headbutt"],
        [],
        ["Juggernaut"],
        [],
        ["Shrug It Off"],
        ["Burning Pact"],
        ["Impervious"],
        ["Reckless Charge"],
        ["Power Through"],
        [],
        [],
        ["Warcry"],
        [],
        [],
        [],
        ["Disarm"],
        ["Singing Bowl"],
        ["Dark Embrace"],
        [],
        ["Immolate"],
        [],
        ["Singing Bowl"],
        [],
        [],
        [],
        ["Third Eye"],
        ["Purity"],
        ["Backflip"],
        [],
        [],
        ["Singing Bowl"],
        [],
        ["Panic Button+"],
        ["Dark Embrace"],
        ["Sentinel"],
        [],
    ]
    skipped = [
        ["Sword Boomerang", "True Grit"],
        [],
        [],
        ["Combust", "Flex"],
        [],
        ["Perfected Strike", "Carnage"],
        ["Perfected Strike", "Bloodletting"],
        ["Sentinel", "Rage"],
        [],
        [],
        ["Entrench", "Flex"],
        ["Pommel Strike", "True Grit"],
        [],
        ["Sever Soul", "Dropkick"],
        [],
        ["Fiend Fire", "Exhume"],
        [],
        ["Havoc", "Body Slam"],
        ["Thunderclap", "Headbutt"],
        ["Iron Wave", "Combust"],
        [],
        ["Flex", "Wild Strike"],
        ["Flex", "Sever Soul", "Thunderclap"],
        [],
        ["Heavy Blade", "Clothesline"],
        [],
        [],
        [],
        ["Shrug It Off", "Seeing Red"],
        ["Clothesline", "Reckless Charge+", "Warcry"],
        ["Pommel Strike", "True Grit"],
        [],
        ["Limit Break", "Demon Form"],
        [],
        ["Havoc", "Twin Strike+", "Rampage"],
        [],
        [],
        [],
        ["Sever Soul", "All-Out Attack"],
        ["Iron Wave", "Battle Hymn"],
        ["Wreath of Flame", "Prostrate"],
        [],
        [],
        ["Recursion+", "Crush Joints+", "Cut Through Fate"],
        [],
        ["Sneaky Strike", "White Noise"],
        [],
        ["Leap", "Ragnarok"],
        [],
    ]
    skipped_relics = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Astrolabe", "Ectoplasm"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Coffee Dripper", "Runic Cube"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    skipped_potions = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Flex Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ["Attack Potion"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    card_count = [
        12,
        12,
        12,
        13,
        14,
        15,
        16,
        17,
        17,
        17,
        18,
        19,
        19,
        20,
        20,
        21,
        21,
        22,
        23,
        24,
        24,
        25,
        25,
        25,
        26,
        26,
        26,
        26,
        27,
        28,
        29,
        29,
        30,
        30,
        31,
        30,
        30,
        30,
        31,
        32,
        33,
        33,
        33,
        34,
        34,
        35,
        36,
        37,
        37,
    ]
    relic_count = [
        2,
        2,
        3,
        3,
        4,
        5,
        5,
        6,
        7,
        7,
        8,
        9,
        9,
        9,
        9,
        9,
        10,
        10,
        10,
        10,
        10,
        10,
        11,
        11,
        12,
        13,
        13,
        13,
        14,
        14,
        14,
        14,
        14,
        15,
        15,
        15,
        16,
        16,
        16,
        17,
        17,
        17,
        17,
        18,
        18,
        19,
        21,
        21,
        21,
    ]
    potion_count = [
        0,
        0,
        0,
        0,
        0,
        1,
        2,
        0,
        0,
        0,
        0,
        1,
        1,
        2,
        2,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
    ]
    fights_count = [
        1,
        1,
        1,
        2,
        2,
        3,
        4,
        5,
        5,
        5,
        6,
        7,
        7,
        8,
        8,
        9,
        9,
        10,
        11,
        12,
        12,
        13,
        14,
        14,
        15,
        15,
        15,
        15,
        16,
        17,
        18,
        18,
        19,
        19,
        20,
        20,
        20,
        20,
        21,
        22,
        23,
        23,
        23,
        24,
        24,
        25,
        25,
        26,
        26,
    ]
    turns_count = [
        1,
        1,
        1,
        2,
        2,
        3,
        7,
        11,
        11,
        11,
        23,
        27,
        27,
        30,
        30,
        38,
        38,
        41,
        47,
        50,
        50,
        55,
        58,
        58,
        63,
        63,
        63,
        63,
        66,
        69,
        73,
        73,
        80,
        80,
        84,
        84,
        84,
        84,
        90,
        95,
        99,
        99,
        99,
        102,
        102,
        107,
        107,
        111,
        111,
    ]
    boss_relics = [
        ("Mark of Pain", ("Astrolabe", "Ectoplasm")),
        ("Empty Cage", ("Coffee Dripper", "Runic Cube")),
    ]

class _run_contents:
    boss_relics = [
        ("Astrolabe", ("Pandora's Box", "Philosopher's Stone")),
        ("Slaver's Collar", ("Black Star", "Violet Lotus")),
    ]

class _streamer_contents:
    boss_relics = [
        ("Velvet Choker", ("Tiny House", "Runic Pyramid")),
        ("Runic Dome", ("Calling Bell", "Cursed Key")),
    ]

class TestFileParser(TestCase):
    def test_character(self):
        self.assertEqual(s.character, "Silent")
        self.assertEqual(sm.character, "Ironclad")
        self.assertEqual(rm.character, "Ironclad")
        self.assertEqual(wa.character, "Watcher")

    def test_modded(self):
        self.assertFalse(s.modded)

    def test_seed(self):
        self.assertEqual(s.seed, "57Z3V6XL40NZS")
        self.assertEqual(sm.seed, rm.seed)

    def test_seeded(self):
        self.assertFalse(s.is_seeded)
        self.assertFalse(sm.is_seeded)
        self.assertFalse(rm.is_seeded)
        self.assertFalse(wa.is_seeded)

    def test_timestamp(self):
        self.assertEqual(s.timestamp, datetime(2022, 5, 3, 20, 14, 30, 317000, tzinfo=UTC))
        self.assertEqual(wa.timestamp, datetime(2023, 6, 16, 20, 34, 58, tzinfo=UTC))
        self.assertEqual(streamer.timestamp, datetime(2023, 7, 12, 20, 9, 44, tzinfo=UTC))

    def test_boss_relics(self):
        for fp, contents in ( (s, _save_contents), (sm, _matched_contents), (rm, _matched_contents), (wa, _run_contents), (streamer, _streamer_contents) ):
            relics = fp.boss_relics
            res = []
            for picked, skipped in relics:
                skip = tuple(x.name for x in skipped)
                res.append( (picked.name, skip) )
            self.assertEqual(res, contents.boss_relics)

class TestSavefile(TestCase):
    def test_debug_only(self):
        with self.assertRaises(RuntimeError):
            Savefile()

    def test_getsave(self):
        self.assertIs(get_savefile(), s)
        self.assertIsNot(get_savefile(), sm)

    def test_timedelta(self):
        self.assertEqual(s.timedelta.seconds, 3379)
        self.assertEqual(sm.timedelta.seconds, 4258)

    def test_display_name(self):
        self.assertEqual(s.display_name, "Current Silent run")
        self.assertEqual(sm.display_name, "Current Ironclad run")

    def test_in_game(self):
        self.assertTrue(s.in_game)
        self.assertTrue(sm.in_game)

    def test_keys(self):
        k = s.keys
        self.assertTrue(k.ruby_key_obtained)
        self.assertTrue(k.emerald_key_obtained)
        self.assertTrue(k.sapphire_key_obtained)

        self.assertEqual(k.ruby_key_floor, 42)
        self.assertEqual(k.sapphire_key_floor, 43)

    def test_keys2(self):
        k = sm.keys
        self.assertTrue(k.ruby_key_obtained)
        self.assertTrue(k.emerald_key_obtained)
        self.assertTrue(k.sapphire_key_obtained)

        self.assertEqual(k.ruby_key_floor, 45)
        self.assertEqual(k.emerald_key_floor, 6)
        self.assertEqual(k.sapphire_key_floor, 43)

    def test_current_health(self):
        self.assertEqual(s.current_health, 32)
        self.assertEqual(sm.current_health, 73)

    def test_max_health(self):
        self.assertEqual(s.max_health, 70)
        self.assertEqual(sm.max_health, 81)

    def test_gold(self):
        self.assertEqual(s.current_gold, 85)
        self.assertEqual(sm.current_gold, 77)

class TestRunParser(TestCase):
    def test_won(self):
        self.assertTrue(wa.won)
        self.assertFalse(streamer.won)

    def test_keys(self):
        k = wa.keys
        self.assertTrue(k.ruby_key_obtained)
        self.assertTrue(k.emerald_key_obtained)
        self.assertTrue(k.sapphire_key_obtained)

        self.assertEqual(k.ruby_key_floor, 41)
        self.assertEqual(k.emerald_key_floor, 10)
        self.assertEqual(k.sapphire_key_floor, 26)

class TestRelicData(TestCase):
    def test_save(self):
        relics = zip(s.relics, _save_contents.relics, strict=True)
        for relic, (name, floor, details) in relics:
            self.assertEqual(relic.name, name)
            self.assertEqual(relic.description(), f"Obtained on floor {floor}{details}")

    def test_matched(self):
        relics = zip(sm.relics, rm.relics[:21], _matched_contents.relics, strict=True)
        for s_relic, r_relic, (name, floor, details) in relics:
            self.assertEqual(s_relic.name, name)
            self.assertEqual(s_relic.description(), f"Obtained on floor {floor}{details}")
            self.assertEqual(s_relic.relic, r_relic.relic)

class TestPath(TestCase):
    def test_length(self):
        self.assertEqual(len(s.path), 45)
        self.assertEqual(len(wa.path), 57)
        self.assertEqual(len(streamer.path), 50)

    def test_streamer(self):
        # Slay the Streamer has a weird thing after the chest
        self.assertEqual(streamer.path[8].floor, 9)
        self.assertEqual(streamer.path[9].floor, 11)

    def test_current_hp(self):
        self.assertEqual([x.current_hp for x in s.path], s.current_hp_counts[1:])
        self.assertEqual([x.current_hp for x in wa.path][:-1], wa.current_hp_counts[1:])
        # slay the streamer kinda breaks this

    def test_max_hp(self):
        self.assertEqual([x.max_hp for x in s.path], s.max_hp_counts[1:])
        self.assertEqual([x.max_hp for x in wa.path][:-1], wa.max_hp_counts[1:])

    def test_gold(self):
        self.assertEqual([x.gold for x in s.path], s.gold_counts[1:])
        self.assertEqual([x.gold for x in wa.path][:-1], wa.gold_counts[1:])

class TestNodeSave(TestCase):
    def test_room_type(self):
        path = zip(s.path, _save_contents.rooms, strict=True)
        for node, short in path:
            self.assertEqual(_rooms_mapping[node.room_type], short)

    def test_current_hp(self):
        path = zip(s.path, _save_contents.current_hp, strict=True)
        for node, hp in path:
            self.assertEqual(node.current_hp, hp)

    def test_max_hp(self):
        path = zip(s.path, _save_contents.max_hp, strict=True)
        for node, hp in path:
            self.assertEqual(node.max_hp, hp)

    def test_gold(self):
        path = zip(s.path, _save_contents.gold, strict=True)
        for node, gold in path:
            self.assertEqual(node.gold, gold)

    def test_floor(self):
        self.assertEqual(s.neow_bonus.floor, 0)
        floor = 1
        for node in s.path:
            self.assertEqual(node.floor, floor)
            floor += 1
        self.assertEqual(floor, 46)

    def test_potions(self):
        path = zip(s.path, _save_contents.potions, strict=True)
        for node, potions in path:
            self.assertEqual([x.name for x in node.potions], potions)

    def test_used_potions(self):
        path = zip(s.path, _save_contents.potions_use, strict=True)
        for node, used in path:
            self.assertEqual([x.name for x in node.used_potions], used)

    def test_picked(self):
        path = zip(s.path, _save_contents.picked, strict=True)
        for node, picked in path:
            self.assertEqual([x.name for x in node.picked], picked)

    def test_skipped(self):
        path = zip(s.path, _save_contents.skipped, strict=True)
        for node, skipped in path:
            self.assertEqual([x.name for x in node.skipped], skipped)

    def test_skipped_relics(self):
        path = zip(s.path, _save_contents.skipped_relics, strict=True)
        for node, skipped in path:
            self.assertEqual([x.name for x in node.skipped_relics], skipped)

    def test_skipped_potions(self):
        path = zip(s.path, _save_contents.skipped_potions, strict=True)
        for node, skipped in path:
            self.assertEqual([x.name for x in node.skipped_potions], skipped)

    def test_card_count(self):
        path = zip(s.path, _save_contents.card_count, strict=True)
        for node, count in path:
            self.assertEqual(node.card_count, count)

    def test_relic_count(self):
        path = zip(s.path, _save_contents.relic_count, strict=True)
        for node, count in path:
            self.assertEqual(node.relic_count, count)

    def test_potion_count(self):
        path = zip(s.path, _save_contents.potion_count, strict=True)
        for node, count in path:
            self.assertEqual(node.potion_count, count)

    def test_fights_count(self):
        path = zip(s.path, _save_contents.fights_count, strict=True)
        for node, count in path:
            self.assertEqual(node.fights_count, count)

    def test_turns_count(self):
        path = zip(s.path, _save_contents.turns_count, strict=True)
        for node, count in path:
            self.assertEqual(node.turns_count, count)

class TestNodeMatched(TestCase):
    def test_room_type(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.rooms, strict=True)
        for save, run, short in path:
            self.assertEqual(_rooms_mapping[save.room_type], short)
            self.assertEqual(save.room_type, run.room_type)

    def test_current_hp(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.current_hp, strict=True)
        for save, run, hp in path:
            self.assertEqual(save.current_hp, hp)
            self.assertEqual(save.current_hp, run.current_hp)

    def test_max_hp(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.max_hp, strict=True)
        for save, run, hp in path:
            self.assertEqual(save.max_hp, hp)
            self.assertEqual(save.max_hp, run.max_hp)

    def test_gold(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.gold, strict=True)
        for save, run, gold in path:
            self.assertEqual(save.gold, gold)
            self.assertEqual(save.gold, run.gold)

    def test_potions(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.potions, strict=True)
        for save, run, potions in path:
            self.assertEqual([x.name for x in save.potions], potions)
            self.assertEqual(save.potions, run.potions)

    def test_used_potions(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.potions_use, strict=True)
        for save, run, used in path:
            self.assertEqual([x.name for x in save.used_potions], used)
            self.assertEqual(save.used_potions, run.used_potions)

    def test_picked(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.picked, strict=True)
        for save, run, picked in path:
            self.assertEqual([x.name for x in save.picked], picked)
            self.assertEqual(save.picked, run.picked)

    def test_skipped(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.skipped, strict=True)
        for save, run, skipped in path:
            self.assertEqual([x.name for x in save.skipped], skipped)
            self.assertEqual(save.skipped, run.skipped)

    def test_skipped_relics(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.skipped_relics, strict=True)
        for save, run, skipped in path:
            self.assertEqual([x.name for x in save.skipped_relics], skipped)
            self.assertEqual(save.skipped_relics, run.skipped_relics)

    def test_skipped_potions(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.skipped_potions, strict=True)
        for save, run, skipped in path:
            self.assertEqual([x.name for x in save.skipped_potions], skipped)
            self.assertEqual(save.skipped_potions, run.skipped_potions)

    def test_card_count(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.card_count, strict=True)
        for save, run, count in path:
            self.assertEqual(save.card_count, count)
            self.assertEqual(save.card_count, run.card_count)

    def test_relic_count(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.relic_count, strict=True)
        for save, run, count in path:
            self.assertEqual(save.relic_count, count)
            self.assertEqual(save.relic_count, run.relic_count)

    def test_potion_count(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.potion_count, strict=True)
        for save, run, count in path:
            self.assertEqual(save.potion_count, count)
            self.assertEqual(save.potion_count, run.potion_count)

    def test_fights_count(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.fights_count, strict=True)
        for save, run, count in path:
            self.assertEqual(save.fights_count, count)
            self.assertEqual(save.fights_count, run.fights_count)

    def test_turns_count(self):
        path = zip(sm.path, rm.path[:49], _matched_contents.turns_count, strict=True)
        for save, run, count in path:
            self.assertEqual(save.turns_count, count)
            self.assertEqual(save.turns_count, run.turns_count)
