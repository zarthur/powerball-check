import csv
import os
import sys

from collections import namedtuple
from typing import List, Sequence, Tuple


MatchResult = namedtuple("MatchResult", ["pb_numbers", "white", "red"])


class PowerBallNumbers:
    def __init__(self, numbers: Sequence[int]):
        self.red_ball = numbers[-1]
        self.white_balls = set(numbers[:-1])

    @property
    def numbers(self):
        all_balls = sorted(self.white_balls)
        all_balls.append(self.red_ball)
        return all_balls

    def __str__(self):
        return "PowerBallNumber({0})".format([str(x) for x in self.numbers])

    def check_match(self, drawing: Sequence[int]) -> Tuple[int, int]:
        drawing_red = drawing[-1]
        drawing_white = set(drawing[:-1])

        red_match = 1 if self.red_ball == drawing_red else 0
        white_match = len(self.white_balls & drawing_white)
        return white_match, red_match


class NumberLoader:
    def __init__(self, filename: str):
        self.numbers = []
        with open(filename) as infile:
            reader = csv.reader(infile)
            for row in reader:
                row = [int(x) for x in row]
                self.numbers.append(PowerBallNumbers(row))

    def get_results(self, drawing: Sequence[int]) -> List[MatchResult]:
        results = []

        for number in self.numbers:
            white_result, red_result = number.check_match(drawing)
            if white_result >= 3 or red_result > 0:
                results.append(MatchResult(number, white_result, red_result))

        return results


def main(filename, drawing):
    if not os.path.exists(filename):
        print("{0} does not exist.".format(filename))
        return

    numbers = NumberLoader(filename)
    matches = sorted(numbers.get_results(drawing),
                     key=lambda x: x.white+x.red,
                     reverse=True)

    for match in matches:
        numbers = ", ".join(str(x) for x in match.pb_numbers.numbers)
        print("W: {0}, R: {1} | {2}"
              .format(str(match.white), str(match.red), numbers))


if __name__ == "__main__":
    if len(sys.argv) == 8:
        _, data_file, *draw_numbers = sys.argv
        main(data_file, [int(x) for x in draw_numbers])
