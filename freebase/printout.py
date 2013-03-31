#!/usr/bin/env python
# coding: utf-8

# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Shawn Simister <simister@google.com>

"""
Freebase output utilities.
"""

import json
from quepy.expression import isnode

def adapt_mql(x):
    if isinstance(x, basestring) and x.index('@') > 0:
        value, lang = x.split('@')
        return {'value':unicode(value[1:-1]),'lang':'/lang/'+lang}
    x = unicode(x)
    if x.index(':') > 0:
        x = format_mql_uri(unicode(x))
    return unicode(x)

def format_mql_uri(uri):
    if uri.startswith('freebase:'):
        uri = uri[9:]
        uri = '/' + uri.replace('.','/')
    elif uri == 'rdf:type':
        uri = "type"
    return uri

def expression_to_mql(e):
    mql_query = []
    visited_nodes = set()
    mql_query.append(node_to_mql(e, 0, visited_nodes))
    return json.dumps(mql_query, indent=2)
    
def node_to_mql(e, node, visited_nodes):
    mql_query = {}
    num_relations = 0
    visited_nodes.add(node)
    for relation, dest in e.iter_edges(node):
        if not dest in visited_nodes:
            relation = format_mql_uri(relation)
            if isnode(dest):
                dest_mql = node_to_mql(e, dest, visited_nodes)
                if type(dest_mql) == dict:
                    dest_mql = [dest_mql]
                mql_query[relation] = dest_mql
            else:
                mql_query[relation] = adapt_mql(dest)
            num_relations += 1
    for relation, dest in iter_incoming_edges(e, node, visited_nodes):
        if not dest in visited_nodes:
            relation = '!' + format_mql_uri(relation)
            if isnode(dest):
                dest_mql = node_to_mql(e, dest, visited_nodes)
                if type(dest_mql) == dict:
                    dest_mql = [dest_mql]
                mql_query[relation] = dest_mql
            else:
                mql_query[relation] = adapt_mql(dest)
            num_relations += 1
    if num_relations == 0:
        return None
    return mql_query

def iter_incoming_edges(e, target, visited_nodes):
    for node in e.iter_nodes():
        if not node in visited_nodes:
            for relation, dest in e.iter_edges(node):
                if dest == target:
                    yield relation, node
