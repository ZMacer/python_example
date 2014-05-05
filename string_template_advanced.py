#string_template_advanced.py
#! /usr/bin/python
# -*- coding:utf8 -*-

import string

template_text = ''' 
    Replaced  : %with_underscore
    Delimiter : %%
    Ignored   : %notunderscored
 '''
d = { 'with_underscore':'replaced',
      'notunderscored':'not replaced',
      }
class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = '[a-z]+_[a-z]+'

t = MyTemplate(template_text)
print 'Modified ID pattern:'
print t.safe_substitute(d)

t = string.Template('$var')
print t.pattern.pattern
##================================================================
import re
class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{) |
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''
t = MyTemplate('''
{{{{
{{var}}
''')
print 'matches:', t.pattern.findall(t.template)
print 'substituted:',t.safe_substitute(var='replacement')
##===============================================================
