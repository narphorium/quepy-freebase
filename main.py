#!/usr/bin/env python
# coding: utf-8

# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Shawn Simister <simister@google.com>

"""
Main script for Freebase quepy.
"""

import sys
import time
import random
import datetime
import json

import os
sys.path.insert(0, '/Users/simister/quepy')

import quepy

freebase = quepy.install("freebase")

#quepy.set_loglevel("DEBUG")

if __name__ == "__main__":
    default_questions = [
        "List movies directed by Martin Scorsese",
        "which movies did Mel Gibson star in?",
        "When was Gladiator released?",
        "who directed Pocahontas?",
        "actors of Fight Club",
    ]

    if "-d" in sys.argv:
        quepy.set_loglevel("DEBUG")
        sys.argv.remove("-d")

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        questions = [question]
    else:
        questions = default_questions

    for question in questions:
        print question
        print "-" * len(question)

        target, query, metadata = freebase.get_query(question, query_lang='mql')

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print "Query not generated :(\n"
            continue

        print query

