from typing import (Any, Callable, Dict, Generator, Generic, Iterator, List,
                    Optional, TypeVar, Union)

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, t: T, marked: bool = False):
        self.marked: bool = marked
        self.t: T = t
        self.frm: Dict[T, Node[T]] = {}
        self.to: Dict[Node[T]] = {}
    
    def __str__(self) -> str:
        return f"{{marked: {self.marked}, t: {self.t}, from: {self.frm}, to: {self.to}}}"

    def get(self) -> T:
        return self.t
    
    def mark(self):
        self.marked = True
    
    def _pop(self, t: T) -> None:
        self.to.pop(t)
        pass

    def _pop_parents(self) -> None:
        frm: Node[T]
        for frm in self.frm.values():
            frm._pop(self.t)
    
    def unmarked_fanin(self) -> int:
        marked = (i for i in self.frm.values() if not i.marked)
        return len(list(marked))
    
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
    
    def __str__(self) -> str:
        return str(self.nodes)

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
