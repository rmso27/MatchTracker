import json
import configparser
from tabulate import tabulate
import sqlite3

# Read configurations
config = configparser.ConfigParser()
config.read('configs/configs.ini')

# `DATABASE = config['database']['DATABASE']` is reading the value of the `DATABASE` key from the
# `database` section of the `configs.ini` file and assigning it to the `DATABASE` variable. This value
# is used as the name of the SQLite database file that the program will connect to.
DATABASE = config['database']['DATABASE']

# Database init
def db_init():
    connection = sqlite3.connect("data/matchtracker.db")
    cursor = connection.cursor()

    return connection, cursor

# `db_connection, db_cursor = db_init()` is initializing a connection to a SQLite database and
# returning both the connection and cursor objects. The connection object is used to connect to the
# database and the cursor object is used to execute SQL queries on the database. The returned objects
# are then assigned to the variables `db_connection` and `db_cursor`, respectively, so that they can
# be used throughout the program to interact with the database.
db_connection, db_cursor = db_init()

def create_tables():
    """
    The function creates two tables in a database, one for players and one for matches.
    """

    db_cursor.execute("CREATE TABLE players(id, name, matches, wins, draws, losses, ratio, points)")
    db_cursor.execute("CREATE TABLE matches(id, date, teamA, teamB, result)")

# create_tables()

def create_player():
    """
    This function creates a new player in a database and allows the user to add more players if desired.
    """

    player_name = input("Nome: ")
    db_cursor.execute(f"INSERT INTO players (id, name, matches, wins, draws, losses, ratio, points) VALUES (0, '{player_name}', 0, 0, 0, 0, '0.00%', 0)")
    db_connection.commit()

    print_players_table()

    add_new_player = input("Queres adicionar outro  jogador? (S / N)")

    if add_new_player == "S":
        create_player()
    if add_new_player == "N":
        exit()

def read_players():
    """
    This function reads all the data from the "players" table in a database and returns it.
    :return: the result of the SQL query "SELECT * FROM players" executed on the database cursor object.
    This query is fetching all the data from the "players" table in the database. The returned value is
    likely a collection of rows or a cursor object that can be iterated over to access the data.
    """

    players_data = db_cursor.execute("SELECT * FROM players")

    return players_data

def delete_player():

    return 0

def create_match():
    """
    This function creates a new match by taking input for the match date, team A and team B players, and
    the match result, and then inserts this information into a database table.
    """

    match_date = input("Data: ")

    counter = 0
    match_teamA = []

    while counter != 5:
        match_teamA += [input(f"Equipa A {counter + 1}: ")]
        counter += 1

    match_teamA = str(match_teamA).replace("'", '"')

    counter = 0
    match_teamB = []

    while counter != 5:
        match_teamB += [input(f"Equipa B {counter + 1}: ")]
        counter += 1

    match_teamB = str(match_teamB).replace("'", '"')

    match_result = input("Result (A / B / Empate): ")

    db_cursor.execute(f"INSERT INTO matches (id, date, teamA, teamB, result) VALUES (0, '{match_date}', '{match_teamA}', '{match_teamB}', '{match_result}')")
    db_connection.commit()

    print_matches_table()

def read_matches():
    """
    This function reads all the data from the "matches" table in a database and returns it.
    :return: The function `read_matches()` is returning the result of the SQL query "SELECT * FROM
    matches" executed using the database cursor. The result is a collection of data representing all the
    matches in the database table "matches".
    """

    matches_data = db_cursor.execute("SELECT * FROM matches")

    return matches_data

def print_matches_table():
    """
    This function prints a table of matches data, including the ID, date, team A, team B, and result.
    """

    matches_table_data = [["ID", "Data", "Equipa A", "Equipa B", "Resultado"]]
    matches_table_data += read_matches()
    matches_table = tabulate(matches_table_data, headers = 'firstrow')

    print(matches_table)

def print_players_table():
    """
    This function prints a table of players' data, including their ID, name, number of games played,
    number of wins, draws, losses, ratio, and points.
    """

    players_table_data = [["ID", "Nome", "Jogos", "Vitorias", "Empates", "Derrotas", "Ratio", "Pontos"]]
    players_table_data += read_players()
    players_table = tabulate(players_table_data, headers = 'firstrow')

    print(players_table)

## MAIN ##

# The `if __name__ == '__main__':` block is the entry point of the program. It checks if the current
# module is being run as the main program (as opposed to being imported as a module into another
# program). If it is the main program, it initializes the database connection by calling the
# `db_init()` function, and then prompts the user to select an option from a menu of choices.
# Depending on the user's choice, it calls one of the functions `print_players_table()`,
# `create_player()`, `delete_player()`, or `create_match()` to perform a specific action related to
# managing player and match data in the database.
if __name__ == '__main__':
    db_init()
    option = input("Opções:\n1 - Ver tabela\n2 - Criar jogador\n3 - Apagar jogador\n4 - Registar jogo\n")
    if option == "1":
        print_players_table()
    if option == "2":
        create_player()
    if option == "3":
        delete_player()
    if option == "4":
        create_match()