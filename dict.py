# Find any undefined words and remove them.
# Remove the word with the largest fanout.
# Iterate

from typing import Set
from graph import Graph, highest_fanout, lowest_fanin


input: Graph[str] = Graph()
input.to('the', 'bible')

result: Set[str] = set()

while len(input) > 0:
    lowest_gen = lowest_fanin(input)

    lowest = next(lowest_gen)
    while input.get(lowest).fanin() == 0:
        print(f'add {lowest}')
        result.add(lowest)
        input.pop(lowest)
        lowest = next(lowest_gen)

    highest_gen = highest_fanout(input)

    highest = next(highest_gen)
    print(f'add2 {highest}')
    input.pop(highest)
    result.add(highest)

print(result)