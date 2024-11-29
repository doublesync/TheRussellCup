import random


def get_random_items(items, num_items):

  if len(items) < num_items:
    return "Error: Not enough items in the list."
  return random.sample(items, num_items)

animations = [[
  "Pro",
  "Anthony Edwards",
  "Austin Reaves",
  "Coby White",
  "Damian Lillard",
  "Darius Garland",
  "De'Aaron Fox",
  "Dejounte Murray",
  "Devin Booker",
  "Domantas Sabonis",
  "Donovan Mitchell",
  "Giannis Antetokounmpo",
  "Ja Morant",
  "Jalen Green",
  "James Harden",
  "Jaylen Brown",
  "Jayson Tatum",
  "Kevin Durant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Luka Doncic",
  "Nikola Jokic",
  "Paolo Banchero",
  "Russell Westbrook",
  "Stephen Curry",
  "Trae Young",
  "Tyrese Haliburton",
  "Tyrese Maxey",
  "Zach LaVine",
  "Zion Williamson"
],
[
  "Pro",
  "Fundamental",
  "Anthony Edwards",
  "Chris Paul",
  "Damian Lillard",
  "De'Aaron Fox",
  "Domantas Sabonis",
  "Donovan Mitchell",
  "Ja Morant",
  "Jason Williams",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Luka Doncic",
  "Magic Johnson",
  "Mike Conley",
  "Nikola Jokic",
  "Paolo Banchero",
  "Stephen Curry",
  "Trae Young",
  "Tyrese Haliburton"
],
[
  "Pro",
  "Allen Iverson",
  "Baron Davis",
  "Ben Simmons",
  "Cade Cunningham",
  "Carmelo Anthony",
  "Chris Paul",
  "CJ McCollum",
  "Coby White",
  "Damian Lillard",
  "D'Angelo Russell",
  "DeMar DeRozan",
  "Derrick Rose",
  "Desmond Bane",
  "Devin Booker",
  "Donovan Mitchell",
  "Dwyane Wade",
  "Giannis Antetokounmpo",
  "Isaiah Thomas",
  "Ja Morant",
  "James Harden",
  "Jason Kidd",
  "Jason Williams",
  "Jayson Tatum",
  "Jeremy Lin",
  "Jimmy Butler",
  "Jordan Poole",
  "Jrue Holiday",
  "Kawhi Leonard",
  "Kemba Walker",
  "Kevin Durant",
  "Kyle Lowry",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Lonzo Ball",
  "Luka Doncic",
  "Mike Bibby",
  "Paul George",
  "Penny Hardaway",
  "Rafer Alston",
  "Russell Westbrook",
  "Scoot Henderson",
  "Stephen Curry",
  "Stephon Marbury",
  "Steve Nash",
  "Terry Rozier III",
  "Trae Young",
  "Zach LaVine",
  "Zion Williamson"
],
[
  "Pro",
  "Allen Iverson",
  "Anthony Edwards",
  "Austin Reaves",
  "Cade Cunningham",
  "Chris Paul",
  "Coby White",
  "Damian Lillard",
  "D'Angelo Russell",
  "Darius Garland",
  "De'Aaron Fox",
  "DeMar DeRozan",
  "Derrick Rose",
  "Devin Booker",
  "Donovan Mitchell",
  "Eric Gordon",
  "Giannis Antetokounmpo",
  "Isaiah Thomas",
  "Ja Morant",
  "Jalen Green",
  "James Harden",
  "Jason Williams",
  "Jaylen Brown",
  "Jayson Tatum",
  "Jimmy Butler",
  "Jordan Poole",
  "Jrue Holiday",
  "Kawhi Leonard",
  "Kemba Walker",
  "Kevin Durant",
  "Klay Thompson",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Lonzo Ball",
  "Luka Doncic",
  "Markelle Fultz",
  "Michael Jordan",
  "Mike Conley",
  "Paolo Banchero",
  "Paul George",
  "Penny Hardaway",
  "Rafer Alston",
  "Reggie Jackson",
  "Russell Westbrook",
  "Scoot Henderson",
  "Stephen Curry",
  "Stephon Marbury",
  "Steve Francis",
  "Terry Rozier III",
  "Tim Hardaway",
  "Trae Young",
  "Zach LaVine",
  "Zion Williamson"
],
[
    "Pro",
    "Allen Iverson",
    "Andrew Wiggins",
    "Anthony Edwards",
    "Austin Reaves",
    "Brandon Ingram",
    "Cade Cunningham",
    "Chris Paul",
    "CJ McCollum",
    "Coby White",
    "Damian Lillard",
    "D'Angelo Russell",
    "Darius Garland",
    "De'Aaron Fox",
    "DeMar DeRozan",
    "Derrick Rose",
    "Devin Booker",
    "Donovan Mitchell",
    "Eric Gordon",
    "Giannis Antetokounmpo",
    "Isaiah Thomas",
    "Ja Morant",
    "Jaden McDaniels",
    "Jalen Green",
    "James Harden",
    "Jason Williams",
    "Jaylen Brown",
    "Jayson Tatum",
    "Jimmy Butler",
    "Jordan Poole",
    "Jrue Holiday",
    "Kawhi Leonard",
    "Kemba Walker",
    "Kevin Durant",
    "Klay Thompson",
    "Kobe Bryant",
    "Kyrie Irving",
    "LaMelo Ball",
    "LeBron James",
    "Lonzo Ball",
    "Luka Doncic",
    "Paolo Banchero",
    "Paul George",
    "Penny Hardaway",
    "Rafer Alston",
    "Reggie Jackson",
    "Russell Westbrook",
    "Scoot Henderson",
    "Stephen Curry",
    "Stephon Marbury",
    "Steve Francis",
    "Terry Rozier III",
    "Tim Hardaway",
    "Trae Young",
    "Zach LaVine",
    "Zion Williamson"
],
[
  "Pro",
  "Allen Iverson",
  "Chris Paul",
  "Damian Lillard",
  "Darius Garland",
  "De'Aaron Fox",
  "Devin Booker",
  "Giannis Antetokounmpo",
  "Ja Morant",
  "James Harden",
  "Jayson Tatum",
  "Jimmy Butler",
  "Joel Embiid",
  "Kevin Durant",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Luka Doncic",
  "Paul George",
  "Stephen Curry",
  "Zach LaVine"
],
[
  "Pro",
  "Allen Iverson",
  "Anthony Edwards",
  "Bradley Beal",
  "Coby White",
  "Damian Lillard",
  "Devin Booker",
  "Ja Morant",
  "James Harden",
  "Jayson Tatum",
  "Jordan Poole",
  "Kevin Durant",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Stephen Curry",
  "Trae Young",
  "Zach LaVine"
],
[
  "Pro",
  "Allen Iverson",
  "Anthony Edwards",
  "Austin Reaves",
  "Brandon Ingram",
  "Chris Paul",
  "Coby White",
  "Cole Anthony",
  "Damian Lillard",
  "D'Angelo Russell",
  "Darius Garland",
  "DeMar DeRozan",
  "Devin Booker",
  "Donovan Mitchell",
  "Ja Morant",
  "James Harden",
  "Jason Williams",
  "Jaylen Brown",
  "Jayson Tatum",
  "Jimmy Butler",
  "Jordan Poole",
  "Josh Giddey",
  "Kawhi Leonard",
  "Kevin Durant",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Lonzo Ball",
  "Luka Doncic",
  "Malik Monk",
  "Markelle Fultz",
  "Michael Jordan",
  "Mike Conley",
  "Paolo Banchero",
  "Paul George",
  "Russell Westbrook",
  "Scoot Henderson",
  "Stephen Curry",
  "Terry Rozier III",
  "Trae Young",
  "Tyrese Haliburton",
  "Zach LaVine",
  "Zion Williamson"
],
[
  "Pro",
  "Allen Iverson",
  "Andrew Wiggins",
  "Anthony Edwards",
  "Chris Paul",
  "Coby White",
  "Damian Lillard",
  "Darius Garland",
  "De'Aaron Fox",
  "Devin Booker",
  "Domantas Sabonis",
  "Ja Morant",
  "Jayson Tatum",
  "Jimmy Butler",
  "Jordan Poole",
  "Kawhi Leonard",
  "Kevin Durant",
  "Kobe Bryant",
  "Kyle Kuzma",
  "Kyrie Irving",
  "LeBron James",
  "Luka Doncic",
  "Markelle Fultz",
  "Paul George",
  "Scottie Pippen",
  "Trae Young",
  "Tyrese Haliburton",
  "Tyrese Maxey",
  "Zach LaVine"
],
[
  "Pro",
  "Andrew Wiggins",
  "Darius Garland",
  "Devin Booker",
  "Giannis Antetokounmpo",
  "James Harden",
  "Jayson Tatum",
  "Jimmy Butler",
  "Joel Embiid",
  "Kawhi Leonard",
  "Kemba Walker",
  "Klay Thompson",
  "Kyrie Irving",
  "Luka Doncic",
  "Paul George",
  "Trae Young",
  "Tyrese Haliburton",
  "Zach LaVine"
],
[
  "Pro",
  "Andrew Wiggins",
  "Anthony Davis",
  "Anthony Edwards",
  "Coby White",
  "Darius Garland",
  "DeMar DeRozan",
  "Ja Morant",
  "Jayson Tatum",
  "Jimmy Butler",
  "Joel Embiid",
  "Karl-Anthony Towns",
  "Kawhi Leonard",
  "Kevin Durant",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Luka Doncic",
  "Nikola Jokic",
  "Penny Hardaway",
  "Stephen Curry",
  "Steve Nash",
  "Terry Rozier III",
  "Trae Young",
  "Tyrese Haliburton"
],
[
  "Pro",
  "Anthony Edwards",
  "Bradley Beal",
  "Chris Paul",
  "Coby White",
  "Darius Garland",
  "DeMar DeRozan",
  "Ja Morant",
  "James Harden",
  "Jayson Tatum",
  "Jimmy Butler",
  "Kevin Durant",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "Larry Bird",
  "LeBron James",
  "Luka Doncic",
  "Paolo Banchero",
  "Paul George",
  "Rajon Rondo",
  "Scottie Pippen",
  "Stephen Curry",
  "Tyrese Haliburton",
  "Zach LaVine"
],
[
    "Pro",
    "Devin Booker",
    "Kobe Bryant",
    "Stephen Curry",
    "Luka Dončić",
    "Joel Embiid",
    "Lebron James",
    "Michael Jordan",
    "Zach LaVine",
    "Zion Williamson"
],
[
  "Allen Iverson",
  "Anthony Edwards",
  "Austin Reaves",
  "Ben Simmons",
  "Bradley Beal",
  "Damian Lillard",
  "De'Aaron Fox",
  "Dejounte Murray",
  "DeMar DeRozan",
  "Derrick Rose",
  "Devin Booker",
  "Domantas Sabonis",
  "Donovan Mitchell",
  "George Gervin",
  "Giannis Antetokounmpo",
  "Ja Morant",
  "Jalen Brunson",
  "James Harden",
  "Jason Williams",
  "Jaylen Brown",
  "Jayson Tatum",
  "Jimmy Butler",
  "Joel Embiid",
  "Jordan Poole",
  "Julius Randle",
  "Kevin Durant",
  "Klay Thompson",
  "Kobe Bryant",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Luka Doncic",
  "Magic Johnson",
  "Malik Monk",
  "Michael Jordan",
  "Nikola Jokic",
  "Nikola Vucevic",
  "Russell Westbrook",
  "Stephen Curry",
  "Trae Young",
  "Tyrese Haliburton",
  "Zach LaVine",
  "Zion Williamson"
],
[
  "Big Man Off Two",
  "Big Man Tomahawks Off Two",
  "Basic One-Handers Off Two",
  "Athletic One-Handers Off Two",
  "Basic Hangs Off Two",
  "Athletic Hangs Off One",
  "Athletic Hangs Off Two",
  "Quick Drops Off One",
  "Quick Drops Off Two",
  "Rim Grazers Off Two",
  "Fist Pump Rim Pulls",
  "Basic Two-Handers Off Two",
  "Hangs Off One",
  "Big Man Hangs Off One",
  "Basic Two-Handers Off One",
  "Big Man Off One",
  "Rim Grazers Off One",
  "Basic One-Handers Off One",
  "Athletic One-Handers Off One",
  "Big Man Tomahawks Off One",
  "Side Arm Tomahawks",
  "Straight Arm Tomahawks",
  "Cock Back Tomahawks",
  "Uber Athletic Tomahawks Off One",
  "Athletic Side Tomahawks",
  "Uber Athletic Tomahawks Off Two",
  "Athletic Front Tomahawks",
  "Leaning Slams",
  "Front Clutches",
  "Front Clutches Off Two",
  "Side Clutches Off One",
  "Big Man Side Clutches Off One",
  "Side Clutches Off Two",
  "Back Scratchers Off One",
  "Big Man Back Scratchers",
  "Back Scratchers Off Two",
  "Back Scratching Rim Hangs",
  "Quick Drop-In Back Scratchers Off Two",
  "Big Man Baseline Reverses Off One",
  "Big Man Baseline Reverses Off Two",
  "Baseline Reverses Off One",
  "Clutch Reverses Off One",
  "Reverses Off One",
  "One-Hand Clutch Reverses",
  "Windmill Baseline Reverses",
  "Clutch Baseline Reverses",
  "Baseline Reverses Off Two",
  "Baseline Clutch Reverses",
  "Clutch Reverses Off Two",
  "Reverses Off Two",
  "Windmill Reverses",
  "Switcheroos Off One",
  "Windmills Off One",
  "Leaning Windmills",
  "Bigman Windmills",
  "Front Windmills",
  "Side Windmills",
  "Athletic Windmills",
  "Basic 360s",
  "Athletic 360s",
  "Cradle Dunks Off One",
  "Pro Under Basket Rim Pulls",
  "Elite Basket Rim Pulls",
  "One Hand Under Basket Athletic",
  "Two Hand Under Basket Athletic",
  "One Hand Under Basket Regular",
  "Two Hand Under Basket Regular",
  "Flashy Off Two",
  "Flashy Off One",
  "Flashy Hangs Off Two",
  "Flashy Hangs Off One",
  "360s Off Two",
  "360s Off One",
  "Under Leg Off Two",
  "Under Leg Off One",
  "Under Leg 360s Off Two",
    "Aaron Gordon",
    "Andrew Wiggins",
    "Anthony Edwards",
    "Ben Simmons",
    "CJ McCollum",
    "Clyde Drexler",
    "Darryl Dawkins",
    "De'Aaron Fox",
    "DeMar DeRozan",
    "Devin Booker",
    "Dominique Wilkins",
    "Draymond Green",
    "Dwight Howard",
    "Giannis Antetokounmpo",
    "Glenn Robinson III",
    "Harrison Barnes",
    "Ja Morant",
    "James Harden",
    "JaVale McGee",
    "Jaylen Brown",
    "Julius Erving",
    "Karl Malone",
    "Karl-Anthony Towns",
    "Keegan Murray",
    "Kevin Huerter",
    "Klay Thompson",
    "Kobe Bryant",
    "Latrell Sprewell",
    "LeBron James",
    "Luka Doncic",
    "Malik Monk",
    "Manu Ginobili",
    "Paul George",
    "Russell Westbrook",
    "Scottie Pippen",
    "Shaquille O'Neal",
    "Shawn Kemp",
    "Trey Lyles",
    "Zach LaVine",
    "Zion Williamson",
    "Pro (Alley Oop)",
    "Elite (Alley Oop)",
    "Zion Williamson (Alley Oop)",
    "Small Contact (Alley Oop)",
    "Big Contact (Alley Oop)",
    "Elite Contact (Alley Oop)"
],
[
  "Pro",
  "Pro 3",
  "Harrison Barnes",
  "Devin Booker",
  "Kobe Bryant",
  "Anthony Davis",
  "DeMar DeRozan",
  "Stephen Curry",
  "DeMar DeRozan",
  "Luka Dončić",
  "Kevin Durant",
  "Paul George",
  "Aaron Gordon",
  "De'Aaron Fox",
  "Kevin Huerter",
  "Bradon Ingram",
  "LeBron James",
  "Nikola Jokić",
  "Michael Jordan",
  "Karl Malone",
  "Boban Marjanović",
  "Donovan Mitchell",
  "Dirk Nowitzki",
  "Domantas Sabonis",
  "Pascal Siakam",
  "Jayson Tatum",
  "Karl-Anthony Towns"
  "Nikola Vučević"
],
[
  "Pro",
  "Kareem Abdul-Jabbar",
  "Giannis Antetokounmpo",
  "Nikola Jokić",
  "Shaquille O'Neal",
  "Domantas Sabonis",
  "Alperen Sengun",
  "Nikola Vučević"
],
[
  "Pro",
  "Harrison Barnes",
  "Devin Booker",
  "Kobe Bryant",
  "Anthony Davis",
  "Dirk Nowitzki",
  "Austin Rivers"
],
[
  "Pro",
  "Pro 2",
  "Pro 3",
  "Andrew Wiggins",
  "Anfernee Simons",
  "Anthony Davis",
  "Anthony Edwards",
  "Austin Reaves",
  "Bam Adebayo",
  "Ben McLemore",
  "Bogdan Bogdanovic",
  "Bradley Beal",
  "Brandon Ingram",
  "Buddy Hield",
  "Cade Cunningham",
  "Cameron Reddish",
  "Cameron Thomas",
  "Chet Holmgren",
  "Chris Paul",
  "CJ McCollum",
  "Coby White",
  "Collin Sexton",
  "Damian Lillard",
  "D'Angelo Russell",
  "Dante Exum",
  "Darius Garland",
  "Davion Mitchell",
  "De'Aaron Fox",
  "Dejounte Murray",
  "DeMar DeRozan",
  "Derrick White",
  "Desmond Bane",
  "Devin Vassell",
  "Dillon Brooks",
  "Dirk Nowitzki",
  "Donovan Mitchell",
  "Donte DiVincenzo",
  "Duncan Robinson",
  "Eric Gordon",
  "Fred VanVleet",
  "Garrison Mathews",
  "Gary Harris",
  "Giannis Antetokounmpo",
  "Glenn Robinson III",
  "Gordon Hayward",
  "Harrison Barnes",
  "Isaiah Joe",
  "Ja Morant",
  "Jabari Smith Jr.",
  "Jalen Green",
  "Jalen Suggs",
  "James Harden",
  "Jason Williams",
  "Jaylen Brown",
  "Jayson Tatum",
  "Jordan Clarkson",
  "Jordan Poole",
  "Jrue Holiday",
  "Kawhi Leonard",
  "Keegan Murray",
  "Kendrick Nunn",
  "Kentavious Caldwell-Pope",
  "Kevin Durant",
  "Kevin Huerter",
  "Keyonte George",
  "Khris Middleton",
  "Klay Thompson",
  "Kyle Kuzma",
  "Kyle Lowry",
  "Kyrie Irving",
  "Lauri Markkanen",
  "LeBron James",
  "Luka Doncic",
  "Maite Cazorla",
  "Malaki Branham",
  "Malik Beasley",
  "Malik Monk",
  "Max Strus",
  "Michael Jordan",
  "Michael Porter Jr.",
  "Mikal Bridges",
  "Mike Conley",
  "Nate Robinson",
  "Nikola Jokic",
  "Paolo Banchero",
  "Pascal Siakam",
  "Paul George",
  "Reggie Jackson",
  "Rui Hachimura",
  "Russell Westbrook",
  "Seth Curry",
  "Shaedon Sharpe",
  "Stephen Curry",
  "Taylor Hendricks",
  "Terrence Ross",
  "Tim Hardaway Jr.",
  "Trae Young",
  "Trey Murphy III",
  "Tyler Herro",
  "Tyrese Haliburton",
  "Tyrese Maxey",
  "Tyus Jones",
  "Zach LaVine"
],
[
  "Pro",
  "Allen Iverson",
  "Andrew Wiggins",
  "Austin Reaves",
  "Brook Lopez",
  "Cade Cunningham",
  "De'Aaron Fox",
  "DeMar DeRozan",
  "Devin Booker",
  "Devin Vassell",
  "Dirk Nowitzki",
  "Harrison Barnes",
  "Kevin Durant",
  "Khris Middleton",
  "Kyle Kuzma",
  "Luka Doncic",
  "Maite Cazorla",
  "Michael Jordan",
  "Nate Robinson",
  "Penny Hardaway",
  "Russell Westbrook",
  "Stephen Curry",
  "Trae Young"
],
[
    "Pro",
    "Pro 2",
    "Allen Iverson",
    "Andrew Wiggins",
    "Anthony Edwards",
    "Austin Reaves",
    "Bradley Beal",
    "Cade Cunningham",
    "Chris Paul",
    "CJ McCollum",
    "Damian Lillard",
    "Dante Exum",
    "Davion Mitchell",
    "De'Aaron Fox",
    "Desmond Bane",
    "Devin Booker",
    "Devin Vassell",
    "Dillon Brooks",
    "Dirk Nowitzki",
    "Donovan Mitchell",
    "Fred VanVleet",
    "Glenn Robinson III",
    "Harrison Barnes",
    "Jalen Green",
    "Jalen Suggs",
    "James Harden",
    "Jason Williams",
    "Jaylen Brown",
    "Jayson Tatum",
    "Jimmy Butler",
    "Jordan Clarkson",
    "Jordan Poole",
    "Jrue Holiday",
    "Keegan Murray",
    "Kent Bazemore",
    "Kevin Durant",
    "Kevin Huerter",
    "Khris Middleton",
    "Klay Thompson",
    "Kobe Bryant",
    "Kyle Kuzma",
    "Kyle Lowry",
    "Kyrie Irving",
    "LeBron James",
    "Luka Doncic",
    "Maite Cazorla",
    "Malik Monk",
    "Michael Jordan",
    "Mike Conley",
    "Nate Robinson",
    "Nikola Jokic",
    "Pascal Siakam",
    "Paul George",
    "Reggie Jackson",
    "Russell Westbrook",
    "Seth Curry",
    "Shaedon Sharpe",
    "Stephen Curry",
    "Terry Rozier III",
    "Trae Young",
    "Tyler Herro",
    "Tyrese Haliburton",
    "Zach LaVine",
    "Zion Williamson"
],
[
  "Andrew Wiggins",
  "Anthony Edwards",
  "Austin Reaves",
  "Bojan Bogdanovic",
  "Bradley Beal",
  "Brice Sensabaugh",
  "Buddy Hield",
  "Chris Paul",
  "CJ McCollum",
  "Damian Lillard",
  "Darius Garland",
  "Davion Mitchell",
  "De'Aaron Fox",
  "Delon Wright",
  "DeMar DeRozan",
  "Desmond Bane",
  "Devin Booker",
  "Devin Vassell",
  "Dillon Brooks",
  "Donovan Mitchell",
  "Eric Gordon",
  "Giannis Antetokounmpo",
  "Harrison Barnes",
  "Immanuel Quickley",
  "Ja Morant",
  "Jaden Hardy",
  "Jalen Green",
  "Jalen Suggs",
  "James Harden",
  "Jarace Walker",
  "Jayson Tatum",
  "Jimmy Butler",
  "Joel Embiid",
  "Jonathan Kuminga",
  "Jordan Clarkson",
  "Jordan Poole",
  "Keon Ellis",
  "Kevin Durant",
  "Kevin Huerter",
  "Khris Middleton",
  "Klay Thompson",
  "Kyrie Irving",
  "LaMelo Ball",
  "LeBron James",
  "Luka Doncic",
  "Malaki Branham",
  "Malik Monk",
  "Moses Moody",
  "Nikola Jokic",
  "Paolo Banchero",
  "Pascal Siakam",
  "Paul George",
  "Reggie Jackson",
  "Rui Hachimura",
  "Scoot Henderson",
  "Stephen Curry",
  "Tyrese Haliburton",
  "Tyrese Maxey",
  "Zach Lavine"
]
]

choices = {
    "dribble_style": 0,
    "passing_style": 1,
    "signature_size_up": 2,
    "regular_breakdown": 3,
    "aggresive_breakdown": 4,
    "escape_moves": 5,
    "crossover_combos": 6,
    "crossover": 7,
    "behind_the_back": 8,
    "stepback": 9,
    "spin": 10,
    "hesitation": 11,
    "triple_threat_style": 12,
    "layups": 13,
    "dunks": 14,
    "post_fade": 15,
    "post_hook": 16,
    "post_hop_shot": 17,
    "dribble_pull_up": 18,
    "spin_jumper": 19,
    "hop_jumper": 20,
    "go-to-shot": 21,
    "motion-style": 22
}

choice = choices[input("Which animation would like to select from? ")]
amount = int(input("How many selections would you like to make? "))

selected_items = get_random_items(animations[choice], amount)
print(f"Here are {amount} randomly selected items from the list: ")
for i in range(amount):
    print(f"{i+1}. {selected_items[i]}")