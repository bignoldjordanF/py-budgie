from typing import Dict, Union
from dataclasses import dataclass
from collections import defaultdict
import csv


@dataclass
class PBFileContents:
    metadata: Dict[str, Union[str, int, float]]
    """Any metadata about the participatory budgeting instance."""

    projects: defaultdict[int, defaultdict[str, Union[str, int, float]]]
    """The project data represented as a projectId->data mapping."""

    voters: defaultdict[int, defaultdict[str, Union[str, int]]]
    """The voter data represented as a voterId->data mapping."""


# Reference:
# [1] http://pabulib.org/format
# [2] http://pabulib.org/code

def read_pb_file(filepath: str) -> PBFileContents:
    """
    Reads the contents of a .pb file [1] into a PBFileContents
    dataclass object. See reference [2] for source.

    Parameters:
        - filepath (str): The path to the .pb file.
    """
    metadata: Dict[str, Union[str, int, float]] = defaultdict(str)
    projects: Dict[int, Dict[str, Union[str, int, float]]] = defaultdict(defaultdict)
    votes: Dict[int, Dict[str, Union[str, int]]] = defaultdict(defaultdict)

    if not filepath.endswith('.pb'):
        filepath += '.pb'

    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        section, header, reader = '', [], csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ('meta', 'projects', 'votes'):
                section = str(row[0]).strip().lower()
                header = next(reader)

            elif section == 'meta':
                metadata[row[0]] = row[1].strip()

            elif section == 'projects':
                projects[row[0]] = defaultdict(str)
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it+1].strip()
            
            elif section == 'votes':
                votes[row[0]] = defaultdict(str)
                for it, key in enumerate(header[1:]):
                    votes[row[0]][key.strip()] = row[it+1].strip()

    return PBFileContents(metadata, projects, votes)
