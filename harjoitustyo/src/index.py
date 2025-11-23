from search import get_player_base_stats, top_10_base_stats, get_h2h_record

def base_stats():
    print('Player name (format= Surname Firstname): ', end="")
    name = input('')
    print('------------------------------------------------------')
    print(get_player_base_stats(name))
    print('------------------------------------------------------')
    starting_tui()


def h2h():
    print('Insert player name and opponent name: (format= Surname Firstname, Surname Firstname) ', end='')
    names = input('')
    names = names.split(',')
    name1 = names[0].strip()
    name2 = names[1].strip()
    print('------------------------------------------------------')
    print(get_h2h_record(name1, name2))
    print('------------------------------------------------------')
    starting_tui()


def top10():
    for stat in top_10_base_stats(10):
        print('------------------------------------------------------')
        print(stat)
        print('------------------------------------------------------')
    starting_tui()


def starting_tui():
    print('Choose operation  (quit with q)')
    print('Commands: [basestats/h2h/top10]: ', end="")
    operation = input('')
    if operation.strip() == 'basestats':
        base_stats()
    elif operation.strip() == 'h2h':
        h2h()
    elif operation.strip() == 'q':
        quit()
    elif operation.strip() == 'top10':
        top10()
    else:
        print('invalid operation')
        print('')
        starting_tui()

if __name__ == '__main__':
    print("Player Statistics App Version 1.0.0")
    print('----------------------------------')
    starting_tui()

