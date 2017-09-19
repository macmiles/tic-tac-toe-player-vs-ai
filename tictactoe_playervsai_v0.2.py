# AUTHOR: SELIM CAM
# DATE: 09.05.2017

import random

# set value to 1 to see additional print info and to better understand how the AI algorithm makes decisions
debug_mode = 0

# default user symbols; p1 (player 1) is you, and p2 (player 2) is the AI
p1 = "X"
p2 = 'O'
number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def print_gui(gui_board):
    print(gui_board[0:3])
    print(gui_board[3:6])
    print(gui_board[6:9])

    return gui_board


def check_winner(gui):
    winner = 0

    # horizontal check - P1 & P2
    for i in range(3):
        if gui[0 + (i * 3)] == p1 and gui[1 + (i * 3)] == p1 and gui[2 + (i * 3)] == p1:
            winner = 1
            break
        if gui[0 + (i * 3)] == p2 and gui[1 + (i * 3)] == p2 and gui[2 + (i * 3)] == p2:
            winner = 2
            break

    # vertical check - P1 & P2
    for j in range(3):
        if gui[0 + j] == p1 and gui[3 + j] == p1 and gui[6 + j] == p1:
            winner = 1
            break
        if gui[0 + j] == p2 and gui[3 + j] == p2 and gui[6 + j] == p2:
            winner = 2
            break

    # diagonal check - P1
    if gui[0] == p1 and gui[4] == p1 and gui[8] == p1:
        winner = 1
    if gui[2] == p1 and gui[4] == p1 and gui[6] == p1:
        winner = 1

    # diagonal check - P2
    if gui[0] == p2 and gui[4] == p2 and gui[8] == p2:
        winner = 2
    if gui[2] == p2 and gui[4] == p2 and gui[6] == p2:
        winner = 2

    if winner == 1 or winner == 2:
        if winner == 1:
            print('Vitory, player wins!')
        else:
            print('Defeat, computer wins...')

        y = input('Would you like to play again?')
        if y.lower() == 'yes' or y.lower() == 'y':
            main()

    available_cell_count = 0
    for each in gui:
        if each in number_list:
            available_cell_count += 1

    if available_cell_count == 0:
        y = input('Game has ended in a tie. Would you like to play again?')
        if y.lower() == 'yes' or y.lower() == 'y':
            main()

    return winner


def cost_check(turn, gui):
    # list stores all the possible moves and their respective costs to win using that route
    cost_result = []

    if turn == p1:
        opponent = p2
    else:
        opponent = p1

    # horizontal check
    for i in range(3):
        range_index = [0 + (i * 3), 1 + (i * 3), 2 + (i * 3)]
        chosen = []
        available = []
        for k in range_index:
            if gui[k] in number_list:
                available.append(k)
            elif gui[k] == turn:
                chosen.append(k)

        cost_result.append({'chosen': chosen, 'available': available})

    # vertical check
    for j in range(3):
        range_index = [0 + j, 3 + j, 6 + j]
        chosen = []
        available = []
        for k in range_index:
            if gui[k] in number_list:
                available.append(k)
            elif gui[k] == turn:
                chosen.append(k)

        cost_result.append({'chosen': chosen, 'available': available})

    # diagonal 1 check
    range_index = [0, 4, 8]
    chosen = []
    available = []
    for k in range_index:
        if gui[k] in number_list:
            available.append(k)
        elif gui[k] == turn:
            chosen.append(k)

    cost_result.append({'chosen': chosen, 'available': available})

    # diagonal 2 check
    range_index = [2, 4, 6]
    chosen = []
    available = []
    for k in range_index:
        if gui[k] in number_list:
            available.append(k)
        elif gui[k] == turn:
            chosen.append(k)

    cost_result.append({'chosen': chosen, 'available': available})

    return cost_result


def ai_logic(gui):
    cell_selection = []
    # pulls cost analysis for all the possible moves the player can make
    player_cost = cost_check(p1, gui)

    # pulls cost analysis for all the possible moves the AI can make
    ai_cost = cost_check(p2, gui)

    # if debug mode is activated, player and ai cost analysis for all possible moves is diplayed
    if debug_mode == 1:
        print('Player Cost:', player_cost)
        print('AI Cost:', ai_cost)

    ai_cell_selection = []
    player_cell_selection = []

    # check to see if player is one move away from winning
    for each in player_cost:
        if len(each['available']) == 1 and len(each['chosen']) == 2:
            player_cell_selection.append(each['available'][0])
            break

    # check to see if AI is one move away from winning
    for each in ai_cost:
        if len(each['available']) == 1 and len(each['chosen']) == 2:
            ai_cell_selection.append(each['available'][0])
            break

    # check to see if player or AI is one move away from winning
    if player_cell_selection or ai_cell_selection:
        # if AI is one move away from winning, then always go with AI's last cell first; otherwise, block the player's last cell
        if ai_cell_selection:
            cell_selection = ai_cell_selection[0]
        else:
            cell_selection = player_cell_selection[0]
    else:
        # list keeps track of cells chosen - ai uses this to win
        if gui[4] != p1 and gui[4] != p2:
            gui[4] = p2
            cell_selection = 4
        else:
            # find the min cost move
            min_cost_value = 99999
            min_cost_index = 0
            for z, each in enumerate(ai_cost):
                # cell count will be equal to 3 if opponent hasn't select a cell in this block of cells
                cell_count = len(each['available']) + len(each['chosen'])
                if cell_count == 3:
                    if len(each['available']) < min_cost_value:
                        min_cost_value = len(each['available'])
                        min_cost_index = z

            cell_selection = random.choice(
                ai_cost[min_cost_index]['available'])

    return cell_selection


def main():
    # winner check
    winner = 0

    # player gets to go first because humans > AI
    current_player = 1

    # blank grid
    grid = number_list

    # print tic-tac-toe grid for the first time
    print_gui(grid)

    # loops until there's a winner or all the cells on the grid are full
    while winner == 0:
        error_check = 1
        if current_player == 1:  # USER ACTIONS
            # continuous loop used for error validation
            while error_check == 1:
                # selects user input
                x = input(
                    'Player %s, please select a cell or type "q" to quit:' % (current_player))

                # input value of 'q' quits the app
                if x.lower() == 'q':
                    return

                # convert string input to an int
                x = int(x)

                # validation to check if the chosen cell is empty
                if grid[x - 1] == "X" or grid[x - 1] == "O":
                    print('Error - that cell is already taken. Try again.')
                else:
                    error_check = 0

            grid[x - 1] = p1
            current_player = 2
        else:  # AI ACTIONS
            # logic determines best possible move for AI
            x = ai_logic(grid)

            # best possible move for AI is executed
            grid[x] = p2

            # switches turns
            current_player = 1

        # print current state of tic-tac-toe board
        print_gui(grid)

        # check if the game has ended
        check_winner(grid)


if __name__ == "__main__":
    main()
