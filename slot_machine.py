import random

# Maximum number of horizontal lines the player can bet on
MAX_LINES = 3

# Betting limits per line
MAX_BET = 100
MIN_BET = 1

# Slot machine grid size (3 rows x 3 columns)
ROWS = 3
COLS = 3

# How many times each symbol appears in the "symbol pool"
# More copies => more likely to be picked
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

# Payout multiplier for each symbol (higher is better)
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns, lines, bet, values):
    """
    Checks the first `lines` horizontal lines (rows) for wins.

    `columns` is a list of columns, like:
      columns = [
        ["A","B","C"],  # column 1 (top/mid/bottom)
        ["D","B","A"],  # column 2
        ["C","B","D"],  # column 3
      ]

    If a given row has the same symbol across ALL columns, it is a winning line.
    Winnings for that line = values[symbol] * bet
    """
    winnings = 0
    winnings_lines = []

    # Loop through each line the user bet on (0,1,2 for top/mid/bottom)
    for line in range(lines):
        # Take the symbol from the first column in that row as the "target" symbol
        symbol = columns[0][line]

        # Check the same row across each column to see if all match
        for colum in columns:
            # NOTE: This line is intended to get the symbol at this row in the current column,
            # but as written it indexes columns by line (so it returns a whole column).
            # You asked not to change code logic, so this is left as-is.
            symbol_to_check = columns[line]

            # If any column doesn't match the target symbol, this line is not a win
            if symbol != symbol_to_check:
                break
        else:
            # The `else` on a `for` runs only if the loop did NOT hit `break`,
            # meaning the entire line matched across columns.
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)  # +1 because lines are shown to users starting at 1

    return winnings, winnings_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Generates a random slot "spin" result.

    Returns `columns`, a list of `cols` columns, each containing `rows` symbols.
    Example return shape for 3x3:
      [
        ["C","D","A"],
        ["B","A","D"],
        ["D","C","C"]
      ]
    """
    all_symbols = []

    # Build a list containing each symbol repeated by its count:
    # e.g., with A:2 and B:4, we add 'A' twice and 'B' four times, etc.
    for symbol, symbol_count in symbols.items():  # .items() gives (key, value)
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []

    # Create each column one at a time
    for col in range(cols):
        column = []

        # Make a fresh copy so each column starts with the full pool
        current_symbols = all_symbols[:]  # shallow copy

        # Pick `rows` symbols for this column
        for row in range(rows):
            value = random.choice(current_symbols)  # pick a random symbol
            current_symbols.remove(value)           # remove so it won't repeat in the same column
            column.append(value)                    # store into this column

        columns.append(column)

    return columns


# Print slot machine results in a nice grid
def print_slot_machine(columns):
    # Loop through each row index (0..2)
    for row in range(len(columns[0])):
        # For each row, print one symbol from each column
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                # end=" | " keeps printing on the same line separated by |
                print(column[row], end=" | ")
            else:
                # Last column: no separator at the end
                print(column[row], end="")
        # Move to the next printed line after finishing the row
        print()


def deposit():
    """
    Ask the user to deposit money until they enter a valid positive number.
    Returns the deposit as an integer.
    """
    while True:
        amount = input("what would you like to deposit? $")

        # isdigit() checks if the string contains only digits (no minus sign, no decimals)
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("please enter a number")
    return amount


# Get number of lines the player wants to bet on
def get_number_lines():
    while True:
        lines = input("enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")

        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("enter a valid number.")
        else:
            print("Enter a valid number")
    return lines


def get_bet():
    """
    Ask user for a bet amount per line until they enter a valid number
    between MIN_BET and MAX_BET.
    """
    while True:
        amount = input("what would you like to bet on each line? $")

        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"amount must be between ${MIN_BET} - ${MAX_BET} ")
        else:
            print("Enter a valid number")
    return amount


def spin(balance):
    """
    Runs one round of the slot machine:
      - ask how many lines to bet on
      - ask bet per line
      - ensure total bet <= balance
      - spin + print slot
      - compute winnings
      - return net change (winnings - total_bet)
    """
    lines = get_number_lines()

    while True:
        bet = get_bet()
        total_bet = bet * lines

        # Prevent betting more than you have
        if total_bet > balance:
            print(
                f"you ain't have enough to bet that amount, your current balance is: ${balance} "
            )
        else:
            break

    print(f"you are betting ${bet} on {lines}. total bet is equal to: ${total_bet}")

    # Generate the slot results and print them
    slot = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slot)

    # Determine how much was won
    winnings, winnings_lines = check_winnings(slot, lines, bet, symbol_value)
    print(f"you won {winnings}")
    print(f"you won on lines:", *winnings_lines)

    # Return how much the balance should change by for this spin
    return winnings - total_bet


def main():
    # Initial money
    balance = deposit()

    # Main game loop
    while True:
        print(f"current balance is ${balance}")
        answer = input("press enter to play (q to quit)")

        # Quit condition
        if answer == "q":
            break

        # Add net win/loss from a spin
        balance += spin(balance)

    # Final result
    print(f"you left with ${balance}")


# Run the program
main()
