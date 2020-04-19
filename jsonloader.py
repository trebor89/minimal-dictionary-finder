import json
import re
from typing import Any, Dict, List, Tuple

import requests

from graph import Graph

# Ordered list for priority's sake.
clean_conversions: List[Tuple[str, str]] = [
    (r'like$', ''),
    (r'ness$', ''),
    (r'^un', ''),
    (r's$', ''),
    (r'ly$', ''),
    (r'ed$', 'e'),
    (r'ed$', ''),
    (r'al$', ''),
    (r'tting$', 't'),
    (r'ing$', 'e'),
    (r'ing$', ''),
    (r'e$', ''),
    (r'ive$', '')
]

hyphenations: List[str] = [
    r'^even-',
    r'-bearing$',
    r'-shaped$',
    r'^non-'
]

def clean_non_hyphenated(g: Graph[str], def_word: str) -> str:
    matched: bool = True
    while matched:
        matched = False
        for (frm, to) in clean_conversions:
            new_word = re.sub(frm, to, def_word)
            if new_word != def_word:
                def_word = new_word
                matched = True
            if def_word in g:
                return def_word

    return def_word

def clean_def_word(g: Graph[str], def_word: str) -> List[str]:
    if def_word in g:
        return [def_word]
    
    for hyph in hyphenations:
        def_word = re.sub(hyph, '', def_word)

    # Split on hyphens, removing words that are already in.
    dehyphenated = def_word.split("-")

    return [clean_non_hyphenated(g, s) for s in dehyphenated]

def load() -> Graph[str]:
    res = Graph()

    js: Dict[str, str] = requests.get(url=r"https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json").json()
    
    for word in js:
        res.get(word.lower())

    for (word, df) in js.items():
        word = word.lower()
        for def_word in re.findall(r"[a-zA-Z]+[-a-zA-Z]*", df):
            def_word: str = def_word.lower()

            clean_def_words = clean_def_word(res, def_word)

            for clean in clean_def_words:
                if clean in res.all:
                    res.to(clean, word)
    return res