from graph import Graph, Node
from jsonloader import load


input: Graph[str] = load()

with open("output.txt", "w") as out:
    out.writelines(sorted(f"{n.t}\n" for n in input if n.necessary))