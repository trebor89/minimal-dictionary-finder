from graph import Graph, Node
from jsonloader import load


print("Loading...")
input: Graph[str] = load()

print("Writing...")
with open("output.txt", "w") as out:
    out.writelines(sorted(f"{n.t}\n" for n in input if n.necessary))