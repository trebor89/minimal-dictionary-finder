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

# Mark all with zero fan-in.
# Keep map from unmarked fanout to set of nodes.
# After each mark, we have to update the marks, moving anydown the list.
# Find the one with the highest fanout, marking it.
# Follow the links backwards, reducing their fanin.