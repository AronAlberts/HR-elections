# Define constants
# Receive input from user
# Decide what, if any, is the action of the program depending on the input
# Open relevant file
# Display information from that file to the user in a neat manner
# Close file

# Constants
CONSTITUENCIES = '1'
PARTIES = '2'
RESULTS = '3'
QUIT = '9'


def main():
    determine_action()


def determine_action():
    ''' Main loop, determines action based on user input '''

    action = get_user_action()

    constituencies_loaded = False
    parties_loaded = False
    results_loaded = False
    constituencies_dict = None
    parties_dict = None

    while action != QUIT:
        if action == CONSTITUENCIES:
            if constituencies_loaded:
                print_constit_table(constituencies_dict)
            else:
                constituencies_dict, constituencies_loaded = \
                    handle_constituencies()
        elif action == PARTIES:
            if parties_loaded:
                print_parties_table(parties_dict)
            else:
                parties_dict, parties_loaded = handle_parties()
        elif action == RESULTS:
            if results_loaded:
                print_results_table(results_dict,
                                    constituencies_dict, parties_dict)
            else:
                results_dict, results_loaded\
                    = handle_results(constituencies_dict, parties_dict)

        action = get_user_action()


def get_user_action():
    ''' Receives input that will decide the flow of the program '''

    action = input('''\n1. Show constituencies
2. Show parties
3. Show results
9. Quit

Select an action: ''')

    return action


def handle_constituencies():
    ''' Handles actions related to displaying constituencies data '''

    filename = input('File name: ')

    constituencies_dict = read_file_to_dict(filename)
    if constituencies_dict is None:
        constituencies_loaded = False
    else:
        print_constit_table(constituencies_dict)
        constituencies_loaded = True

    return (constituencies_dict, constituencies_loaded)


def handle_parties():
    '''Handles actions related to displaying parties data '''

    filename = input('File name: ')

    parties_dict = read_file_to_dict(filename)
    if parties_dict is None:
        parties_loaded = False
    else:
        print_parties_table(parties_dict)
        parties_loaded = True

    return (parties_dict, parties_loaded)


def handle_results(constituencies_dict, parties_dict):
    ''' Handles actions related to displaying results data '''

    filename = input('File name for results: ')

    if constituencies_dict is not None and parties_dict is not None:
        results_dict = results_to_dict(filename, parties_dict)
        if results_dict is None:
            results_loaded = False
        else:
            print_results_table(results_dict,
                                constituencies_dict, parties_dict)
            results_loaded = True
    else:
        results_loaded = False
        results_dict = None

    return (results_dict, results_loaded)


def read_file_to_dict(filename):
    ''' Reads contents of file and returns them a dictionary '''

    try:
        with open(filename, 'r') as file:
            lines_list = file.read().splitlines()
            key_value_list = [item.split(';') for item in lines_list]
            file_dict = {item[0]: item[1] for item in key_value_list}
    except FileNotFoundError:
        file_dict = None

    return file_dict


def print_constit_table(file_dict):
    ''' Prints constituency data in neat looking table '''

    try:
        print('\n''{:<20}{:>10}'.format('Constituency', 'Electorals'))
        print('-' * 30)

        for constit, electorals in file_dict.items():
            print('{:<20}{:>10}'.format(constit, electorals))

        print('-' * 30)

        sum_electorals = get_sum_electorals(file_dict)

        print('{:<20}{:>10}'.format('Total:', sum_electorals))
    except AttributeError:
        pass


def get_sum_electorals(file_dict):
    ''' Returns sum of electorals for all constituencies '''

    sum_values = 0

    for value in file_dict.values():
        value = int(value)
        sum_values += value

    return sum_values


def print_parties_table(parties_dict):
    ''' Prints list of parties in a neat table '''

    print_parties_header()

    print_parties_body(parties_dict)


def print_parties_body(parties_dict):
    ''' Prints body of parties table '''

    for a_list, party in parties_dict.items():
        print('{:<6}{:>26}'.format(a_list, party),)


def print_parties_header():
    ''' Prints header of parties table '''

    print('\n''{:<6}{:>26}'.format('List', 'Party'))
    print('-' * 32)


def get_number_of_parties(parties_dict):
    ''' Returns number of parties as int '''

    try:
        parties_list = [party for party in parties_dict]
        num_parties = len(parties_list)
    except TypeError:
        num_parties = None

    return num_parties


def results_to_dict(filename, parties_dict):
    ''' Reads contents of results file into dictionary '''

    if len(parties_dict) == 0:
        results_dict = None
    else:
        try:
            with open(filename, 'r') as file:
                lines_list = file.read().splitlines()
                results_keys_list = get_keys_list(parties_dict, lines_list)
                results_values_list = get_values_list(parties_dict,
                                                      lines_list)
                results_dict = make_results_dict(parties_dict,
                                    results_keys_list, results_values_list)
        except FileNotFoundError:
            results_dict = None

    return results_dict


def make_results_dict(parties_dict, results_keys_list, results_values_list):
    ''' Returns a dictionary where the keys are constituencies and the
    values are parties and their respective votes '''

    results_dict = {
        results_keys_list[i]: results_values_list[
            i * len(parties_dict): (i + 1) * len(parties_dict)
            ] for i in range(len(results_keys_list))
        }

    return results_dict


def get_values_list(parties_dict, lines_list):
    ''' Returns list of tuples to be used as values for results dictionary '''

    results_values_list = [
        tuple(
            lines_list[i].split(';')
            ) for i in range(
                len(lines_list)
                ) if i % (len(parties_dict) + 1) != 0
        ]

    return results_values_list


def get_keys_list(parties_dict, lines_list):
    ''' Returns list of values to be used as keys for results dictionary '''

    results_keys_list = [
        lines_list[i] for i in range(0, len(lines_list), len(parties_dict) + 1)
        ]

    return results_keys_list


def print_results_table(results_dict,
                        constituencies_dict, parties_dict):
    ''' Prints a neat table for voting results in a single constituency '''

    constit_to_search = (input('Constituency: '))

    total_votes = get_total_votes(results_dict, constit_to_search)
    if total_votes is None:
        pass
    else:
        turnout_float = get_voter_turnout(constit_to_search,
                                          total_votes, constituencies_dict)

        print_results_header(constit_to_search)
        print_results_body(results_dict, constit_to_search,
                           parties_dict, total_votes)

        print_results_footer(total_votes, turnout_float)


def print_results_header(constit_to_search):
    ''' Prints header for results table '''

    print(f'\n{constit_to_search}')
    print('{:<10}{:>26}{:>10}{:>10}'.format('List', 'Party', 'Votes', 'Ratio'))
    print('-' * 56)


def print_results_body(results_dict, constit_to_search,
                       parties_dict, total_votes):
    ''' Prints body of results table '''

    for tup in results_dict[constit_to_search]:
        party = parties_dict[tup[0]]
        votes = tup[1]
        votes = int(votes)
        ratio = (votes / total_votes) * 100
        print('{:<10}{:>26}{:>10}{:>10.1f}'.format(
            tup[0], party, tup[1], ratio
            ))


def print_results_footer(total_votes, turnout_float):
    print('-' * 56)
    print('{:<36}{:>10}{:>10}'.format('Total:', total_votes, '100.0'))
    print('{:<46}{:>10.1f}'.format('Turnout:', turnout_float))


def get_voter_turnout(constit_to_search, total_votes, constituencies_dict):
    ''' Gets voter turnout percentage '''

    num_voters = constituencies_dict[constit_to_search]
    num_voters = int(num_voters)
    turnout = (total_votes / num_voters) * 100

    return turnout


def get_total_votes(results_dict, constit_to_search):
    ''' Returns total votes for given constituency '''

    total_votes = 0
    try:
        for tup in results_dict[constit_to_search]:
            votes = tup[1]
            votes = int(votes)
            total_votes += votes
    except KeyError:
        total_votes = None

    return total_votes


main()
