from typing import (Any, Callable, Dict, Generator, Generic, Iterator, List,
                    Optional, Set, TypeVar, Union)

T = TypeVar('T')

class Node(Generic[T]):
    def __init__(self, g: 'Graph[T]', t: T) -> None:
        self.g: 'Graph[T]' = g
        self.t: T = t
        self.necessary: bool = True
        self.to: Set[Node[T]] = set()
    
    def __str__(self) -> str:
        return f"{self.t}: {[n.t for n in self.to]}"
    
    def get(self) -> T:
        return self.t

class Graph(Generic[T]):
    def __init__(self):
        self.all: Dict[T, Node[T]] = {}
    
    def __iter__(self) -> Iterator[Node[T]]:
        return iter(self.all.values())

    def __contains__(self, item: T):
        return item in self.all
    
    def get(self, t: T) -> Node[T]:
        if t not in self.all:
            self.all[t] = Node(self, t)
        
        return self.all[t]

    def to(self, frm: T, to: T) -> None:
        n_to = self.get(to)
        self.get(frm).to.add(n_to)
        n_to.necessary = False