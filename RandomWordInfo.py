import requests
from bs4 import BeautifulSoup
from random import randint
import re

#Convert 'enable1.txt' to list form
with open("enable1.txt") as enable:
    l = []
    for line in enable:
        l.append(line)
    l = [i.strip() for i in l]
    
class WordInfo:
    def __init__(self, wordList):
        self.wordList = wordList
    
    def randWord(self):
        return self.wordList[randint(0,len(self.wordList)-1)]
    
    def definition(self, word):
        #This next section would randomly throw an IndexError, so I just made a
        #try-except catch that just gets another random word in case one came 
        #up.
        while 1:
            try:
                #Get dictionary.com
                link = "http://www.dictionary.com/browse/"+word
                site = requests.get(link).text
                soup = BeautifulSoup(site,"lxml")
                divs = soup.findAll("div", {"class":"def-content"})
                pos = soup.findAll("span", {"class":"dbox-pg"})
                #Remove HTML formatting from extracted text
                definition = re.sub("<[^>]+?>","", str(divs[0])).strip()
                pos = re.sub("<[^>]+?>","", str(pos[1])).strip()
                break
            except IndexError:
                word = self.randWord()
        return "\nWord: " + word + "\n\nPart of Speech: " + pos + "\n\nDefinition: " + definition
    
    def synonyms(self, word):
        link = "http://www.thesaurus.com/browse/"+word
        site = requests.get(link).text
        soup = BeautifulSoup(site,"lxml")
        spans = soup.findAll("span", {"class":"text"})
        spans = [re.sub("<[^>]+?>","",str(x)).strip() for x in spans]
        return "\nSynonyms: " + ", ".join(spans[0:3])
    
    def regexFind(self,pattern):
        r = re.compile(pattern)
        found = filter(r.match,self.wordList)
        return "Found: " + ", ".join(found)

w = WordInfo(l)
#word = raw_input("Enter a word: ")
#print w.definition(word)
#print w.synonyms(word)
print w.regexFind("q[^u]")
