#!/bin/python3

import matplotlib.pyplot as plt

# Template to copy/paste from. Example data: (Name, Birth Year, Lifespan)
people_template = [
    (), 
    ()
]

# People from Adam to Abraham.
people = [
    ("Adam", 0, 930),        # Genesis 5
    ("Seth", 130, 912),      # Genesis 5
    ("Enosh", 235, 905),     # Genesis 5
    ("Cainan", 325, 910),    # Genesis 5
    ("Mahalalel", 395, 895), # Genesis 5
    ("Jared", 460, 962),     # Genesis 5
    ("Enoch", 622, 365),     # Genesis
    ("Methuselah", 687, 969),# Genesis 5
    ("Lamech", 874, 777),    # Genesis 5
    ("Noah", 1056, 950),     # Genesis 9
    ("Shem", 1558, 500),     # Genesis 11
    ("Arphaxad", 1658, 403), # Genesis 11
    ("Salah", 1693, 403),    # Genesis 11
    ("Eber", 1723, 430),     # Genesis 11
    ("Peleg", 1757, 209),    # Genesis 11
    ("Reu", 1787, 207),      # Genesis 11
    ("Serug", 1819, 200),    # Genesis 11
    ("Nahor", 1849, 119),    # Genesis 11
    ("Terah", 1878, 205),    # Genesis 11
    ("Abram", 1948, 175)     # Genesiss 25:8
]

# People of Abraham and his descendants.
people2 = [
    ("Abraham", 1948, 175),  # Genesis 25:8
    ("Ishmael", 0 , 137),    # Genesis 25:17 TODO - Determine year.
    ("", , )
]

# Sort people by birth year descending
people.sort(key=lambda x: x[1], reverse=True)

names = [p[0] for p in people]
start_years = [p[1] for p in people]
lifespans = [p[2] for p in people]

fig, ax = plt.subplots(figsize=(10, 6))

bar_height = 1.0  # Full height, so bars touch each other

for i, (name, start, span) in enumerate(zip(names, start_years, lifespans)):
    ax.barh(i, span, left=start, height=bar_height, color='skyblue', edgecolor='black')
    ax.plot([0, start], [i, i], linestyle='dotted', color='gray')  # Dotted line from y-axis to bar start

ax.set_yticks(range(len(names)))
ax.set_yticklabels(names)
ax.set_xlabel('Year')
ax.set_title('Lifespans')

plt.tight_layout()
plt.show()
