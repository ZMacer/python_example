# -*- coding: utf-8 -*-
#textwrap_fill.py
#! /usr/bin/python

sample_text = '''
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired. It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text eitors.
    '''
import textwrap

print 'No dedent:\n'
print textwrap.fill(sample_text,width=50)
print
##===============================================================
dedented_text = textwrap.dedent(sample_text)
print 'Dedented:'
print dedented_text
##===============================================================
dedented_text = textwrap.dedent(sample_text).strip()
print 'dedented_text:\n'
print dedented_text
print
for width in [45,70]:
    print '%d Columns:\n' % width
    print textwrap.fill(dedented_text,width= width)
    print
##===============================================================
dedented_text = textwrap.dedent(sample_text).strip()
print textwrap.fill(dedented_text,
                    initial_indent='',
                    subsequent_indent=' '*4,
                    width=50,
                    )
print
print textwrap.fill(dedented_text,
                    initial_indent=' '*4,#first line 四个空格开头，
                    subsequent_indent='',#其余行顶行
                    width=50,
                    )
##===============================================================
