## IMPORTS ##

# Import modules
import configparser
import sqlite3
from tabulate import tabulate
from os.path import exists

## MISC CONFIGS ##

# Read configurations
config = configparser.ConfigParser()
config.read('configs/configs.ini')

# Set database file
DATABASE = config['database']['DATABASE']

# Database init
def db_init():
    connection = sqlite3.connect("data/matchtracker.db")
    cursor = connection.cursor()

    return connection, cursor

db_connection, db_cursor = db_init()

# Create tables
def create_tables():
    """
    The function creates two tables in a SQLite database if they do not already exist.
    """

    db_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='players'")
    if db_cursor.fetchone()[0] == 0: {
        db_cursor.execute("CREATE TABLE players(id, name, matches, wins, draws, losses, ratio, points)")
    }

    db_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='matches'")
    if db_cursor.fetchone()[0] == 0: {
        db_cursor.execute("CREATE TABLE matches(id, date, teamA, teamB, result)")
    }

## PLAYER ACTIONS ##

# Create player
def create_player():

    player_name = input("Nome: ")
    db_cursor.execute(f"SELECT * FROM players")
    player_counter = len(db_cursor.fetchall())
    db_cursor.execute(f"INSERT INTO players (id, name, matches, wins, draws, losses, ratio, points) VALUES ('{player_counter}', '{player_name}', 0, 0, 0, 0, '0.00%', 0)")
    db_connection.commit()

    print_players_table()

    add_new_player = input("Queres adicionar outro  jogador? (S / N)")
    if add_new_player == "S":
        create_player()
    if add_new_player == "N":
        menu()

# Read player
def read_players():

    players_data = db_cursor.execute("SELECT * FROM players")

    return players_data

# Delete player
def delete_player():

    print_players_table()

    player_id = input("ID: ")
    db_cursor.execute(f"DELETE FROM players WHERE id = {player_id}")
    db_connection.commit()

    print_players_table()

    delete_new_player = input("Queres apagar outro  jogador? (S / N)")
    if delete_new_player == "S":
        delete_player()
    if delete_new_player == "N":
        menu()

# Print players table
def print_players_table():

    players_table_data = [["ID", "Nome", "Jogos", "Vitorias", "Empates", "Derrotas", "Ratio (%)", "Pontos"]]
    players_table_data += read_players()
    players_table = tabulate(players_table_data, headers = 'firstrow')

    print(players_table)

## MATCH ACTIONS

# Create match
def create_match():

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

    calculate_points(match_teamA, match_teamB, match_result)

# Read match
def read_matches():

    matches_data = db_cursor.execute("SELECT * FROM matches")

    return matches_data

## COMPUTING ##

# Calculate points
def calculate_points(teamA, teamB, result):

    if result == 'A':
        for member in teamA:
            db_cursor.execute(f"UPDATE players SET matches = matches + 1, wins = wins + 1, ratio = ROUND((wins*1.0 / matches*1.0) * 100, 2), points = points + 3 || '%' WHERE name = '{member}'")
            db_connection.commit()
        for member in teamB:
            db_cursor.execute(f"UPDATE players SET matches = matches + 1, losses = losses + 1, ratio = ROUND((wins*1.0 / matches*1.0) * 100, 2) || '%' WHERE name = '{member}'")
            db_connection.commit()

    if result == 'B':
        for member in teamB:
            db_cursor.execute(f"UPDATE players SET matches = matches + 1, wins = wins + 1, ratio = ROUND((wins*1.0 / matches*1.0) * 100, 2), points = points + 3 || '%' WHERE name = '{member}'")
            db_connection.commit()
        for member in teamA:
            db_cursor.execute(f"UPDATE players SET matches = matches + 1, losses = losses + 1, ratio = ROUND((wins*1.0 / matches*1.0) * 100, 2) || '%' WHERE name = '{member}'")
            db_connection.commit()

    if result == 'Empate':
        for member in teamA:
            db_cursor.execute(f"UPDATE players SET matches = matches + 1, draws = draws + 1, ratio = ROUND((wins*1.0 / matches*1.0) * 100, 2), points = points + 1 || '%' WHERE name = '{member}'")
            db_connection.commit()
        for member in teamB:
            db_cursor.execute(f"UPDATE players SET matches = matches + 1, draws = draws + 1, ratio = ROUND((wins*1.0 / matches*1.0) * 100, 2), points = points + 1 || '%' WHERE name = '{member}'")
            db_connection.commit()

# Print match
def print_matches_table():

    matches_table_data = [["ID", "Data", "Equipa A", "Equipa B", "Resultado"]]
    matches_table_data += read_matches()
    matches_table = tabulate(matches_table_data, headers = 'firstrow')

    print(matches_table)

    menu()

## MAIN ##

# Main menu
def menu():

    option = input("Opções:\n1 - Ver tabela\n2 - Criar jogador\n3 - Apagar jogador\n4 - Registar jogo\n5 - Saír\n")
    if option == "1":
        print_players_table()
        menu()
    if option == "2":
        create_player()
    if option == "3":
        delete_player()
    if option == "4":
        create_match()
    if option == "5":
        exit()

if __name__ == '__main__':
    db_init()
    create_tables()
    menu()