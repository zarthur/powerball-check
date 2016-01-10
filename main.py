import csv
import os
import sys
from typing import Sequence, Tuple


class PowerBallNumbers:
    def __init__(self, numbers: Sequence[int]):
        self._red_ball = numbers[-1]
        self._white_balls = set(numbers[:-1])

    @property
    def numbers(self):
        white = ", ".join([str(x) for x in sorted(self._white_balls)])
        red = str(self._red_ball)
        return "{0}, {1}".format(white, red)

    def __str__(self):
        return "PowerBallNumber({0})".format(self.numbers)

    def check_match(self, drawing: Sequence[int]) -> Tuple[int, int]:
        drawing_red = drawing[-1]
        drawing_white = set(drawing[:-1])

        red_match = 1 if self._red_ball == drawing_red else 0
        white_match = len(self._white_balls & drawing_white)
        return white_match, red_match


class NumberLoader:
    def __init__(self, filename: str):
        self.numbers = []
        with open(filename) as infile:
            reader = csv.reader(infile)
            for row in reader:
                row = [int(x) for x in row]
                self.numbers.append(PowerBallNumbers(row))

    def get_results(self, drawing: Sequence[int]) -> Tuple:
        results = []
        for number in self.numbers:
            white_result, red_result = number.check_match(drawing)
            if white_result >= 3 or red_result > 0:
                results.append((number, (white_result, red_result)))
        return results


def main(filename, drawing):
    if not os.path.exists(filename):
        print("{0} does not exist.".format(filename))
        return

    numbers = NumberLoader(filename)
    matches = numbers.get_results(drawing)
    for pb_numbers, (white_count, red_count) in matches:
        message = ("W: {0}, R: {1} | {2}"
                   .format(white_count, red_count, pb_numbers.numbers))
        print(message)


if __name__ == "__main__":
    if len(sys.argv) == 8:
        main(sys.argv[1], [int(x) for x in sys.argv[2:]])
