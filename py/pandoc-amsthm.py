#!/usr/bin/env python

"""
A pandoc filter to define amsthm environement through YAML, the use of Div,
with templates and this filter.
See detail in https://github.com/ickc/pandoc-amsthm
"""

from pandocfilters import toJSONFilters, RawBlock, stringify

import re

def environment(key, value, format, meta):
    # Is it a div?
    if key == 'Div':

        # Get the attributes
        [[id, classes, properties], content] = value

        currentClasses = set(classes)

        for environment, definedClasses in getDefined(meta).items():
            # Is the classes correct?
            if currentClasses <= definedClasses:
                value[1] = [RawBlock('tex', '\\begin{' + ', '.join(set.intersection(currentClasses, definedClasses)) + '}')] + content + [RawBlock('tex', '\\end{' + ', '.join(set.intersection(currentClasses, definedClasses)) + '}')]
                break

def getDefined(meta):
    # Return the amsthm environment defined in the meta
    if not hasattr(getDefined, 'value'):
        getDefined.value = {}
        if 'amsthm' in meta and meta['amsthm']['t'] == 'MetaMap':
            for environment, classes in meta['amsthm']['c'].items():
                if classes['t'] == 'MetaList':
                    getDefined.value[environment] = []
                    for klass in classes['c']:
                        string = stringify(klass)
                        if re.match('^[a-zA-Z][\w.:-]*$', string):
                            getDefined.value[environment].append(string)
                    getDefined.value[environment] = set(getDefined.value[environment])
    return getDefined.value

def main():
    toJSONFilters([environment])

if __name__ == '__main__':
    main()