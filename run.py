"""code needed to connect game to leaderboard in Google Sheets, as well as to
produce random numbers"""
import random
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

"""declare constants to be used for input verification"""
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
SMALL_INPUT_CARRIER = [
    "1", "2", "3", "4", "5", "6", "A", "B", "C", "D", "E", "F"
    ]
MEDIUM_INPUT_CARRIER = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "A",
    "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"
     ]
LARGE_INPUT_CARRIER = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "15", "16", "A", "B", "C", "D", "E", "F", "G", "H",
    "I", "J", "K", "L", "M", "N", "O", "P"
    ]
SMALL_INPUT_BATTLESHIP = [
    "1", "2", "3", "4", "5", "6", "7", "A", "B", "C", "D", "E",
    "F", "G"
    ]
MEDIUM_INPUT_BATTLESHIP = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"
    ]
LARGE_INPUT_BATTLESHIP = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "15", "16", "17", "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"
    ]
SMALL_INPUT_SUB_DES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "A", "B", "C", "D", "E",
    "F", "G", "H"
    ]
MEDIUM_INPUT_SUB_DES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
    "L", "M"
    ]
LARGE_INPUT_SUB_DES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "15", "16", "17", "18", "A", "B", "C", "D", "E", "F",
    "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"
    ]
SMALL_INPUT_GUNBOAT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D",
    "E", "F", "G", "H", "I"
    ]
MEDIUM_INPUT_GUNBOAT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N",
    ]
LARGE_INPUT_GUNBOAT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "15", "16", "17", "18", "19", "A", "B", "C", "D",
    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
    "Q", "R", "S"
    ]
SMALL_INPUT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J"
    ]
MEDIUM_INPUT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "15", "A", "B", "C", "D", "E", "F", "G", "H", "I",
    "J", "K", "L", "M", "N", "O"
    ]
LARGE_INPUT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
    "13", "14", "15", "16", "17", "18", "19", "20", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
    "Q", "R", "S", "T"
    ]

"""global variables"""
taken_player_grid_spaces = []
taken_enemy_grid_spaces = []


def convert_collumn(collumn):
    """converts collumn number into letter"""
    letter = ""
    if collumn == 1:
        letter = "A"
    elif collumn == 2:
        letter = "B"
    elif collumn == 3:
        letter = "C"
    elif collumn == 4:
        letter = "D"
    elif collumn == 5:
        letter = "E"
    elif collumn == 6:
        letter = "F"
    elif collumn == 7:
        letter = "G"
    elif collumn == 8:
        letter = "H"
    elif collumn == 9:
        letter = "I"
    elif collumn == 10:
        letter = "J"
    elif collumn == 11:
        letter = "K"
    elif collumn == 12:
        letter = "L"
    elif collumn == 13:
        letter = "M"
    elif collumn == 14:
        letter = "N"
    elif collumn == 15:
        letter = "O"
    elif collumn == 16:
        letter = "P"
    elif collumn == 17:
        letter = "Q"
    elif collumn == 18:
        letter = "R"
    elif collumn == 19:
        letter = "S"
    elif collumn == 20:
        letter = "T"
    return letter


def convert_letter(letter):
    """converts collumn letter into number"""
    if letter == "A":
        collumn = 1
    elif letter == "B":
        collumn = 2
    elif letter == "C":
        collumn = 3
    elif letter == "D":
        collumn = 4
    elif letter == "E":
        collumn = 5
    elif letter == "F":
        collumn = 6
    elif letter == "G":
        collumn = 7
    elif letter == "H":
        collumn = 8
    elif letter == "I":
        collumn = 9
    elif letter == "J":
        collumn = 10
    elif letter == "K":
        collumn = 11
    elif letter == "L":
        collumn = 12
    elif letter == "M":
        collumn = 13
    elif letter == "N":
        collumn = 14
    elif letter == "O":
        collumn = 15
    elif letter == "P":
        collumn = 16
    elif letter == "Q":
        collumn = 17
    elif letter == "R":
        collumn = 18
    elif letter == "S":
        collumn = 19
    elif letter == "T":
        collumn = 20
    return collumn


class MapGrid:
    """define a class to handle the map grids for the game"""
    def __init__(self, size):
        self.size = size
        if self.size == 0:
            self.row0 = [
                "  |", " A |", " B |", " C |", " D |", " E |", " F |", " G |",
                " H |", " I |", " J |"
                ]
            self.row1 = [
                "1 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row2 = [
                "2 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row3 = [
                "3 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row4 = [
                "4 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row5 = [
                "5 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row6 = [
                "6 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row7 = [
                "7 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row8 = [
                "8 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row9 = [
                "9 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row10 = [
                "10|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row_divide = [
                "--|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|"
            ]
        elif self.size == 1:
            self.row0 = [
                "  |", " A |", " B |", " C |", " D |", " E |", " F |", " G |",
                " H |", " I |", " J |", " K |", " L |", " M |", " N |", " O |"
                ]
            self.row1 = [
                "1 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row2 = [
                "2 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row3 = [
                "3 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row4 = [
                "4 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row5 = [
                "5 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row6 = [
                "6 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row7 = [
                "7 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row8 = [
                "8 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row9 = [
                "9 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row10 = [
                "10|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row11 = [
                "11|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row12 = [
                "12|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row13 = [
                "13|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row14 = [
                "14|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row15 = [
                "15|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row_divide = [
                "--|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|", "---|", "---|", "---|", "---|", "---|"
            ]
        elif self.size == 2:
            self.row0 = [
                "  |", " A |", " B |", " C |", " D |", " E |", " F |", " G |",
                " H |", " I |", " J |", " K |", " L |", " M |", " N |", " O |",
                " P |", " Q |", " R |", " S |", " T |"
                ]
            self.row1 = [
                "1 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row2 = [
                "2 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row3 = [
                "3 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row4 = [
                "4 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row5 = [
                "5 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row6 = [
                "6 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row7 = [
                "7 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row8 = [
                "8 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row9 = [
                "9 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row10 = [
                "10|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row11 = [
                "11|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row12 = [
                "12|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row13 = [
                "13|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row14 = [
                "14|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row15 = [
                "15|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row16 = [
                "16|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row17 = [
                "17|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row18 = [
                "18|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row19 = [
                "19|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row20 = [
                "20|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row_divide = [
                "--|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|", "---|", "---|"
            ]

    def validate_row_placement(
        self, ship_direction, ship_length, row_choice, number_placed
    ):
        """validates row placement input of ship on map"""
        is_valid = False
        if self.size == 0:
            if ship_length == 5:
                if ship_direction == 0:
                    length_input = list(range(1, 7))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 11))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 4:
                if ship_direction == 0:
                    length_input = list(range(1, 8))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 11))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 3:
                if ship_direction == 0:
                    length_input = list(range(1, 9))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 11))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 2:
                if ship_direction == 0:
                    length_input = list(range(1, 10))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 11))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
        elif self.size == 1:
            if ship_length == 5:
                if ship_direction == 0:
                    length_input = list(range(1, 12))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 16))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 4:
                if ship_direction == 0:
                    length_input = list(range(1, 13))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 16))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 3:
                if ship_direction == 0:
                    length_input = list(range(1, 14))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 16))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 2:
                if ship_direction == 0:
                    length_input = list(range(1, 15))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 16))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
        elif self.size == 2:
            if ship_length == 5:
                if ship_direction == 0:
                    length_input = list(range(1, 17))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 21))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 4:
                if ship_direction == 0:
                    length_input = list(range(1, 18))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 21))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 3:
                if ship_direction == 0:
                    length_input = list(range(1, 19))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 21))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
            elif ship_length == 2:
                if ship_direction == 0:
                    length_input = list(range(1, 20))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
                elif ship_direction == 1:
                    length_input = list(range(1, 21))
                    num = 0
                    while num < len(length_input):
                        if int(row_choice) == length_input[num]:
                            is_valid = True
                            num = len(length_input)
                        else:
                            num += 1
        return is_valid

    def validate_col_place(
        self, ship_direction, ship_length, collumn_choice, number_placed
    ):
        """validates collumn placement input of ship on map"""
        is_valid = False
        if self.size == 0:
            if ship_length == 5:
                if ship_direction == 0:
                    num = 0
                    while num < len(SMALL_INPUT):
                        if collumn_choice == SMALL_INPUT[num]:
                            is_valid = True
                            num = len(SMALL_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(SMALL_INPUT_CARRIER):
                        if collumn_choice == SMALL_INPUT_CARRIER[num]:
                            is_valid = True
                            num = len(SMALL_INPUT_CARRIER)
                        else:
                            num += 1
            elif ship_length == 4:
                if ship_direction == 0:
                    num = 0
                    while num < len(SMALL_INPUT):
                        if collumn_choice == SMALL_INPUT[num]:
                            is_valid = True
                            num = len(SMALL_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(SMALL_INPUT_BATTLESHIP):
                        if collumn_choice == SMALL_INPUT_BATTLESHIP[num]:
                            is_valid = True
                            num = len(SMALL_INPUT_BATTLESHIP)
                        else:
                            num += 1
            elif ship_length == 3:
                if ship_direction == 0:
                    num = 0
                    while num < len(SMALL_INPUT):
                        if collumn_choice == SMALL_INPUT[num]:
                            is_valid = True
                            num = len(SMALL_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(SMALL_INPUT_SUB_DES):
                        if collumn_choice == SMALL_INPUT_SUB_DES[num]:
                            is_valid = True
                            num = len(SMALL_INPUT_SUB_DES)
                        else:
                            num += 1
            elif ship_length == 2:
                if ship_direction == 0:
                    num = 0
                    while num < len(SMALL_INPUT):
                        if collumn_choice == SMALL_INPUT[num]:
                            is_valid = True
                            num = len(SMALL_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(SMALL_INPUT_GUNBOAT):
                        if collumn_choice == SMALL_INPUT_GUNBOAT[num]:
                            is_valid = True
                            num = len(SMALL_INPUT_GUNBOAT)
                        else:
                            num += 1
        elif self.size == 1:
            if ship_length == 5:
                if ship_direction == 0:
                    num = 0
                    while num < len(MEDIUM_INPUT):
                        if collumn_choice == MEDIUM_INPUT[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(MEDIUM_INPUT_CARRIER):
                        if collumn_choice == MEDIUM_INPUT_CARRIER[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT_CARRIER)
                        else:
                            num += 1
            elif ship_length == 4:
                if ship_direction == 0:
                    num = 0
                    while num < len(MEDIUM_INPUT):
                        if collumn_choice == MEDIUM_INPUT[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(MEDIUM_INPUT_BATTLESHIP):
                        if collumn_choice == MEDIUM_INPUT_BATTLESHIP[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT_BATTLESHIP)
                        else:
                            num += 1
            elif ship_length == 3:
                if ship_direction == 0:
                    num = 0
                    while num < len(MEDIUM_INPUT):
                        if collumn_choice == MEDIUM_INPUT[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(MEDIUM_INPUT_SUB_DES):
                        if collumn_choice == MEDIUM_INPUT_SUB_DES[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT_SUB_DES)
                        else:
                            num += 1
            elif ship_length == 2:
                if ship_direction == 0:
                    num = 0
                    while num < len(MEDIUM_INPUT):
                        if collumn_choice == MEDIUM_INPUT[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(MEDIUM_INPUT_GUNBOAT):
                        if collumn_choice == MEDIUM_INPUT_GUNBOAT[num]:
                            is_valid = True
                            num = len(MEDIUM_INPUT_GUNBOAT)
                        else:
                            num += 1
        elif self.size == 2:
            if ship_length == 5:
                if ship_direction == 0:
                    num = 0
                    while num < len(LARGE_INPUT):
                        if collumn_choice == LARGE_INPUT[num]:
                            is_valid = True
                            num = len(LARGE_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(LARGE_INPUT_CARRIER):
                        if collumn_choice == LARGE_INPUT_CARRIER[num]:
                            is_valid = True
                            num = len(LARGE_INPUT_CARRIER)
                        else:
                            num += 1
            elif ship_length == 4:
                if ship_direction == 0:
                    num = 0
                    while num < len(LARGE_INPUT):
                        if collumn_choice == LARGE_INPUT[num]:
                            is_valid = True
                            num = len(LARGE_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(LARGE_INPUT_BATTLESHIP):
                        if collumn_choice == LARGE_INPUT_BATTLESHIP[num]:
                            is_valid = True
                            num = len(LARGE_INPUT_BATTLESHIP)
                        else:
                            num += 1
            elif ship_length == 3:
                if ship_direction == 0:
                    num = 0
                    while num < len(LARGE_INPUT):
                        if collumn_choice == LARGE_INPUT[num]:
                            is_valid = True
                            num = len(LARGE_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(LARGE_INPUT_SUB_DES):
                        if collumn_choice == LARGE_INPUT_SUB_DES[num]:
                            is_valid = True
                            num = len(LARGE_INPUT_SUB_DES)
                        else:
                            num += 1
            elif ship_length == 2:
                if ship_direction == 0:
                    num = 0
                    while num < len(LARGE_INPUT):
                        if collumn_choice == LARGE_INPUT[num]:
                            is_valid = True
                            num = len(LARGE_INPUT)
                        else:
                            num += 1
                elif ship_direction == 1:
                    num = 0
                    while num < len(LARGE_INPUT_GUNBOAT):
                        if collumn_choice == LARGE_INPUT_GUNBOAT[num]:
                            is_valid = True
                            num = len(LARGE_INPUT_GUNBOAT)
                        else:
                            num += 1
        return is_valid

    def print_grid(self):
        """function to print the grid to the console"""
        dividing_row = ""
        title_row = ""
        first_row = ""
        second_row = ""
        third_row = ""
        fourth_row = ""
        fifth_row = ""
        sixth_row = ""
        seventh_row = ""
        eighth_row = ""
        ninth_row = ""
        tenth_row = ""
        eleventh_row = ""
        twelth_row = ""
        thirteenth_row = ""
        fourteenth_row = ""
        fifteenth_row = ""
        sixteenth_row = ""
        seventeenth_row = ""
        eighteenth_row = ""
        ninteenth_row = ""
        twentieth_row = ""
        if self.size == 0:
            for i in range(0, 11):
                dividing_row += self.row_divide[i]
                title_row += self.row0[i]
                first_row += self.row1[i]
                second_row += self.row2[i]
                third_row += self.row3[i]
                fourth_row += self.row4[i]
                fifth_row += self.row5[i]
                sixth_row += self.row6[i]
                seventh_row += self.row7[i]
                eighth_row += self.row8[i]
                ninth_row += self.row9[i]
                tenth_row += self.row10[i]
            print(title_row)
            print(dividing_row)
            print(first_row)
            print(dividing_row)
            print(second_row)
            print(dividing_row)
            print(third_row)
            print(dividing_row)
            print(fourth_row)
            print(dividing_row)
            print(fifth_row)
            print(dividing_row)
            print(sixth_row)
            print(dividing_row)
            print(seventh_row)
            print(dividing_row)
            print(eighth_row)
            print(dividing_row)
            print(ninth_row)
            print(dividing_row)
            print(tenth_row)
            print(dividing_row)
        if self.size == 1:
            for i in range(0, 16):
                dividing_row += self.row_divide[i]
                title_row += self.row0[i]
                first_row += self.row1[i]
                second_row += self.row2[i]
                third_row += self.row3[i]
                fourth_row += self.row4[i]
                fifth_row += self.row5[i]
                sixth_row += self.row6[i]
                seventh_row += self.row7[i]
                eighth_row += self.row8[i]
                ninth_row += self.row9[i]
                tenth_row += self.row10[i]
                eleventh_row += self.row11[i]
                twelth_row += self.row12[i]
                thirteenth_row += self.row13[i]
                fourteenth_row += self.row14[i]
                fifteenth_row += self.row15[i]
            print(title_row)
            print(dividing_row)
            print(first_row)
            print(dividing_row)
            print(second_row)
            print(dividing_row)
            print(third_row)
            print(dividing_row)
            print(fourth_row)
            print(dividing_row)
            print(fifth_row)
            print(dividing_row)
            print(sixth_row)
            print(dividing_row)
            print(seventh_row)
            print(dividing_row)
            print(eighth_row)
            print(dividing_row)
            print(ninth_row)
            print(dividing_row)
            print(tenth_row)
            print(dividing_row)
            print(eleventh_row)
            print(dividing_row)
            print(twelth_row)
            print(dividing_row)
            print(thirteenth_row)
            print(dividing_row)
            print(fourteenth_row)
            print(dividing_row)
            print(fifteenth_row)
            print(dividing_row)
        if self.size == 2:
            for i in range(0, 21):
                dividing_row += self.row_divide[i]
                title_row += self.row0[i]
                first_row += self.row1[i]
                second_row += self.row2[i]
                third_row += self.row3[i]
                fourth_row += self.row4[i]
                fifth_row += self.row5[i]
                sixth_row += self.row6[i]
                seventh_row += self.row7[i]
                eighth_row += self.row8[i]
                ninth_row += self.row9[i]
                tenth_row += self.row10[i]
                eleventh_row += self.row11[i]
                twelth_row += self.row12[i]
                thirteenth_row += self.row13[i]
                fourteenth_row += self.row14[i]
                fifteenth_row += self.row15[i]
                sixteenth_row += self.row16[i]
                seventeenth_row += self.row17[i]
                eighteenth_row += self.row18[i]
                ninteenth_row += self.row19[i]
                twentieth_row += self.row20[i]
            print(title_row)
            print(dividing_row)
            print(first_row)
            print(dividing_row)
            print(second_row)
            print(dividing_row)
            print(third_row)
            print(dividing_row)
            print(fourth_row)
            print(dividing_row)
            print(fifth_row)
            print(dividing_row)
            print(sixth_row)
            print(dividing_row)
            print(seventh_row)
            print(dividing_row)
            print(eighth_row)
            print(dividing_row)
            print(ninth_row)
            print(dividing_row)
            print(tenth_row)
            print(dividing_row)
            print(eleventh_row)
            print(dividing_row)
            print(twelth_row)
            print(dividing_row)
            print(thirteenth_row)
            print(dividing_row)
            print(fourteenth_row)
            print(dividing_row)
            print(fifteenth_row)
            print(dividing_row)
            print(sixteenth_row)
            print(dividing_row)
            print(seventeenth_row)
            print(dividing_row)
            print(eighteenth_row)
            print(dividing_row)
            print(ninteenth_row)
            print(dividing_row)
            print(twentieth_row)
            print(dividing_row)

    def valid_enemy_shot_input(self, row, collumn):
        """function validates ai input when ai chooses a grid to shoot"""
        print("placeholder")


class EnemyAI:
    """defining a class to manage the AI"""
    def __init__(self, difficulty, size):
        self.difficulty = difficulty
        if size == 0:
            self.map_size = 10
        elif size == 1:
            self.map_size = 15
        elif size == 2:
            self.map_size = 20
        self.turn_row = 0
        self.turn_collumn = 0

    def turn(self, hit_last, sunk_last, unsunk_ship, row, collumn):
        if self.difficulty == 0:
            self.turn_row = random.randint(1, self.map_size)
            self.turn_collumn = random.randint(1, self.map_size)
        elif self.difficulty == 1:
            if sunk_last:
                self.turn_row = random.randint(1, self.map_size)
                self.turn_collumn = random.randint(1, self.map_size)
            elif not hit_last:
                self.turn_row = random.randint(1, self.map_size)
                self.turn_collumn = random.randint(1, self.map_size)
            elif hit_last:
                direction = random.randint(0, 1)
                if direction == 0:
                    if self.turn_row == self.map_size:
                        self.turn_row -= 1
                    elif self.turn_row == 1:
                        self.turn_row += 1
                    else:
                        increase_decrease = random.randint(0, 1)
                        if increase_decrease == 0:
                            self.turn_row -= 1
                        elif increase_decrease == 1:
                            self.turn_row += 1
                elif direction == 1:
                    if self.turn_collumn == self.map_size:
                        self.turn_collumn -= 1
                    elif self.turn_collumn == 1:
                        self.turn_collumn += 1
                    else:
                        increase_decrease = random.randint(0, 1)
                        if increase_decrease == 0:
                            self.turn_collumn -= 1
                        elif increase_decrease == 1:
                            self.turn_collumn += 1
        elif self.difficulty == 2:
            if not unsunk_ship:
                self.turn_row = random.randint(1, self.map_size)
                self.turn_collumn = random.randint(1, self.map_size)
            elif unsunk_ship:
                self.turn_row = row
                self.turn_collumn = collumn
                direction = random.randint(0, 1)
                if direction == 0:
                    if self.turn_row == self.map_size:
                        self.turn_row -= 1
                    elif self.turn_row == 1:
                        self.turn_row += 1
                    else:
                        increase_decrease = random.randint(0, 1)
                        if increase_decrease == 0:
                            self.turn_row -= 1
                        elif increase_decrease == 1:
                            self.turn_row += 1
                if direction == 1:
                    if self.turn_collumn == self.map_size:
                        self.turn_collumn -= 1
                    elif self.turn_collumn == 1:
                        self.turn_collumn += 1
                    else:
                        increase_decrease = random.randint(0, 1)
                        if increase_decrease == 0:
                            self.turn_collumn -= 1
                        elif increase_decrease == 1:
                            self.turn_collumn += 1


class Ship:
    """class for all ships used"""
    def __init__(self, type, direction=0):
        self.type = type
        self.direction = direction
        if self.type == "carrier":
            self.segments = ["", "", "", "", ""]
        elif self.type == "battleship":
            self.segments = ["", "", "", ""]
        elif self.type == "destroyer" or self.type == "submarine":
            self.segments = ["", "", ""]
        elif self.type == "gunboat":
            self.segments = ["", ""]

    def ship_placed(self, row, collumn):
        """function for filling segments lists with co-ordinates"""
        if self.direction == 0:
            for i in range(len(self.segments)):
                letter = convert_collumn(collumn)
                self.segments[i] = letter + str(row)
                collumn += 1
        elif self.direction == 1:
            letter = convert_collumn(collumn)
            for i in range(len(self.segments)):
                self.segments[i] = letter + str(row)
                row += 1


"""declaring all possible class instances to be used within later functions"""
player_map_small = MapGrid(0)
player_map_medium = MapGrid(1)
player_map_large = MapGrid(2)
hidden_map_small = MapGrid(0)
hidden_map_medium = MapGrid(1)
hidden_map_large = MapGrid(2)
enemy_map_small = MapGrid(0)
enemy_map_medium = MapGrid(1)
enemy_map_large = MapGrid(2)
enemy_easy_small = EnemyAI(0, 0)
enemy_easy_medium = EnemyAI(0, 1)
enemy_easy_large = EnemyAI(0, 2)
enemy_normal_small = EnemyAI(1, 0)
enemy_normal_medium = EnemyAI(1, 1)
enemy_normal_large = EnemyAI(1, 2)
enemy_hard_small = EnemyAI(2, 0)
enemy_hard_medium = EnemyAI(2, 1)
enemy_hard_large = EnemyAI(2, 2)
player_carrier = Ship("carrier")
player_battleship = Ship("battleship")
player_submarine = Ship("submarine")
player_destroyer = Ship("destroyer")
player_gunboat = Ship("gunboat")
enemy_carrier = Ship("carrier")
enemy_battleship = Ship("battleship")
enemy_submarine = Ship("submarine")
enemy_destroyer = Ship("destroyer")
enemy_gunboat = Ship("gunboat")


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


def valid_start_placing_input(choice):
    """function validating first input related to ship placing"""
    num = 0
    is_valid = False
    while num < 6:
        if choice == SHIP_INPUT[num]:
            is_valid = True
            num = 9
        else:
            num += 1
    return is_valid


def taken_spaces(number_placed, who):
    """ensures already taken spaces are tracked"""
    if number_placed == 1:
        if who == "player":
            for i in len(player_carrier.segments):
                taken_space = player_carrier.segments[i]
                taken_player_grid_spaces.append(taken_space)
        elif who == "enemy":
            for i in len(enemy_carrier.segments):
                taken_space = enemy_carrier.segments[i]
                taken_enemy_grid_spaces.append(taken_space)
    elif number_placed == 2:
        if who == "player":
            for i in len(player_battleship.segments):
                taken_space = player_battleship.segments[i]
                taken_player_grid_spaces.append(taken_space)
        elif who == "enemy":
            for i in len(enemy_battleship.segments):
                taken_space = enemy_battleship.segments[i]
                taken_enemy_grid_spaces.append(taken_space)
    elif number_placed == 3:
        if who == "player":
            for i in len(player_submarine.segments):
                taken_space = player_submarine.segments[i]
                taken_player_grid_spaces.append(taken_space)
        elif who == "enemy":
            for i in len(enemy_submarine.segments):
                taken_space = enemy_submarine.segments[i]
                taken_enemy_grid_spaces.append(taken_space)
    elif number_placed == 4:
        if who == "player":
            for i in len(player_destroyer.segments):
                taken_space = player_destroyer.segments[i]
                taken_player_grid_spaces.append(taken_space)
        elif who == "enemy":
            for i in len(enemy_destroyer.segments):
                taken_space = enemy_destroyer.segments[i]
                taken_enemy_grid_spaces.append(taken_space)
    elif number_placed == 5:
        if who == "player":
            for i in len(player_gunboat.segments):
                taken_space = player_gunboat.segments[i]
                taken_player_grid_spaces.append(taken_space)
        elif who == "enemy":
            for i in len(enemy_gunboat.segments):
                taken_space = enemy_gunboat.segments[i]
                taken_enemy_grid_spaces.append(taken_space)


def place_current_ship_small_invalid_input(number_placed):
    """controls output in event of an invalid input"""
    print(
        "Invalid input, please enter a number between 1 and 10, or a letter" +
        " between A and J if enterring a collumn."
        )
    print(
        "Also, please remember that your ship cannot go over" +
        " the edge of the map"
        )
    place_current_ship_small(number_placed)


def update_placements(row_choice, collumn_choice, ship_length):
    """updates map and ship objects with ship placement info"""


def place_current_ship_small(number_placed):
    """controls actual placing of ship on small map"""
    if number_placed == 1:
        if player_carrier.direction == 0:
            print(
                f"The {player_carrier.type} cannot be closer than" +
                f" {len(player_carrier.segments)} grid spaces to the" +
                " right-hand edge of the map."
                )
            print(
                "You will now choose the row and collumn of the" +
                "left-most segment of the ship."
                )
        else:
            print(
                f"The {player_carrier.type} cannot be closer than" +
                f" {len(player_carrier.segments)} grid spaces to the" +
                " bottom edge of the map."
                )
            print(
                "You will now choose the row and collumn of the" +
                "top-most segment of the ship."
                )
        row_choice = input("Please enter the row number here: ")
        row_validity = player_map_small.validate_row_placement(
            player_carrier.direction, 5, row_choice, number_placed
            )
        if not row_validity:
            place_current_ship_small_invalid_input(number_placed)
        col_choice = input("Please enter the collumn letter here: ").upper()
        collumn_validity = player_map_small.validate_col_place(
            player_carrier.direction, 5, col_choice, number_placed
            )
        if not collumn_validity:
            place_current_ship_small_invalid_input(number_placed)


def place_ships_small_output(validity, choice, number_placed):
    """controls result of user input on ship placement for small maps"""
    if not validity:
        print(
            f"Invalid input, please input one of the following: {SHIP_INPUT}"
            )
        placing_ship(number_placed)

    if choice == "1" or choice == "p" or choice == "place":
        place_current_ship_small(number_placed)
    elif choice == "2" or choice == "r" or choice == "rotate":
        if number_placed == 1:
            if player_carrier.direction == 0:
                player_carrier.direction = 1
            else:
                player_carrier.direction = 0
        elif number_placed == 2:
            if player_battleship.direction == 0:
                player_battleship.direction = 1
            else:
                player_battleship.direction = 0
        elif number_placed == 3:
            if player_submarine.direction == 0:
                player_submarine.direction = 1
            else:
                player_submarine.direction = 0
        elif number_placed == 4:
            if player_destroyer.direction == 0:
                player_destroyer.direction = 1
            else:
                player_destroyer.direction = 0
        elif number_placed == 5:
            if player_gunboat.direction == 0:
                player_gunboat.direction = 1
            else:
                player_gunboat.direction = 0
        placing_ship(number_placed)


def placing_ship(number_placed):
    """function controlling exact process for placing ships"""
    if number_placed == 1:
        if player_carrier.direction == 0:
            print(
                f"Current ship: {player_carrier.type}" +
                f"- {player_carrier.segments}"
                )
            print("Current orientation: Horizontal (left to right)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
        elif player_carrier.direction == 1:
            print(
                f"Current ship: {player_carrier.type}" +
                f"- {player_carrier.segments}"
                )
            print("Current orientation: Vertical (top to bottom)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
    elif number_placed == 2:
        if player_battleship.direction == 0:
            print(
                f"Current ship: {player_battleship.type}" +
                f"- {player_battleship.segments}"
                )
            print("Current orientation: Horizontal (left to right)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
        elif player_battleship.direction == 1:
            print(
                f"Current ship: {player_battleship.type}" +
                f"- {player_battleship.segments}"
                )
            print("Current orientation: Vertical (top to bottom)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
    elif number_placed == 3:
        if player_submarine.direction == 0:
            print(
                f"Current ship: {player_submarine.type}" +
                f"- {player_submarine.segments}"
                )
            print("Current orientation: Horizontal (left to right)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
        elif player_submarine.direction == 1:
            print(
                f"Current ship: {player_submarine.type}" +
                f"- {player_submarine.segments}"
                )
            print("Current orientation: Vertical (top to bottom)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
    elif number_placed == 4:
        if player_destroyer.direction == 0:
            print(
                f"Current ship: {player_destroyer.type}" +
                f"- {player_destroyer.segments}"
                )
            print("Current orientation: Horizontal (left to right)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
        elif player_destroyer.direction == 1:
            print(
                f"Current ship: {player_destroyer.type}" +
                f"- {player_destroyer.segments}"
                )
            print("Current orientation: Vertical (top to bottom)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
    elif number_placed == 5:
        if player_gunboat.direction == 0:
            print(
                f"Current ship: {player_gunboat.type}" +
                f"- {player_gunboat.segments}"
                )
            print("Current orientation: Horizontal (left to right)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)
        elif player_gunboat.direction == 1:
            print(
                f"Current ship: {player_gunboat.type}" +
                f"- {player_gunboat.segments}"
                )
            print("Current orientation: Vertical (top to bottom)")
            print("1. [P]lace")
            print("2. [R]otate")
            choice = input("Please enter your choice here: ")
            validity = valid_start_placing_input(choice)
            place_ships_small_output(validity, choice, number_placed)


def place_ships_small():
    """function controlling ship placing process for small maps"""
    print("Please place your ships.")
    number_placed = 1
    while number_placed < 5:
        placing_ship(number_placed)


def place_ships_medium():
    """function controlling ship placing process for medium maps"""


def place_ships_large():
    """function controlling ship placing process for large maps"""


def start_game(difficulty, size):
    """funtion that controls the game starting"""
    print("YOUR GRID:")
    if size == 0:
        player_map_small.print_grid()
        place_ships_small()
    elif size == 1:
        player_map_medium.print_grid()
        place_ships_medium()
    elif size == 2:
        player_map_large.print_grid()
        place_ships_large()


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
    print("DIFFICULTY")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [E]asy")
    print("2. [N]ormal")
    print("3. [H]ard")
    print("4. [B]ack")
    choice = input("Please enter your choice here: ").lower()
    validity = valid_difficulty_input(choice)
    difficulty_output(validity, choice, difficulty, size)


def valid_map_input(choice):
    """function to check validity of input on map size screen"""

    num = 0
    is_valid = False
    while num < 12:
        if choice == MAP_SIZE_INPUT[num]:
            is_valid = True
            num = 12
        else:
            num += 1
    return is_valid


def map_output(validity, choice, difficulty, size):
    """funtion controls result of user input on map size screen"""
    if not validity:
        print(
            f"Invalid input, please input from the following: {MAP_SIZE_INPUT}"
            )
        map_screen(difficulty, size)

    if choice == "1" or choice == "s" or choice == "small":
        size = 0
        map_screen(difficulty, size)
    elif choice == "2" or choice == "m" or choice == "medium":
        size = 1
        map_screen(difficulty, size)
    elif choice == "3" or choice == "l" or choice == "large":
        size = 2
        map_screen(difficulty, size)
    elif choice == "4" or choice == "b" or choice == "back":
        options_screen(difficulty, size)


def map_screen(difficulty, size):
    """funtion that controls the map size screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)
    print("MAP SIZE")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [S]mall (10x10)")
    print("2. [M]edium (15x15)")
    print("3. [L]arge (20x20)")
    print("4. [B]ack")
    choice = input("Please enter your choice here: ").lower()
    validity = valid_map_input(choice)
    map_output(validity, choice, difficulty, size)


def leaderboard_screen(difficulty, size):
    """function that controls the leaderboard screen"""
    print("placeholder")


menu_screen(0, 0)
