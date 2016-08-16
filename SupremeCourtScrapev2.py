from bs4 import BeautifulSoup, SoupStrainer

import requests
import re
import string
import sys

_fix_mixed_unicode_re = re.compile("([\x7F-\xFF]+)")
def fix_mixed_unicode(mixed_unicode):
    assert isinstance(mixed_unicode, unicode)
    def handle_match(match):
        return match.group(0).encode("raw_unicode_escape").decode("1252")
    return _fix_mixed_unicode_re.sub(handle_match, mixed_unicode)


def scrapeCornellLow(url):
    r  = requests.get("https://" +url)

    data = r.text
    data = data.replace("&#151;","&#45;")
    data = data.replace("&#148;","&#34;")
    data = data.replace("&#147;","&#34;")
    data = data.replace("&#146;","&#39;")
    data = data.replace("&#167;","sec.")

    soup = BeautifulSoup(data)
    for link in soup.findAll('a'):
        try:
            if link.has_attr('href'):
                topic = link.text
                if ("syllabi" in link['href']):
                    print "topic link text: "+topic+"\t\t ***: "+link['href']
                    scrapeLawCases(link['href'], topic)
        except:
            print sys.exc_info()[0]
            for ch in textStr:
                print ch+" "+str(ord(ch))
            print "exception = "+link.text.encode('utf-8','ignore')


def scrapeLawCases(url, topic):
    print "enter scrapeLawCases "+url
    url = "https://www.law.cornell.edu" +url
    print "url = "+url
    r  = requests.get(url)

    data = r.text
    data = data.replace("&#151;","&#45;")
    data = data.replace("&#148;","&#34;")
    data = data.replace("&#147;","&#34;")
    data = data.replace("&#146;","&#39;")
    data = data.replace("&#167;","sec.")

    soup = BeautifulSoup(data)
    for link in soup.findAll('a'):
        try:
            if link.has_attr('href'):
                textStr = re.sub(r'[^\x00-\x7F]',' ', link.text)
                if (".ZS.html" in link['href']):
                    print "case link : "+textStr+"\t\t ***: "+link['href']
        except:
            print sys.exc_info()[0]
            for ch in textStr:
                print ch+" "+str(ord(ch))
            print "exception = "+link.text.encode('utf-8','ignore')
            

def scapeWebSyllabus(url, topic):
    r  = requests.get("https://" +url)

    data = r.text
    data = data.replace("&#151;","&#45;")
    data = data.replace("&#148;","&#34;")
    data = data.replace("&#147;","&#34;")
    data = data.replace("&#146;","&#39;")
    data = data.replace("&#167;","sec.")

    soup = BeautifulSoup(data)

    action = soup.find(attrs={"name":"ACTION"})
    argDate = soup.find(attrs={"name":"ARGDATE"})
    caseName = soup.find(attrs={"name":"CASENAME"})
    courtBelow = soup.find(attrs={"name":"COURTBELOW"})
    decDate = soup.find(attrs={"name":"DECDATE"})
    docket = soup.find(attrs={"name":"ACTION"})
    caseNameStr = caseName["content"]
    print caseNameStr+"\n"
    if " v. " in caseNameStr:
        plantiff = caseNameStr.split(" v. ")[0];
        defendant = caseNameStr.split(" v. ")[1];
    elif " V. " in caseNameStr:
        plantiff = caseNameStr.split(" V. ")[0];
        defendant = caseNameStr.split(" V. ")[1];

    print ("url:  "+url+"\n")
    print ("topic:  "+topic +"\n")
    print ("action:  "+action["content"] +"\n")
    print ("argDate:  "+argDate["content"] +"\n")
    print ("caseName:  "+caseName["content"] +"\n")
    print ("decDate:  "+decDate["content"] +"\n")
    print ("docket:  "+docket["content"] +"\n")
    print ("courtBelow:  "+courtBelow["content"] +"\n")
    print ("plantiff:  "+plantiff +"\n")
    print ("defendant:  "+defendant +"\n")

    # syllabus
    # need authors (justices)
    # opinion
    # descent 
    # unanimous? //*[@id="content"]/p[4]
     
    page = soup.findAll('p')
    i=1
    for p in page:
        textStr = fix_mixed_unicode(p.text)
         
        textStr = textStr.encode('utf-8','ignore')
        clean = re.sub('[\0\200-\377]', '', textStr)
        # textStr = re.sub("\xe2\x80\x93", "-", textStr)
        # textStr = re.sub("\x00\xa0", "-", textStr)
            
        print (clean)
        #for ch in clean:
        #    print ch+" "+str(ord(ch))
        #if i>3:
        #    break
        #i += 1

    for link in soup.findAll('a'):
        try:
            if link.has_attr('href'):
                textStr = link.text
                print "link text: "+textStr+"\t\t ***: "+link['href']
        except:
            for ch in textStr:
                print ch+" "+str(ord(ch))
            print "exception = "+link.text.encode('utf-8','ignore')



def main():
    #url = "www.law.cornell.edu/supct/search/display.html?terms=tax&url=/supct/html/98-2043.ZS.html"
    url = "www.law.cornell.edu/supct/topiclist.html#T"
    scrapeCornellLow(url)


if __name__ == '__main__':
    main()
