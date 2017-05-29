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
    def __init__(self):
        with open("enable1.txt") as enable:
            self.l = []
            for line in enable:
                self.l.append(line)
            self.l = [i.strip() for i in self.l]
        
        self.wordList = self.l
            
    def randWord(self):
        #Prints a random word from the inputted word list
        return self.wordList[randint(0,len(self.wordList)-1)]
    
    def definition(self, word):
        while 1:
            try:
                #Get dictionary.com
                link = "http://www.dictionary.com/browse/"+word
                site = requests.get(link).text
                soup = BeautifulSoup(site,"lxml")
                #Find the divs with the definition and part of speech
                divs = soup.findAll("div", {"class":"def-content"})
                pos = soup.findAll("span", {"class":"dbox-pg"})
                #Remove HTML formatting from extracted text
                definition = re.sub("<[^>]+?>","", str(divs[0])).strip()
                pos = re.sub("<[^>]+?>","", str(pos[1])).strip()
                break
            except IndexError:
                word = self.randWord()
                continue
        return "\nWord: " + word + "\n\nPart of Speech: " + pos + "\n\nDefinition: " + definition
    
    def synonyms(self, word):
        site = requests.get("http://www.synonym.com/synonyms/" + word,"lxml")
        soup = BeautifulSoup(site.text)
        syn = soup.findAll("li",{"class" : "syn"})
        syns = []
        for i in syn:
            href = BeautifulSoup(str(i)).findAll("a",{"href" : lambda x: x and "/synonyms/" in x})[0]
            syns.append(href.text)
            
        return "Synonyms: " + ", ".join(syns[:10])
    
    def regexFind(self,pattern):
        #Compile the pattern and search through the inputted list for matches
        r = re.compile(pattern)
        found = filter(r.match,self.wordList)
        if len(found) > 100:
            yn = raw_input("Found " + str(len(found)) + " matches, " + "print them all? (Y/N): ")
            if yn in "Yy":
                return "Found " + str(len(found)) + " results: " + ", ".join(found)
            else:
                return "Did not print."
        else:
            return "Found " + str(len(found)) + " results: " + ", ".join(found)
    
    def wordVariations(self,word):
        r = re.compile(word)
        found= filter(r.match,self.wordList)
        return "Found " + ", ".join(found)
