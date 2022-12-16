"""code needed to connect game to leaderboard in Google Sheets"""
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('project3_leaderboard')

leaderboard = SHEET.worksheet('board')

data = leaderboard.get_all_values()

# declare constants to be used for input verification
MENU_INPUT = ["1", "s", "start", "2", "o", "options", "3", "l", "leaderboard"]
OPTIONS_INPUT = ["1", "d", "difficulty", "2", "m", "map", "3", "b", "back"]
AI_INPUT = [
    "1", "e", "easy", "2", "n", "normal", "3", "h", "hard", "4", "b", "back"
    ]
MAP_SIZE_INPUT = [
    "1", "s", "small", "2", "m", "medium", "3", "l", "large", "4", "b", "back"
    ]
LEADERBOARD_INPUT = ["1", "b", "back"]
SHIP_INPUT = ["1", "p", "place", "2", "r", "rotate"]


def valid_menu_input(choice):
    """function to check validity of input on menu screen"""

    num = 0
    is_valid = False
    while num < 9:
        if choice == MENU_INPUT[num]:
            is_valid = True
            num = 9
        else:
            num += 1
    return is_valid


def ai_difficulty(difficulty):
    """function translates difficulty into text for user"""
    result = ""
    if difficulty == 0:
        result = "Easy"
    elif difficulty == 1:
        result = "Normal"
    elif difficulty == 2:
        result = "Hard"
    return result


def map_size(size):
    """function translates map size into text for user"""
    result = ""
    if size == 0:
        result = "Small"
    elif size == 1:
        result = "Medium"
    elif size == 2:
        result = "Large"
    return result


def start_game(difficulty, size):
    """funtion that controls the game starting"""
    print("placeholder")


def menu_output(validity, choice, difficulty, size):
    """funtion controls result of user input on menu screen"""
    if not validity:
        print(
            f"Invalid input, please input one of the following: {MENU_INPUT}"
            )
        menu_screen(difficulty, size)

    if choice == "1" or choice == "s" or choice == "start":
        start_game(difficulty, size)
    elif choice == "2" or choice == "o" or choice == "options":
        options_screen(difficulty, size)
    elif choice == "3" or choice == "l" or choice == "leaderboard":
        leaderboard_screen(difficulty, size)


def menu_screen(difficulty, size):
    """function that controls menu screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)

    print("BATTLESHIPS")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [S]tart")
    print("2. [O]ptions")
    print("3. [L]eaderboard")
    choice = input("Please enter your choice here: ").lower()
    validity = valid_menu_input(choice)
    menu_output(validity, choice, difficulty, size)


def valid_options_input(choice):
    """function to check validity of input on options screen"""

    num = 0
    is_valid = False
    while num < 9:
        if choice == OPTIONS_INPUT[num]:
            is_valid = True
            num = 9
        else:
            num += 1
    return is_valid


def options_output(validity, choice, difficulty, size):
    """funtion controls result of user input on menu screen"""
    if not validity:
        print(
            f"Invalid input, please input one of the following:{OPTIONS_INPUT}"
            )
        options_screen(difficulty, size)

    if choice == "1" or choice == "d" or choice == "difficulty":
        difficulty_screen(difficulty, size)
    elif choice == "2" or choice == "m" or choice == "map":
        map_screen(difficulty, size)
    elif choice == "3" or choice == "b" or choice == "back":
        menu_screen(difficulty, size)


def options_screen(difficulty, size):
    """funtion that controls the options screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)
    print("OPTIONS")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [D]ifficulty")
    print("2. [M]ap")
    print("3. [B]ack")
    choice = input("Please enter your choice here: ").lower()
    validity = valid_options_input(choice)
    options_output(validity, choice, difficulty, size)


def valid_difficulty_input(choice):
    """function to check validity of input on difficulty screen"""

    num = 0
    is_valid = False
    while num < 12:
        if choice == AI_INPUT[num]:
            is_valid = True
            num = 12
        else:
            num += 1
    return is_valid


def difficulty_output(validity, choice, difficulty, size):
    """funtion controls result of user input on difficulty screen"""
    if not validity:
        print(
            f"Invalid input, please input one of the following: {AI_INPUT}"
            )
        difficulty_screen(difficulty, size)

    if choice == "1" or choice == "e" or choice == "easy":
        difficulty = 0
        difficulty_screen(difficulty, size)
    elif choice == "2" or choice == "n" or choice == "normal":
        difficulty = 1
        difficulty_screen(difficulty, size)
    elif choice == "3" or choice == "h" or choice == "hard":
        difficulty = 2
        difficulty_screen(difficulty, size)
    elif choice == "4" or choice == "b" or choice == "back":
        options_screen(difficulty, size)


def difficulty_screen(difficulty, size):
    """funtion that controls the difficulty screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)
    print("OPTIONS")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [E]asy")
    print("2. [N]ormal")
    print("3. [H]ard")
    print("4. [B]ack")
    choice = input("Please enter your choice here: ").lower()
    validity = valid_difficulty_input(choice)
    difficulty_output(validity, choice, difficulty, size)


def map_screen(difficulty, size):
    print("placeholder")


def leaderboard_screen(difficulty, size):
    """function that controls the leaderboard screen"""
    print("placeholder")


menu_screen(0, 0)
