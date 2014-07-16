# -*- coding: utf-8 -*-
#re_simple_match.py
#! /usr/bin/python
import re

pattern = 'this'
text = 'Does this text match the pattern?'
match = re.search(pattern,text)
s = match.start()
e = match.end()

print 'Found "%s"\nin "%s"\nfrom %d to %d ("%s")' % \
      (match.re.pattern,match.string,s,e,text[s:e])
##===============================================================
regexes = [ re.compile(p) for p in ['this','that']]
print 'Text: %r\n' % text

for regex in regexes:
    print 'Seeking "%s" ->' % regex.pattern,
    if regex.search(text):
        print 'match!'
    else:
        print 'no match'
##===============================================================

text = 'abbaaabbbbaaaaa'
pattern = 'ab'
for match in re.findall(pattern,text):
    print 'Fond "%s"' % match
print

for match in re.finditer(pattern,text):
    s = match.start()
    e = match.end()
    print 'Found "%s" at %d:%d' %(text[s:e],s,e)

##===============================================================
def test_patterns(text,patterns=[]):
    for pattern,desc in patterns:
        print 'Pattern %r (%s)\n' % (pattern,desc)
        print '  %r' % text
        for match in re.finditer(pattern,text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\') #这句查找'\'的个数让我感觉莫名其妙妙，本例中为0
            prefix = '.'*(s+n_backslashes)
            print '  %s%r' % (prefix,substr)
        print
    return
if __name__ =='__main__':
    test_patterns('abbaaabbbbaaaaa',[('ab',"'a'followed by 'b'"),])
    #匹配重头多次匹配
    test_patterns(
'abbaabbba',
[ ('ab*', 'a followed by zero or more b'),
('ab+', 'a followed by one or more b'),
('ab?', 'a followed by zero or one b'),
('ab{3}', 'a followed by three b'),
('ab{2,3}', 'a followed by two to three b'),
])
    #?可以是匹配只进行一次，不会重头多次匹配
    test_patterns(
'abbaabbba',
[ ('ab*?', 'a followed by zero or more b'),
('ab+?', 'a followed by one or more b'),
('ab??', 'a followed by zero or one b'),
('ab{3}?', 'a followed by three b'),
('ab{2,3}?', 'a followed by two to three b'),
])
