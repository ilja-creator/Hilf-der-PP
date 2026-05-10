from menu.main import menu
from chase.main import chase

wins = 0

state = menu(state="title")
while state == "chase":
    if chase():
        wins += 1
    state = menu(state="menu")

print(wins)