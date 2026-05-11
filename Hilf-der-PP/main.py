from menu.main import menu
from dogs.chase.main import chase
from dogs.skye.main import skye

wins = 0

state = menu(state="title")
while state == "chase" or state == "skye":
    if state == "chase":
        if chase():
            wins += 1
    elif state == "skye":
        if skye():
            wins += 1
    state = menu(state="menu")

print(wins)