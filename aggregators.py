# coding: utf-8

import helpers
from itertools import groupby

def monthly(data, aggregate_func):
    return timed_group(data, lambda x: (x['key'].month, x['key'].year),
                       aggregate_func, min)

def weekly(data, aggregate_func):
    return timed_group(data, lambda x: (x['key'].isocalendar()[1],
                       x['key'].year), aggregate_func, min)

def timed_group(data, group_func, aggregate_func, group_label_func):
    groups = []
    for k, g in groupby(data, group_func):
        groups.append((k, list(g)))

    data = list()
    for g in groups:
        value = aggregate_func([r['data'] for r in g[1]])
        label = group_label_func([r['key'] for r in g[1]])
        data.append(helpers.make_record(label, value))
    return data    
