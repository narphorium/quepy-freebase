#!/usr/bin/env python
# coding: utf-8

# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Shawn Simister <simister@google.com>

"""
Semantics for Freebase quepy.
"""

from quepy.semantics import FixedType, HasKeyword, FixedRelation, \
                            FixedDataRelation

# Setup the Keywords for this application
HasKeyword.relation = "freebase:type.object.name"
HasKeyword.language = "en"

FixedType.fixedtyperelation = "freebase:type.object.type"

class DefinitionOf(FixedRelation):
    relation = "freebase:common.topic.article"
    reverse = True


class HasName(FixedDataRelation):
    relation = "freebase:type.object.name"
    language = "en"


class LabelOf(FixedRelation):
    relation = "freebase:type.object.name"
    reverse = True


class NameOf(FixedRelation):
    relation = "freebase:type.object.name"
    reverse = True

