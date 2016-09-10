from bs4 import BeautifulSoup, SoupStrainer

import requests
import re
import string
import sys, traceback
import codecs



#_fix_mixed_unicode_re = re.compile("([\x7F-\xFF]+)")
#def fix_mixed_unicode(mixed_unicode):
#    assert isinstance(mixed_unicode, unicode)
#    def handle_match(match):
#        return match.group(0).encode("raw_unicode_escape").decode("1252")
#    return _fix_mixed_unicode_re.sub(handle_match, mixed_unicode)

outcsv = None

def scrapeCornellLow(url):
    r  = requests.get("https://" +url)

    data = r.text
    data = data.replace("&#151;","&#45;")
    data = data.replace("&#148;","&#34;")
    data = data.replace("&#147;","&#34;")
    data = data.replace("&#146;","&#39;")
    data = data.replace("&#167;","sec.")
    print ("scrape url = "+url)
    soup = BeautifulSoup(data, "lxml")
    for link in soup.findAll('a'):
        try:
            if link.has_attr('href'):
                topic = link.text
                if ("/supct/cases/topics" in link['href']):
                    print( "topic link text: "+topic+"\t\t ***: "+link['href'] )
                    scrapeLawCases(link['href'], topic)
                    #outcsv.close()
                    #sys.exit(-10)
        except:
            traceback.print_exc(file=sys.stdout)
            print (sys.exc_info()[0])
            for ch in topic:
                print( ch+" "+str(ord(ch)))
            print( "exception = "+link.text.encode('utf-8','ignore'))
            sys.exit(-1)

def scrapeLawCases(url, topic):
    print( "enter scrapeLawCases** "+url)
    url = "https://www.law.cornell.edu" +url
    print( "url = "+url)
    r  = requests.get(url)

    data = r.text
    data = data.replace("&#151;","&#45;")
    data = data.replace("&#148;","&#34;")
    data = data.replace("&#147;","&#34;")
    data = data.replace("&#146;","&#39;")
    data = data.replace("&#167;","sec.")

    soup = BeautifulSoup(data, "lxml")
    for link in soup.findAll('a'):
        try:
            if link.has_attr('href'):
                print ("html = "+link['href'])
                textStr = re.sub(r'[^\x00-\x7F]',' ', link.text)
                print("textStr = "+textStr)
                if (link['href'].endswith("ZS.html")):
                    print( "case link : "+textStr+"\t\t ***: "+link['href'])
                    scrapeWebSyllabus(textStr, link['href'],topic)
                    #outcsv.close()
                    #sys.exit(-1)
        except:
            print (sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)
            for ch in textStr:
                print( ch+" "+str(ord(ch)))
            print( "exception = "+link.text.encode('utf-8','ignore'))
            sys.exit(-1)

            

def scrapeWebSyllabus(casetitle, url, topic):
    global outcsv
    
    url = "https://www.law.cornell.edu" +url
    print( 'enter scrapewebsyllabus '+url)
    r  = requests.get(url)

    data = r.text
    data = data.replace("&#151;","&#45;")
    data = data.replace("&#148;","&#34;")
    data = data.replace("&#147;","&#34;")
    data = data.replace("&#146;","&#39;")
    data = data.replace("&#167;","sec.")

    soup = BeautifulSoup(data, "lxml")

    action = soup.find(attrs={"name":"ACTION"})
    argDate = soup.find(attrs={"name":"ARGDATE"})
    caseName = soup.find(attrs={"name":"CASENAME"})
    courtBelow = soup.find(attrs={"name":"COURTBELOW"})
    decDate = soup.find(attrs={"name":"DECDATE"})
    docket = soup.find(attrs={"name":"DOCKET"})
    if (caseName == None):
        caseContent = soup.find('casecontent')
        #print ("caseContent = "+repr(caseContent.contents))
        #print ("length = "+str(len(caseContent.contents)))
        # NOTE: 1 is arbitrary
        if (len(caseContent.contents) > 1): 
            if (not parseTocHeader(soup,url,topic)):
                print ("******* NEED DIFFERENT PARSER! ")
                sys.exit(-10)
            parseOpinions(soup)   
    else:
        try:
            caseNameStr = caseName["content"]
            print( caseNameStr+"\n")
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
            print( "ERROR no v. or V.")
            

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
            print ("argDate:  "+argDate +"\n")
        except:
            argDate = "empty?"
        try:
            caseName = caseName["content"]
            print ("caseName:  "+caseName +"\n")
        except:
            caseName = "empty?"
        try:
            decDate = decDate["content"]
            print ("decDate:  "+decDate +"\n")
        except:
            traceback.print_exc(file=sys.stdout)
            decDate = "empty?"
        try:
            docket = docket["content"]
            print ("docket:  "+docket +"\n")
        except:
            traceback.print_exc(file=sys.stdout)
            docket = "empty?"
        try:
            courtBelow = courtBelow["content"]
            print ("courtBelow:  "+courtBelow +"\n")
        except:
            traceback.print_exc(file=sys.stdout)
            courtBelow = "empty?"    
        print ("plantiff:  "+plantiff +"\n")
        print ("defendant:  "+defendant +"\n")
        
        outcsv.write(topic+"|"+caseNameStr+"||"+plantiff+"|"+defendant+"|"+docket+"|"+argDate+"|"+action+"|"+url+"\n")
    
    
    # syllabus
    # need authors (justices)
    # opinion
    # descent 
    # unanimous? //*[@id="content"]/p[4]
     
    page = soup.findAll('p')
    i=1
    for p in page:
        textStr = p.text #fix_mixed_unicode(p.text)
         
        textStr = textStr.encode('utf-8','ignore')
        clean = textStr #re.sub('[\0\200-\377]', '', textStr)
        # textStr = re.sub("\xe2\x80\x93", "-", textStr)
        # textStr = re.sub("\x00\xa0", "-", textStr)
            
        print (clean)
        #for ch in clean:
        #    print ch+" "+str(ord(ch))
        #if i>3:
        #    break
        #i += 1
        
    '''
    THE CODE BELOW WILL NOT WORK FOR
    <ul class="writingtoc">
        <li>
            <span class="writnav">
                <b>opinion</b>, GINSBURG</span>
            <a href="#writing-type-1-GINSBURG">
                <span class="writnav"> [HTML] </span>
            </a>
        </li>
    '''

    for link in soup.findAll('a'):
        try:
            if link.has_attr('href'):
                textStr = link.text
                clean = link.text #textStr.encode('utf-8','ignore')
                #clean = re.sub('[\0\200-\377]', '', textStr)
                #print "link text: "+clean+"\t\t ***: "+link['href']
                if (re.search("ZO[1-9]*\.html", link['href'], flags=0) != None):
                    print( "OPINION FOUND = "+"link text: "+clean+"\t\t ***: "+link['href'])
                elif (re.search("ZC[1-9]*\.html", link['href'], flags=0) != None):
                    print( "Concurrence FOUND = "+"link text: "+clean+"\t\t ***: "+link['href'])
                elif (re.search("ZD[1-9]*\.html", link['href'], flags=0) != None):
                    print( "Dissent FOUND = "+"link text: "+clean+"\t\t ***: "+link['href'])
                elif (re.search("[1-9]+\s*U\.\s*S\.\s*[1-9]+", clean, flags=0) != None):
                    print( "Citation FOUND = "+"link text: "+clean+"\t\t ***: "+link['href'])
                elif (re.search("[1-9]+\s*U\.\s*S\.\s*C\.[\(\)a-z0-9\s]*", clean, flags=0) != None):
                    print( "Code FOUND = "+"link text: "+clean+"\t\t ***: "+str(link['href']))
                                                

        except:
            traceback.print_exc(file=sys.stdout)
            #for ch in textStr:
            #    print( ch+" "+str(ord(ch)))
            #print( "exception = "+link.text.encode('utf-8','ignore'))
            

def strip_tags(html):
    soup = BeautifulSoup(html)
     
    for tag in soup.findAll(True):
        s = ""

        for c in tag.contents:
            s += unicode(c)

            tag.replaceWith(s)

    return soup

    
'''
    Example 1    
    <ul class="writingtoc">
            <li>
                <span class="writnav">
                    <a href="#writing-USSC_CR_0410_0113_ZS">
                        <b>Syllabus</b>
                    </a>
                </span>
            </li>
            <li>
                <span class="writnav">
                    <a href="#writing-USSC_CR_0410_0113_ZO">
                        <b>Opinion</b>, Blackmun</a>
                </span>
            </li>
'''
def parseOpinions(soup):
    ulList = soup.find_all('ul', class_="writingtoc")
    for ul in ulList:
        for li in ul.findAll('li'):
            linkList = li.findAll('a')
            for link in linkList:
                textStr = link.text #strip_tage(li.text)
                print ("header line = "+textStr + " href = "+link['href'])
        
            
def parseTocHeader(soup,url,topic):
    global outcsv
    rtnTrue = True
    TocItems = []
    parties = []
    casename = []
    try:
        tocList = soup.find_all('p', class_="toccaption")
        #print ("parseToc = "+str(len(tocList))+" "+repr(tocList))
        for toc in tocList:
            textStr = toc.text # does not work ->strip_tags(toc.text)
            print ("header line = "+textStr)
            textStr = textStr.replace("\n","")
            TocItems.append(textStr)
        if (len(TocItems) < 4):
            outcsv.write(topic+"|"+repr(tocList)+"|empty|empty|empty|empty|empty|empty|empty|"+url+"\n")
            outcsv.flush()        
        else:
            try:
                casename = TocItems[1].split("(No.")
                casename[1] = "(No." + casename[1]
            except:
                try:
                    casename = TocItems[1].split("(Nos.")
                    casename[1] = "(Nos." + casename[1]
                except:
                    casename.append(TocItems[1])
                    casename.append("Empty?")
            if (len(casename) == 0):
                casename.append(TocItems[0])
                casename.append("Empty?")
            if "EX PARTE" in casename[0].upper() or "IN RE" in casename[0].upper():
                parties.append(casename[0])
                parties.append(casename[0])            
            else:
                try:
                    if (" v. " in casename[0]):
                        parties = casename[0].upper().split("V.")
                    print ("split v. parties = "+repr(parties))
                    if (len(parties) < 2):
                        parties.append(casename[0])
                        parties.append(casename[0])                                    
                except:
                    print ("exception casename = "+repr(casename))
                    print ("parties = "+repr(parties))
                    parties.append(casename[0])
                    parties.append(casename[0])
                    print ("except parties = "+repr(parties))
                    casename.append(TocItems[1])
                    casename.append("empty?")        
            try:                
                outcsv.write(topic+"|"+casename[0]+"|"+TocItems[0]+"|"+parties[0]+"|"+parties[1]+"|"+casename[1]+"|"+TocItems[2]+"|"+TocItems[3]+"|"+TocItems[2]+"|"+url+"\n")
                outcsv.flush()
            except:
                outcsv.write(topic+"|"+repr(tocList)+"|empty|empty|empty|empty|empty|empty|empty|"+url+"\n")
                outcsv.flush()
                    
    except:
        print ("topic = "+topic)
        print ("casename = "+repr(casename))
        print ("TocItems = "+repr(TocItems))
        print ("parties = "+repr(parties))
        print ("toclist = "+repr(tocList))        
        traceback.print_exc(file=sys.stdout)
        rtnTrue = False
    return rtnTrue

def main():
    global outcsv
    #if sys.stdout.encoding != 'cp850':
    #    sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
    #if sys.stderr.encoding != 'cp850':
    #    sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')
    # test
    #socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9051)
    #socket.socket = socks.socksocket
   # url = "www.law.cornell.edu/supct/search/display.html?terms=tax&url=/supct/html/98-2043.ZS.html"
   # url = "/supct/search/display.html?terms=tax&url=/supct/html/98-2043.ZS.html"
   # url = "/supct/search/display.html?terms=abortion&url=/supct/html/99-830.ZS.html"
   # url = "/supct/search/display.html?terms=bankruptcy&url=/supct/html/10-179.ZS.html"
    #scrapeWebSyllabus(url, "test")
    #print requests.get("https://icanhazip.com").text
    outcsv = open("./scotus_syllabus3.csv","w")
    outcsv.write("topic,casename, pubref,plantiff,defendant,docket num,argued,decided, ruling,url\n")
    url = "www.law.cornell.edu/supct/cases/topic.htm"
    scrapeCornellLow(url)
    outcsv.close()


if __name__ == '__main__':
    main()
