from graph import Graph
from typing import Dict
import json
import re
import requests

def load() -> Graph[str]:
    res = Graph()

    js: Dict[str, str] = requests.get(url=r"https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json").json()
    
    for word in js:
        res.get(word.lower())

    for (word, df) in js.items():
        for def_word in re.findall(r"[a-zA-Z]+[-a-zA-Z]*", df):
            if def_word in res.all:
                res.to(def_word.lower(), word.lower())
    return res