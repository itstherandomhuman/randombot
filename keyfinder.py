#!/usr/bin/env python

## the global variable for all values as list
global listOfValues
listOfValues = []

def keyfind(layer, keyword:str):
    global listOfValues
    if isinstance(layer, dict):
        for k,v in layer.items():
            if k == keyword:
                listOfValues += [layer[k]]
            keyfind(layer[k], keyword=keyword)
    elif isinstance(layer, list):
        for i in layer:
            keyfind(i, keyword=keyword)

    return listOfValues
