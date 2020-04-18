from graph import Graph
from typing import Dict
import json
import re
import requests

def load() -> Graph[str]:
    res = Graph()

    js: Dict[str, str] = requests.get(url=r"https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json")
    
    for (word, df) in js.items():
        for def_word in re.split(r"['\"-().;, ]", df):
            if def_word in js:
                res.to(def_word.lower(), word.lower())
        res.get(word)
    return res