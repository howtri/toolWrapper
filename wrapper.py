# Tristan Howell
# Designed to wrap around any tool and run that with a passed list as input for CLI arguments on a Linux machine
# Accept any number of args
# Built in safety checks

import argparse
import sys
import subprocess

def main():
    # modify for specific tool for safety checks
    check_for = None
    accepted_cli_args = []
    max_size = 100

    parser = argparse.ArgumentParser(description='Runs bulk actions')
    parser.add_argument('tool_path', metavar='action', type=str,
                        help=f'Path to the tool to use')
    parser.add_argument('input_file_path', metavar='path', type=str,
                        help='Path to file for tool to be ran against for each line in file')
    parser.add_argument('cli_args', metavar='action', type=str,
                        help=f'Action to perform. Options: {accepted_cli_args}')
    args = parser.parse_args()

    # attempts to read in passed args
    try:
        with open(args.input_file_path, 'r') as input_file:
            input = [line.rstrip() for line in input_file if check_for in line]
    except Exception as e:
        print(f'Make this more specific {e}')

    # per apolloCLI --help these are the only allowed actions
    if args.cli_args not in accepted_cli_args:
        print(f'Passed action must be one of the following {accepted_cli_args}')
        sys.exit()

    # to mitigate risk only allows 20 hosts at a time
    if len(input) > max_size:
        print(f'Script accepts max of {max_size}. Exiting!')
        sys.exit()

    # verifies the hosts and action performed with user
    print(*[inputs + '\n' for inputs in input])
    user_accept = input(f'Perform: {args.cli_args} on each of the above inputs? yes/no: ').lower()

    if user_accept != 'yes':
        print(f'User did not accept with answer: {user_accept}')
        sys.exit()

    try:
        # uses subprocess to pass action and input to specified tool
        codes = [subprocess.check_call(f"{args.tool_path} %s %s" % (f'{args.cli_args}', inputs), shell=True)
                 for inputs in input]
    except Exception as e:
        print(f'Encountered error {e}')

    print(f'Complete. Codes (success = 0): {codes}')

if __name__ == '__main__':
    main()