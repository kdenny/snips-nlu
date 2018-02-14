# coding=utf-8
from __future__ import unicode_literals

from future.builtins import object

import csv
import io


def utf_8_encoder(f):
    for line in f:
        yield line.encode("utf-8")


class CustomEntity(object):
    """Entity of a :class:AssistantDataset

        Attributes:
            :class:CustomEntity.utterances: language of the dataset
            :class:CustomEntity.automatically_extensible: should the NLU output
             be filtered on
            :class:CustomEntity.use_synonyms: should the synonyms be used in
            the NLU
            :class:CustomEntity.json: the entity in json format
    """

    def __init__(self, utterances, automatically_extensible=True,
                 use_synonyms=True):
        self.utterances = utterances
        self.automatically_extensible = automatically_extensible
        self.use_synonyms = use_synonyms

    @classmethod
    def from_file(cls, entity_file_name):
        utterances = []
        with io.open(entity_file_name, "r", encoding="utf8") as f:
            reader = csv.reader(list(utf_8_encoder(f)))
            for row in reader:
                row = [cell.encode("utf-8") for cell in row]
                value = row[0]
                if len(row) > 1:
                    synonyms = row[1:]
                else:
                    synonyms = []
                utterances.append(EntityUtterance(value, synonyms))
        return cls(utterances, automatically_extensible=True,
                   use_synonyms=True)


    @property
    def json(self):
        entity_dict = dict()
        entity_dict["automatically_extensible"] = self.automatically_extensible
        entity_dict["use_synonyms"] = self.use_synonyms
        entity_dict["data"] = [u.json for u in self.utterances]
        return entity_dict


class EntityUtterance(object):
    def __init__(self, value, synonyms=None):
        self.value = value
        if synonyms is None:
            synonyms = []
        self.synonyms = synonyms

    @property
    def json(self):
        return {"value": self.value, "synonyms": self.synonyms}