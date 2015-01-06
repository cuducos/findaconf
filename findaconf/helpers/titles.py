# coding: utf-8


def get_search_title(count, query):
    """
    Returns the title for a search
    :param count: (int) number of results found in the search
    :param query: (string) word/expression searched for
    :return: (string) The title for the page with the search results
    """
    if count == 0:
        prefix = 'Sorry, no conferences'
    elif count == 1:
        prefix = '1 conference'
    else:
        prefix = '{} conferences'.format(count)
    return '{} found for “{}”'.format(prefix, query)
