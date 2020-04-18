from typing import (Any, Callable, Dict, Generator, Generic, Iterator, List,
                    Optional, Set, TypeVar, Union)

T = TypeVar('T')

class Node(Generic[T]):
    def __init__(self, g: 'Graph[T]', t: T) -> None:
        self.g: 'Graph[T]' = g
        self.t: T = t
        self.marked: bool = False
        self.to: Set[Node[T]] = set()
    
    def get(self) -> T:
        return self.t

def unmarked(n: Node[T]) -> bool:
    return not n.marked

class Graph(Generic[T]):
    def __init__(self):
        self.all: Dict[T, Node[T]] = {}
        self.unmarked: Set[Node[T]] = set()

    def mark(self, n: Node[T]) -> None:
        self.unmarked.remove(n)
        n.marked = True
    
    def get(self, t: T) -> Node[T]:
        if t not in self.all:
            self.all[t] = Node(self, t)
            self.unmarked.add(self.all[t])
        
        return self.all[t]

    def to(self, frm: T, to: T) -> None:
        self.get(frm).to.add(self.get(to))