from Model.Ship import Ship
from Model.Player import Player


def __main__():
    """
    For prototyping purposes only. Will be used to model the final game loop.
    The basic structure of the game loop.
    :return: None
    """
    # ask for dims
    game_dims = get_dims()
    player_name = get_player_name()
    # Create the player object
    player = Player(player_name, game_dims)
    ships = get_ships()  # Get description of the fleet

    for ship in ships:
        player.add_my_ship(ship)

    # transmit boat types to opponent
    send_ship_types(ships)
    # get enemy's boat types
    opp_ship_types = get_ship_types()
    print("Here are opp's ship_types:", opp_ship_types)

    game_on = True

    while game_on:
        change_turn = False
        while not change_turn:
            change_turn, game_on = your_move(player)  # Play a move

        change_turn = False
        while game_on and not change_turn:
            change_turn, game_on = opp_move(player)  # Respond to enemy's move


def your_move(player: Player) -> (bool, bool):
    """
    Utility function to simulate your move on the opponent's board.
    :param player: Player object.
    :return: (Bool, Bool) : change_turn and game_on booleans indicating whether to
                            reverse the turn and whether the game is not over.
    """
    change_turn = False
    game_on = True
    print("Opponent's Board\n", player.opp_board)
    # get a move from player and execute it
    move = get_move()
    # update opp board based on their response
    response = get_response(move)
    if response == 1:
        # hit a ship, but not destroyed
        player.opp_board.mark_ship_hit(move)
        player.opp_board.update_redundant_squares(move, False)
    elif response == 2:
        # hit a ship and destroyed, but not won yet
        player.opp_board.mark_ship_hit(move)
        player.opp_board.update_redundant_squares(move, True)
    elif response == 3:
        # hit a ship and destroyed and won
        player.opp_board.mark_ship_hit(move)
        player.opp_board.update_redundant_squares(move, True)
        game_on = False
        change_turn = True
        print("You Won")
    elif response == 0:
        # missed
        player.opp_board.mark_ship_miss(move)
        change_turn = True
    else:
        # invalid move
        print("Invalid Move")

    return change_turn, game_on


def opp_move(player: Player) -> (bool, bool):
    """
    Utility function to simulate opponent's moves on your board.
    :param player: Player object
    :return: (Bool, Bool) : change_turn and game_on booleans indicating whether to
                            reverse the turn and whether the game is not over.
    """
    change_turn = False
    game_on = True
    print("Your Board\n", player.my_board)
    opp_move = get_move()  # Get opponent's move
    hit_resp = player.my_board.hit(opp_move)  # Execute the move
    if hit_resp == 1:
        if player.my_board.ship_destroyed(opp_move):
            player.my_board.update_redundant_squares(opp_move, True)
            if player.my_board.all_ships_destroyed():
                hit_resp = 3
                game_on = False
                print("You Lost")
            else:
                hit_resp = 2
        else:
            player.my_board.update_redundant_squares(opp_move)
    else:
        change_turn = True

    # send a response
    send_response(hit_resp)

    return change_turn, game_on


def get_move() -> tuple:
    """
    Utility function to get the player's move.
    :return: tuple of the move
    """
    return get_tuple('What move to make?')


def get_response(move) -> int:
    """
    Utility function to enter the response to a move.
    :param move: The move to which to respond.
    :return: 1: hit, 2: hit and ship destroyed, 3: game over, you win, -1: miss
    """
    print("Move made:", move)
    return int(input('What response to return?'))


def get_dims() -> tuple:
    """
    Utility function to get the dimensions of the board to use.
    :return: tuple of the dimensions to use.
    """
    return get_tuple('What dimensions to use?')


def get_tuple(prompt) -> tuple:
    """
    Utility function to get user input in the form of a tuple.
    :param prompt: The prompt to display while asking for user input.
    :return: tuple entered by the user in response to the prompt.
    """
    resp = input(prompt)
    resp = resp.split(",")
    resp = list(map(str.strip, resp))
    resp = list(map(int, resp))
    return tuple(resp)


def get_player_name() -> str:
    """
    Utility fill-in function to get player's name.
    :return: string of player's name
    """
    return 'Sahil'


def get_ships() -> list:
    """
    Utility function to get description of ships to place on the grid.
    :return: list of ship objects.
    """
    done = False
    ships = []
    while not done:
        ship_loc = get_tuple('Input ship location')
        ship_len = int(input('Length?'))
        ship_dir = get_tuple('Input direction')
        ships.append(Ship(ship_loc, ship_len, ship_dir))
        done = True if int(input('Done?')) == 1 else False

    return ships


def send_ship_types(ships: list):
    """
    Utility function to transmit your ship types to the opponent.
    :param ships: List of ship objects
    :return: None
    """
    ship_lens = {}
    for ship in ships:
        if ship.length not in ship_lens:
            ship_lens[ship.length] = 0
        ship_lens[ship.length] += 1
    print("Here are the ship types.", ship_lens)


def get_ship_types() -> dict:
    """
    Utility function to get the types of ships in opponent's fleet.
    :return: Dictionary of mappings from ship length to number of ships of that length
    """
    print("Enter ship_len, ship_freqs")
    ship_types = {}
    done = False
    while not done:
        resp = get_tuple("Enter ship_len, ship_freq")
        ship_types[resp[0]] = resp[1]
        done = True if int(input("Done?")) == 1 else False

    return ship_types


def send_response(response: int):
    """
    Utility function to send a response to the user.
    :param response: int, 1 if hit, 2 if ship destroyed, 3 if win, -1 if miss
    :return: None
    """
    print("Received response", response)


if __name__ == '__main__':
    __main__()

