from bs4 import BeautifulSoup, SoupStrainer

import requests
import re
import string
import sys, traceback

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
            traceback.print_exc(file=sys.stdout)
            print sys.exc_info()[0]
            for ch in topic:
                print ch+" "+str(ord(ch))
            print "exception = "+link.text.encode('utf-8','ignore')
            sys.exit(-1)

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
                    scrapeWebSyllabus(link['href'],topic)
        except:
            print sys.exc_info()[0]
            traceback.print_exc(file=sys.stdout)
            for ch in textStr:
                print ch+" "+str(ord(ch))
            print "exception = "+link.text.encode('utf-8','ignore')
            sys.exit(-1)

            

def scrapeWebSyllabus(url, topic):
    print 'enter scrapewebsyllabus'
    url = "https://www.law.cornell.edu" +url
    r  = requests.get(url)

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
    try:
        caseNameStr = caseName["content"]
        print caseNameStr+"\n"
    except:
        caseNameStr = "empty?"
    plantiff = "empty?"
    defendant = "empty?"
    if " v. " in caseNameStr:
        plantiff = caseNameStr.split(" v. ")[0];
        defendant = caseNameStr.split(" v. ")[1];
    elif " V. " in caseNameStr:
        plantiff = caseNameStr.split(" V. ")[0];
        defendant = caseNameStr.split(" V. ")[1];
    else:
        print "ERROR no v. or V."
        

    print ("***** Case information ******")
    print ("url:  "+url+"\n")
    print ("topic:  "+topic +"\n")
    try:
        action = action["content"]
        print ("action:  "+action["content"] +"\n")
    except:
        action = "empty? "
    try:
        argDate = argDate["content"]
        print ("argDate:  "+argDate["content"] +"\n")
    except:
        argDate = "empty?"
    try:
        caseName = caseName["content"]
        print ("caseName:  "+caseName["content"] +"\n")
    except:
        caseName = "empty?"
    try:
        decDate = decDate["content"]
        print ("decDate:  "+decDate["content"] +"\n")
    except:
        decDate = "empty?"
    try:
        docket = docket["content"]
        print ("docket:  "+docket["content"] +"\n")
    except:
        docket = "empty?"
    try:
        courtBelow = courtBelow["content"]
        print ("courtBelow:  "+courtBelow["content"] +"\n")
    except:
        courtBelow = "empty?"    
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
                clean = textStr.encode('utf-8','ignore')
                print "link text: "+clean+"\t\t ***: "+link['href']
        except:
            traceback.print_exc(file=sys.stdout)
            for ch in textStr:
                print ch+" "+str(ord(ch))
            print "exception = "+link.text.encode('utf-8','ignore')
            sys.exit(-1)




def main():
    #url = "www.law.cornell.edu/supct/search/display.html?terms=tax&url=/supct/html/98-2043.ZS.html"
    url = "www.law.cornell.edu/supct/topiclist.html#T"
    scrapeCornellLow(url)


if __name__ == '__main__':
    main()
