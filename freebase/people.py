#!/usr/bin/env python
# coding: utf-8

# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Shawn Simister <simister@google.com>

"""
Freebase people domain semantics.
"""

from refo import Plus, Question
from quepy.semantics import HasKeyword
from quepy.semantics import FixedType, HasKeyword, FixedRelation, \
                            FixedDataRelation
from quepy.regex import Lemma, Lemmas, Pos, RegexTemplate, Particle
from semantics import NameOf, LabelOf, HasName, DefinitionOf

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

# People types

class IsPerson(FixedType):
    fixedtype = "freebase:people.person"


# People relations

class BirthPlaceOf(FixedRelation):
    relation = "freebase:people.person.place_of_birth"
    reverse = True


class BirthDateOf(FixedRelation):
    relation = "freebase:people.person.date_of_birth"
    reverse = True


# People regular expressions