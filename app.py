# PYTHON BASED TIC-TAC-TOE GAME WITH A WORKING AI
# AUTHOR: SELIM CAM
# DATE: 09.22.2017

#  X | O | X
# --- --- ---
#  O | X | O
# --- --- ---
#  X | O | X

import random

# set value to 1 to better understand how the AI algorithm makes decisions
debug_mode = 0

# default user symbols
player = "X"
ai = 'O'

# default grid list
number_list = list(range(1, 10))
corner_list = [1, 3, 7, 9]


def print_gui(grid):
    print('')
    print(' %s | %s | %s ' % (grid[0], grid[1], grid[2]))
    print('--- --- ---')
    print(' %s | %s | %s ' % (grid[3], grid[4], grid[5]))
    print('--- --- ---')
    print(' %s | %s | %s ' % (grid[6], grid[7], grid[8]))
    print('')


def check_winner(grid):
    # winner = 0 (default), 1 (player wins), 2 (ai wins), 3 (tie)
    winner = 0

    turn_list = [player, ai]

    for turn in turn_list:
        # horizontal check
        for i in range(3):
            if grid[0 + (i * 3)] == turn and grid[1 + (i * 3)] == turn and grid[2 + (i * 3)] == turn:
                if turn == player:
                    winner = 1
                else:
                    winner = 2
                break

        # vertical check
        for j in range(3):
            if grid[0 + j] == turn and grid[3 + j] == turn and grid[6 + j] == turn:
                if turn == player:
                    winner = 1
                else:
                    winner = 2
                break

        # diagonal check
        if grid[0] == turn and grid[4] == turn and grid[8] == turn:
            if turn == player:
                winner = 1
            else:
                winner = 2
            break
        if grid[2] == turn and grid[4] == turn and grid[6] == turn:
            if turn == player:
                winner = 1
            else:
                winner = 2
            break

    # checks to see how many of the cells in the grid have been selected
    selected_cells = 0
    for each in grid:
        if each not in number_list:
            selected_cells += 1
    
    # if all cells in the grid have been selected and there's still no winner, we have a tie game (winner == 3)
    if selected_cells == 9:
        winner = 3

    return winner


def cost_check(turn, grid):
    # grid stores all the possible moves and their respective costs to win using that route
    cost_result = []

    # determine who opponent is
    if turn == player:
        opponent = ai
    else:
        opponent = player

    # horizontal check
    for i in range(3):
        range_index = [0 + (i * 3), 1 + (i * 3), 2 + (i * 3)]
        chosen = []
        available = []
        for k in range_index:
            if grid[k] in number_list:
                available.append(k + 1)
            elif grid[k] == turn:
                chosen.append(k + 1)

        cost_result.append({'chosen': chosen, 'available': available})

    # vertical check
    for j in range(3):
        range_index = [0 + j, 3 + j, 6 + j]
        chosen = []
        available = []
        for k in range_index:
            if grid[k] in number_list:
                available.append(k + 1)
            elif grid[k] == turn:
                chosen.append(k + 1)

        cost_result.append({'chosen': chosen, 'available': available})

    # diagonal 1 check
    range_index = [0, 4, 8]
    chosen = []
    available = []
    for k in range_index:
        if grid[k] in number_list:
            available.append(k + 1)
        elif grid[k] == turn:
            chosen.append(k + 1)

    cost_result.append({'chosen': chosen, 'available': available})

    # diagonal 2 check
    range_index = [2, 4, 6]
    chosen = []
    available = []
    for k in range_index:
        if grid[k] in number_list:
            available.append(k + 1)
        elif grid[k] == turn:
            chosen.append(k + 1)

    cost_result.append({'chosen': chosen, 'available': available})

    return cost_result


def ai_logic(grid):
    # pulls cost analysis for all the possible moves the player can make
    player_cost = cost_check(player, grid)

    # pulls cost analysis for all the possible moves the AI can make
    ai_cost = cost_check(ai, grid)
    
    # if debug mode is activated (debug_mode == 1), player and ai cost analysis for all possible moves is diplayed
    if debug_mode == 1:
        print('### Player Cost:', player_cost)
        print('### AI Cost:', ai_cost)

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
        if grid[4] != player and grid[4] != ai:
            cell_selection = 5
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

            # if there are no viable moves for the AI to win and the player isn't one move away from winning, the else condition will trigger and the first available move is selected by the AI
            if min_cost_value != 99999:
                cell_selection = random.choice(
                    ai_cost[min_cost_index]['available'])
                for each in ai_cost[min_cost_index]['available']:
                    if each in corner_list:
                        cell_selection = each
                        break
            else:
                for each in ai_cost:
                    if len(each['available']) > 0:
                        cell_selection = random.choice(each['available'])
                        break

    return cell_selection


def main():
    # app header
    print(
        'TIC-TAC-TOE GAME BY SELIM CAM [NOTE: enter "q" to quit at any time]')
    print('===================================================================')

    # set winner to default value
    winner = 0

    # player gets to go first because humans > AI
    current_player = 1

    # grid is set to a default list of values 1-9 
    grid = number_list[:]

    # print tic-tac-toe grid for the first time
    print_gui(grid)

    # loops until there's a winner or all the cells on the grid are full
    while winner == 0:
        error_check = 0

        if current_player == 1:  # USER ACTIONS
            # continuous loop used for error validation
            while error_check == 0:
                # selects user input
                x = input(">> It's your move, please choose a cell: ")

                # input value of 'q' quits the app
                if x.lower() == 'q':
                    return

                try:
                    # convert string input to an int
                    x = int(x)

                    # checks to see if the input is a value between 1-9
                    if x not in number_list:
                        print(
                            'Error - enter a number between 1-9 to select a cell on the grid.')
                    else:
                        # validation to check if the chosen cell is empty
                        if grid[x - 1] not in number_list:
                            print('Error - that cell is already taken. Try again.')
                        else:
                            error_check = 1  # if this executes, then error check was passed
                except ValueError:
                    print(
                        'Error - make sure to enter a number. Preferably one that\'s between 1-9.')
            
            # execute the players move
            grid[x - 1] = player
            
            # switch turns
            current_player = 2
        else:  # AI ACTIONS
            # logic determines best possible move for AI
            x = ai_logic(grid)

            print('## AI HAS PICKED CELL %s ##' % (x))

            # executes best possible move for AI
            grid[x - 1] = ai

            # switch turns
            current_player = 1

        # check if the game has ended
        winner = check_winner(grid)

        # print current state of tic-tac-toe board after AI's turn or after the game has ended
        if current_player == 1 or winner != 0:
            print_gui(grid)

        # remind the user that he's a mere mortal and will probably never win
        if winner != 0:
            if winner == 1:
                print("Victory! Congrats you have achieved the impossible.")
            elif winner == 2:
                print("Defeat! It's okay, you have proven that you're only human. Well, a blind human. Honestly, how did you not see that?")
            elif winner == 3:
                print("Tie. Can't say I didn't see that coming.")

            # prompt user to try again
            y = input(">> Care to try again? [y/n] ")
            if y.lower() == 'yes' or y.lower() == 'y':
                main()


if __name__ == "__main__":
    main()
