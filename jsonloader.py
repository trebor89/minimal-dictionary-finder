import json
import re
from typing import Any, Dict, List, Tuple

import requests

from graph import Graph

# Ordered list for priority's sake.
clean_conversions: List[Tuple[str, str]] = [
    (r'-bearing', ''),
    (r'-shaped$', ''),
    (r'like$', ''),
    (r'ness$', ''),
    (r'^non-', ''),
    (r'^un', ''),
    (r's$', ''),
    (r'ly$', ''),
    (r'ed$', ''),
    (r'al$', ''),
    (r'ing$', 'e'),
    (r'ing$', ''),
]

def clean_def_word(g: Graph[str], def_word: str) -> str:
    if def_word in g:
        return def_word

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

def load() -> Graph[str]:
    res = Graph()

    js: Dict[str, str] = requests.get(url=r"https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json").json()
    
    for word in js:
        res.get(word.lower())

    for (word, df) in js.items():
        word = word.lower()
        for def_word in re.findall(r"[a-zA-Z]+[-a-zA-Z]*", df):
            def_word = def_word.lower()

            def_word = clean_def_word(res, def_word)

            # if word == 'amygdaliferous':
            #     print(df)

            if def_word in res.all:
                res.to(def_word.lower(), word.lower())
    return res