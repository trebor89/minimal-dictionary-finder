# Find any undefined words and mark them
# Perform the marking closure.
# Loop until done.
# Find the highest fanout word and mark it.
# Perform the marking closure.
# Iterate until all words are marked

import re
from typing import Any, Generator, Set, Union

import jsonloader
from graph import Graph, Node, unmarked

input: Graph[str] = jsonloader.load()

result: Set[str] = set()

def unmarked_fanout(n: Node[str]) -> int:
    return len(list(filter(unmarked, n.to)))

while input.unmarked:
    print(f"Size: {len(input.unmarked)}")
    # Find the one with the highest fanout.
    n: Node[str] = max(input.unmarked, key = unmarked_fanout)

    result.add(n.t)

    # Take the marking closure.
    to_mark: Set[Node[str]] = {n}
    while to_mark:
        n: Node[str] = to_mark.pop()

        input.mark(n)

        to_mark.update(filter(unmarked, n.to))

with open("output.txt", "w") as out:
    for word in result:
        out.write(f"{word}\n")
