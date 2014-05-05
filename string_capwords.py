#string_capwords.py
#! /usr/bin/python
# -*- coding:utf8 -*-

import string
s = 'The quick brown fox junped over the lazy dog.'
print s
print string.capwords(s)
leet = string.maketrans('abegiloprstz','463611092572')
print s
print s.translate(leet)
values = { 'var':'foo'}

t = string.Template("""
Variable        : $var
Escape          : $$
Variable in text: ${var}iable
""")
print 'Template:',t.substitute(values)

s = """
Variable        : %(var)s
Escape          : %%
Variable in text: %(var)siable
"""
print 'interpolation:',s % values
