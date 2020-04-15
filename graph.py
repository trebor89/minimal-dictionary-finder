from typing import (Any, Callable, Dict, Generator, Generic, Iterator, List,
                    Optional, TypeVar, Union)

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, t: T):
        self.t: T = t
        self.frm: Dict[T, Node[T]] = {}
        self.to: Dict[Node[T]] = {}

    def get(self) -> T:
        return self.t
    
    def _pop(self, t: T) -> None:
        self.to.pop(t)
        pass

    def _pop_parents(self) -> None:
        frm: Node[T]
        for frm in self.frm.values():
            frm._pop(self.t)
    
    def fanin(self) -> int:
        return len(self.frm)

    def fanout(self) -> int:
        return len(self.to)

    def _to(self, next: 'Node[T]'):
        self.to[next.get()] = next
        next.frm[self.t] = self


class Graph(Generic[T]):
    def __init__(self):
        self.nodes: Dict[T, Node[T]] = {}

    def __iter__(self) -> Iterator[Node[T]]:
        return iter(self.nodes.values())

    def __len__(self) -> int:
        return len(self.nodes)

    def __bool__(self) -> bool:
        return bool(self.nodes)

    def pop(self, t: T) -> Node[T]:
        n: Node[T] = self.nodes.pop(t)

        n._pop_parents()

        return n

    def get(self, t: T) -> Node[T]:
        if t not in self.nodes:
            self.nodes[t] = Node(t)

        return self.nodes[t]

    def to(self, frm: T, to: T):
        self.get(to)
        self.get(frm)._to(self.get(to))


def lowest_fanin(g: Graph[T]) -> Generator[T, None, None]:
    while g:
        yield min(g, key=Node.fanin).get()

def highest_fanout(g: Graph[T]) -> Generator[T, None, None]:
    while g:
        yield max(iter(g), key=Node.fanout).get()
