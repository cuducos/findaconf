# coding: utf-8


def get_search_title(count, query, include_query=False):
    if count == 0:
        prefix = 'Sorry, no conferences'
    elif count == 1:
        prefix = '1 conference'
    else:
        prefix = '{} conferences'.format(count)
    return '{} found for “{}”'.format(prefix, query)
