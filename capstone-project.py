import PySimpleGUI as sg
import random

with open("words.txt") as words:
    word_list = ("".join(words.read()))
    word_list = word_list.split()


def startmenu():
    startmenu = [[sg.Text("Welcome to Wordle!", size=(20, 1), text_color="white")],  # sets up the start menu for the window to read
                 [sg.Button("Start"), sg.Button("Exit")]]
    return startmenu


def restart_win(guess_word):
    restart_w = [[sg.Text(f"You Won! The word was {guess_word}")],
                 [sg.Button("Play Again"), sg.Button("Exit")]]
    window = sg.Window("Wordle", restart_w)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            break
        if event == "Play Again":
            window.close()
            gameplay()
            break


def restart_loss(guess_word):
    restart_l = [[sg.Text(f"You Lost! The word was {guess_word}")],
                 [sg.Button("Play Again"), sg.Button("Exit")]]
    window = sg.Window("Wordle", restart_l)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            break
        if event == "Play Again":
            window.close()
            window = sg.Window("Wordle")
            gameplay()
            break


def gameplay():
    game_window = [
        [sg.Text("Guesses must be 5 letters long! Make your best guess!")],          #
        [sg.Input(key="GUESS"), sg.Button("Enter", key="ENTER_BUTTON", bind_return_key=True), sg.Button("Hint", key="HINT")]]
    window = sg.Window("Wordle", game_window)
    guess_word = random.choice(word_list)
    print(guess_word)
    turn = 0
    while turn <= 50:
        event, values = window.read()
        if turn == 50:
            window.close()
            window = sg.Window(
                "WordleL", restart_loss(guess_word.capitalize()))
            break
        if event == sg.WIN_CLOSED:
            break
        if event == "HINT":
            window.extend_layout(
                window, [[sg.Text(f"First letter is {guess_word[0]}", key="HINT_LINE")]])
        if event == "ENTER_BUTTON":
            if "HINT_LINE" in window.AllKeysDict:
                window["HINT"].update(visible=False)
                window["HINT_LINE"].update(visible=False)
            if len(values["GUESS"]) != 5 or values["GUESS"].isalpha() == False:
                window["GUESS"].update("")
            count = 0
            win = 0
            guess = values["GUESS"].upper()
            window.extend_layout(window, [[sg.Text(guess[0], key=turn+0), sg.Text(guess[1], key=turn+1), sg.Text(
                guess[2], key=turn+2), sg.Text(guess[3], key=turn+3), sg.Text(guess[4], key=turn+4)]])
            for letter, correct in zip(guess, guess_word):
                if letter == correct:
                    window[turn+count].update(background_color="green")
                    win += 1
                elif letter != correct:
                    if letter in guess_word:
                        window[turn+count].update(background_color="orange")
                    else:
                        window[turn+count].update(background_color="red")
                count += 1
            if win == 5:
                window.close()
                window = sg.Window(
                    "Wordle", restart_win(guess_word.capitalize()))
                return True
                break

        window["GUESS"].update("")
        turn += 10


window = sg.Window("Wordle", startmenu())
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        window.close()
        break
    elif event == "Start":
        window.close()
        gameplay()
        if gameplay == True:
            restart_win(guess_word)
            break
        elif gameplay == False:
            restart_loss(guess_word)
