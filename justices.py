from bs4 import BeautifulSoup, SoupStrainer

import requests
import re
import string

_fix_mixed_unicode_re = re.compile("([\x7F-\xFF]+)")
def fix_mixed_unicode(mixed_unicode):
    assert isinstance(mixed_unicode, unicode)
    def handle_match(match):
        return match.group(0).encode("raw_unicode_escape").decode("1252")
    return _fix_mixed_unicode_re.sub(handle_match, mixed_unicode)

url = "en.wikipedia.org/wiki/List_of_Justices_of_the_Supreme_Court_of_the_United_States"

r  = requests.get("https://" +url)

data = r.text
data = data.replace("&#151;","&#45;")
data = data.replace("&#160;","&#34;")
data = data.replace("&#147;","&#34;")
data = data.replace("&#146;","&#39;")

dash = [226, 128, 147]
dashChar = "".join(map(chr, dash))

soup = BeautifulSoup(data)

#for links in soup.find_all("span"):
#    links.decompose()
[span.extract() for span in soup.find_all("span")] 
  
table = soup.find(class_="wikitable sortable")
for row in table.find_all('tr')[1:]:
    cols = row.findAll('td')
    #page_text = cols.text.encode('utf-8').decode('ascii', 'ignore')
    #for c in cols:
    #    print repr(c.text)
    try:
        num, judge, state, bornDied, activeYears, Chief, Retire, AppointedBy, termination = [c.text.encode('utf-8',errors='backslashreplace') for c in cols]
        #num, judge, state, bornDied, activeYears, Chief, Retire, AppointedBy, termination = [c.text.encode('utf-8').decode('ascii') for c in cols]
        judge = re.sub('[\0\200-\377]', '', judge)
        print "judge = "+judge
        print "state = "+state
        activeYears = activeYears.replace(dashChar,"-")
        print "active years = "+activeYears
      #  for ch in activeYears:
      #          print ch+" "+str(ord(ch))
      #  break        
      #  print "repr ="+repr(c.text)
        
    except Exception, e:
        for c in cols:
            print "repr r = "+repr(c.text)
            for ch in c.text.encode('utf-8').decode('ascii'):
                print ch+" "+str(ord(ch))
            break
        print repr(e)
        break
                
        
   
