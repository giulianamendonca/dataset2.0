import csv
from dataclasses import dataclass
import random


@dataclass
class Parameters:
    rows: int
    columns: int
    min_digits: int
    max_digits: int
    distribution: str
    mode: float
    currency_flag: bool


def main():
    parameters = get_parameters()

    # generates the name of the file and as a seed for dataset generation
    label = get_label()

    create_file(label, parameters)


def get_parameters() -> Parameters:
    """
    Prompt the user for the parameters needed by the generator.

    Returns:
        Parameters object. Contains:
            - rows: number of rows in the dataset
            - columns: number of columns in the dataset
            - min_digits: minimum number of digits per number (see `get_range`)
            - max_digits: maximum number of digits per number (see `get_range`)
            - distribution: T for triangular, U for uniform
            - mode: percentage of the [min, max] range for the triangular distribution, 0 if uniform
            - currency_flag: True if numbers are to be represented as currency, False if not. If True, min_digits/max_digits are automatically increased by 2.
    """
    # shape of the dataset
    rows = get_number("Number of rows")
    columns = get_number("Number of columns")

    while True:
        min_digits = get_number("Min digits per number")
        max_digits = get_number("Max digits per number")

        if min_digits > max_digits:
            print("min must be less than or equal to max")
        else:
            break

    # additional information
    distribution, mode = get_distribution()

    currency = ""
    while currency not in ["Y", "N"]:
        currency = input("Currency? Y/N ").upper()

    currency_flag = currency == "Y"

    # adjusts min and max digits if currency is set to True
    if currency_flag:
        min_digits += 2
        max_digits += 2

    return Parameters(rows, columns, min_digits, max_digits, distribution, mode, currency_flag)


def get_number(text: str) -> int:
    """
    Prompt the user for an integer greater than zero.

    Args:
        text (str): message to display when prompting user

    Returns:
        n (int): integer entered by the user. Re-prompts if input is invalid or non-positive.
    """
    while True:
        try:
            n = int(input(f"{text}: "))
            if n > 0:
                return n
            else:
                print("Number must be positive")
        except ValueError:
            continue


def get_distribution() -> tuple[str, float]:
    """
    Prompt the user to select the desired distribution and, if triangular, its mode.

    Returns:
        tuple: (str, float)
            - distribution: T for triangular, U for uniform
            - mode: percentage of the [min, max] range for the triangular distribution, 0 if uniform. Stored as a 0-1 interval.
    """
    while True:
        distribution = input("Distribution [T for triangular / U for uniform]: ").upper()

        if distribution not in ["T", "U"]:
            print("Invalid distribution. Please enter T or U")
            continue

        if distribution == "T":
            try:
                mode_percent = int(input("Mode (percentage of the range): "))
            except ValueError:
                print("Mode must be an integer")
                continue

            if 1 <= mode_percent <= 100:
                mode = mode_percent / 100
                break
            else:
                print("Mode must be a number between 1 and 100")
                continue
        # sets mode as 0 and exits loop
        else:
            mode = 0
            break

    return distribution, mode


def get_label() -> int:
    """
    Generates a random integer. It is not seeded, but the return value will serve as seed for further RNG.

    Returns:
        label (int): random integer that will be used filename suffix and RNG seed in dataset generation
    """
    label = random.randint(0, 99999)

    return label


def create_file(label: int, parameters: Parameters) -> None:
    """
    Generates a .csv file with randomized numbers according to the given parameters.

    Args:
        - label (int): seed to initialize the RNG, also used as name for the generated file. Passed as arg for the get_digits function.
        - parameters (Parameters): configuration for dataset generation. Passed as arg for the get_digits function.

    Returns:
        None. Writes a .csv file to disk with the generated dataset.
    """
    filename = "dataset_" + str(label) + ".csv"

    random.seed(label)

    with open(filename, 'w', newline='') as file:
        number_writer = csv.writer(file, delimiter=',')

        digits_per_row = get_digits(label, parameters)

        for digits in digits_per_row:
            lowest_number, highest_number = get_range(digits)
            mode_real = lowest_number + parameters.mode * (highest_number - lowest_number)

            numbers = [
                random.randint(lowest_number, highest_number)
                if parameters.distribution == "U"
                else int(round(random.triangular(lowest_number, highest_number, mode_real)))
                for _ in range(parameters.columns)
            ]

            # undoes the alteration in the number of digits when currency is True
            if parameters.currency_flag:
                numbers = [number / 100 for number in numbers]

            # writes numbers in the file
            number_writer.writerow(numbers)


def get_digits(label: int, parameters: Parameters) -> list[int]:
    """
    Obtain the number of digits for each row.

    Args:
        - label (int): seed to initialize the RNG
        - parameters (Parameters): configuration for dataset generation

    Returns:
        - digits (list - int): list containing the number of digits for each row in the dataset, randomly chosen within [min_digits, max_digits]
    """
    random.seed(label)

    digits = [
        random.randint(parameters.min_digits, parameters.max_digits)
        for _ in range(parameters.rows)
    ]

    return digits


def get_range(digits_number: int) -> tuple[int, int]:
    """
    Sets the upper and lower limits for a row.

    Args:
        - digits_number: number of digits for a given row in the dataset, as determined by the get_digits function

    Returns:
        - lowest (int): lower limit for a given row
        - highest (int): upper limit for a give row,
    """
    lowest = 10 ** (digits_number - 1)
    highest = 10 ** digits_number - 1

    return lowest, highest


if __name__ == "__main__":
    main()
