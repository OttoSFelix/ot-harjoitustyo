from search import get_player_base_stats

def base_stats():
    print('Player name (format= Surname Firstname): ', end="")
    name = input('')
    print('------------------------------------------------------')
    print(get_player_base_stats(name))
    print('------------------------------------------------------')
    starting_tui()


def h2h():
    print('Under delevopement')

def starting_tui():
    print('Choose operation  (quit with q)')
    print('Commands: [basestats/h2h]: ', end="")
    operation = input('')
    if operation.strip() == 'basestats':
        base_stats()
    elif operation.strip() == 'h2h':
        h2h()
    elif operation.strip() == 'q':
        quit()
    else:
        print('invalid operation')
        print('')
        starting_tui()

if __name__ == '__main__':
    print("Player Statistics App Version 1.0.0")
    print('----------------------------------')
    starting_tui()

