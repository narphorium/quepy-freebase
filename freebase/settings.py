#!/usr/bin/env python
# coding: utf-8

# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Shawn Simister <simister@google.com>

"""
Freebase Settings.
"""

# Freeling config
USE_FREELING = False
FREELING_CMD = ""  # Only set if USE_FREELING it's True

# NLTK config
NLTK_DATA_PATH = []  # List of paths with NLTK data

# Encoding config
DEFAULT_ENCODING = "utf-8"
# Sparql config
SPARQL_PREAMBLE = u"""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX freebase: <http://rdf.freebase.com/ns/>
"""
