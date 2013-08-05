from bs4 import BeautifulSoup
import urllib2
import re

tao = urllib2.urlopen("http://leocharre.com/wp-content/uploads/tao_te_ching_translated_by_wing_tsit_chan.html")
tao_html = tao.read()
tao.close()

soup = BeautifulSoup(tao_html)

lines = re.split('(\d+.\d)', soup.get_text())[1:]
print lines

f = open('taoteching.txt', 'w')

cur = 0
for i, line in enumerate(lines):
    if len(line) == 0: continue # skip empty strings
    if i % 2 == 0:              # even lines are chapter numbers
        chapter = int(float(line))
        if cur != chapter:
            f.write('\n' + str(chapter) + '\n')
            cur = chapter
    else:
        f.write(line.strip() + '\n')


f.close()
