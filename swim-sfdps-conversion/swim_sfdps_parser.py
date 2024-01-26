#!/usr/bin/env python3

import pandas as pd
import xml.etree.ElementTree as ET
import re

### Defining some Utilities
letter_only_regex = re.compile("[a-zA-Z]*")
def getIndexedName(colName: str, row_dict: list):
  nameList = list(row_dict.keys())
  index_regex = colName + '\[\d\]$'
  index_regex = re.compile(index_regex)
  if colName in nameList:
    indexes = list(filter(index_regex.match, nameList))
    return f"{colName}[{len(indexes) + 1}]"
  return colName

### Defining the parsing alg
def parseNode(node, pathToNode: str, row_dict: dict):
  path = "_".join([pathToNode, node.tag]) if len(pathToNode) else node.tag
  path = getIndexedName(path, row_dict)
  if node.attrib:
    for attr, val in node.attrib.items():
        # Attributes sometimes contain links, which we don't want
        if re.search(letter_only_regex, attr).group() == attr:
          colName = ".".join([path, attr])
          # ADD COLUMNS AND VALUES TO DICT
          row_dict[colName] = val
  if len(node):
    for child in node:
      parseNode(child, path, row_dict)
  else:
    text = node.text if node.text else "NaN"
    colName = path
    colName = getIndexedName(colName, row_dict)
    row_dict[colName] = text

### Setting file_name and parsing
file_name = 'sample-data-1-8-24.xml'
rows = []
root = ET.parse(file_name).getroot()
for i, message in enumerate(root.findall('message')):
  row_dict = {}
  parseNode(message, "", row_dict)
  rows.append(row_dict)

df = pd.DataFrame(rows)
csv_name = f"{file_name[:-4]}.csv"
df.to_csv(csv_name)