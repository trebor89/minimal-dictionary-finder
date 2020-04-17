# Find any undefined words and mark them
# Perform the marking closure.
# Loop until done.
# Find the highest fanout word and mark it.
# Perform the marking closure.
# Iterate until all words are marked

from typing import Generator, Set, Union

from graph import Graph, Node

input: Graph[str] = Graph()
input.to('the', 'bible')
input.to('book', 'bible')

result: Set[str] = set()

def mark_all_zero_fanin(g: Graph[str]) -> None:
    # Mark all fanin0 and add to result.
    for n in g:
        if not n.marked and n.fanin() == 0:
            result.add(n.get())
            n.mark()
    
    # While we encounter unamrked parents, mark them.
    while g:
        encountered = False
        for n in g:
            if not n.marked and n.unmarked_fanin() == 0:
                n.mark()
                encountered = True
        if not encountered:
            break

def highest_unmarked_fanout(g: Graph[str]) -> Union[Node[str], None]:
    gen: Generator[Node[str]] = (n for n in g if not n.marked)
    return max(gen, default = None, key = lambda n: n.fanout())

# mark all zero fanin recursively.
# Graph the largest fanout and add it, marking it.
# Remove elements from loops.
# Do until graph empty.

mark_all_zero_fanin(input)

while list((n for n in input if not n.marked)):
    mx = highest_unmarked_fanout(input)
    result.add(mx.get())
    mx.mark()

print(result)