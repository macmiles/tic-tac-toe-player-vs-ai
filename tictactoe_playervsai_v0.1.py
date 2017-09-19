# AUTHOR: SELIM CAM
# DATE: 08.31.2017

import random

p1 = "X"
p2 = 'O'
number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def print_gui(gui_list):
    print(gui_list[0:3])
    print(gui_list[3:6])
    print(gui_list[6:9])

    return gui_list


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

        # cost_result.append({'cells': cells, 'cost': cost})
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

        # cost_result.append({'cells': cells, 'cost': cost})
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
    # cost_result.append({'cells': cells, 'cost': cost})
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
    # cost_result.append({'cells': cells, 'cost': cost})
    cost_result.append({'chosen': chosen, 'available': available})

    return cost_result


def ai_logic(gui):
    cell_selection = []
    # triggers when opponent is one away from winning - ai uses this to defend
    player_cost = cost_check(p1, gui)
    print('Player Cost:', player_cost)
    for each in player_cost:
        if len(each['available']) == 1 and len(each['chosen']) == 2:
            cell_selection = each['available'][0]
            break

    if cell_selection:
        return cell_selection
    else:
        ai_cost = []
        # list keeps track of cells chosen - ai uses this to win
        if gui[4] != p1 and gui[4] != p2:
            gui[4] = p2
            cell_selection = 4
        else:
            ai_cost = cost_check(p2, gui)
            print('AI Cost:', ai_cost)
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

            cell_selection = random.choice(ai_cost[min_cost_index]['available'])
        return cell_selection


def main():
    # winner check
    winner = 0

    # first player goes first
    current_player = 1

    # blank gui
    number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    gui_list = number_list

    # print board for the first time
    print_gui(gui_list)

    while winner == 0:
        # loop to ensure user input is correct
        error_check = 1
        if current_player == 1:
            # USER ACTIONS
            while error_check == 1:
                # selects user input
                x = input('Player %s, please select a cell or type "q" to quit:' % (current_player))

                # if user would like to quit
                if x.lower() == 'q':
                    return

                x = int(x)
                if gui_list[x - 1] == "X" or gui_list[x - 1] == "O":
                    print('Error - that cell is already taken. Please try again.')
                else:
                    error_check = 0

            gui_list[x - 1] = p1
            current_player = 2
        else:
            x = ai_logic(gui_list)
            gui_list[x] = p2
            current_player = 1

        print_gui(gui_list)

        ### CHECK TO SEE IF THE GAME HAS ENDED ###
        winner = check_winner(gui_list)

if __name__ == "__main__":
    main()
