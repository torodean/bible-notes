#!/bin/python3

import matplotlib.pyplot as plt

# Example data: (Name, Birth Year, Lifespan)
people = [
    ("Adam", 0, 930),
    ("Seth", 130, 912),
    ("Enosh", 235, 905),
    ("Cainan", 325, 910),
    ("Mahalalel", 395, 895),
    ("Jared", 460, 962),
    ("Enoch", 622, 365),
    ("Methuselah", 687, 969),
    ("Lamech", 874, 777),
    ("Noah", 1056, 950),
    ("Shem", 1558, 500),
    ("Arphaxad", 1658, 403),
    ("Salah", 1693, 403),
    ("Eber", 1723, 430),
    ("Peleg", 1757, 209),
    ("Reu", 1787, 207),
    ("Serug", 1819, 200),
    ("Nahor", 1849, 119),
    ("Terah", 1878, 205),
    ("Abram", 1948, 170)
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
