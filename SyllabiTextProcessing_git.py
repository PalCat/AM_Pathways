import hashlib

import nltk
from nltk.corpus import stopwords
from spacy.lemmatizer import Lemmatizer
import string
import re
import pandas as pd
import spacy
punctuations = string.punctuation
import os
from NSF_AM_Pathway import ReadIni
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
from IPython.core.display import display, HTML
import sys
import networkx as nx
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
import numpy as np

RESULT_LOC, RESULT_CUR_DIR, COLLEGE, ROOT_DIR, SYLLABI_LOC, REPORT_TYPE, COURSE_TYPE = ReadIni.getINIVariables()
# Read from ini
BLOOMS_TAXONOMY_FILE_PATH = ""
ACRONYMS_PATH = ""

lemmatizer = spacy.lemmatizer.Lemmatizer
#nlp = spacy.load('en_core_web_sm')
#nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg')

def getAcronymsDict():
  try:
    acronyms = pd.read_excel(ACRONYMS_PATH)
    f = lambda x: x.lower()
    acronyms_l = acronyms.applymap(f)
    acronyms_dict = dict()
    lastRow = acronyms_l.last_valid_index()
    for a in range(lastRow):
      acronyms_dict.update({acronyms_l.iloc[a]['Acronym']: acronyms_l.iloc[a]['Expansion']})
  except:
    print("getAcronymsDict----> Acronyms file not found.")
  return acronyms_dict

def getFiles(syllabiDir):
  files = []
  if(syllabiDir != None):
    try:
      for i in range(len(syllabiDir)):
        if os.path.exists(syllabiDir[i]):
          for r, d, f in os.walk(syllabiDir[i]):
            for file in f:
              if( ".txt" in file):
                files.append(os.path.join(r,file))
        else:
          print("Syllabi directory" +syllabiDir[i] +"not found.")
          #raise Exception("Syllabi directory" +syllabiDir[i] +"not found.")
          #sys.exit()
    except:
      print("Unable to find files. Please check the given directory path.")
  return files

def getTextFromSyllabi(syllabiDir):
  syllabiText = ""
  try:
    fileName = getFiles(syllabiDir)
    if len(fileName) != 0:
      for index, f in enumerate(fileName):
        syllabus = open(f)
        syllabiText += syllabus.read().lower()
    else:
      raise Exception("No files found in the syllabus directory")
  except:
    print("Unable to get text from file.")
  return syllabiText

def removeStopWords(text):
  stop_words = set(stopwords.words("english"))
  stop_words.remove('to')
  add_stopwords = ['?', ',', '.', '[', ']', ':', '(', ')', '/"', "\'", '//']
  stop_words.update(add_stopwords)
  for w in stop_words:
    text1 = text.replace(w, "")
  return text1

def textCleanUp(text):
  cleanText = ""
  acronyms_dict = getAcronymsDict()
  for a in acronyms_dict:
    text = re.sub(acronyms_dict[a], a, text)  # Convert programmable logic controller -> plc
    text = re.sub(r'\([' + a + ')]*\)', '', text)  # remove repetations of plc (plc). discard "(plc)"
  text = re.sub("alternating current", "ac", text)  # alternating current is not changing. explicit conversion for now
  text = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", text)
  text = re.sub('[^A-Za-z0-9]+', ' ', text)
  pattern = '[0-9]'
  text = re.sub(pattern, '', text)
  cleanText = removeStopWords(text)
  return cleanText

def createCSVFromList(list, fileName):
  dataFrame = pd.DataFrame(list)
  if not os.path.exists(RESULT_LOC):
    os.makedirs(RESULT_LOC)
  if not os.path.exists(RESULT_LOC + RESULT_CUR_DIR):
    os.makedirs(RESULT_LOC + RESULT_CUR_DIR)
  dataFrame.to_csv(RESULT_LOC+RESULT_CUR_DIR+"\\"+fileName +".csv")
  freq = nltk.FreqDist(list)
  dataFreq = pd.DataFrame.from_dict(freq,orient='index')
  dataFreq.to_csv(RESULT_LOC+RESULT_CUR_DIR + "\\" + fileName + "_freq.csv")

def getVerbNounLemma(cleanText):
  verbLemma = []
  nounLemma = []
  acronyms_dict = getAcronymsDict()
  doc = nlp(cleanText)
  for w in doc:
    if(w.text not in acronyms_dict):
      if "VERB" in w.pos_:
        verbLemma.append(w.lemma_)
      elif ("NOUN" in w.pos_ or "PROPN" in w.pos_):
        nounLemma.append(w.lemma_)
  createCSVFromList(verbLemma, "verbLemma"+COLLEGE+"_"+ COURSE_TYPE)
  createCSVFromList(nounLemma, "nounLemma"+COLLEGE+"_"+ COURSE_TYPE)
  return verbLemma, nounLemma

def getVerbNounPair(cleanText):
  verbNounPair = []
  acronyms_dict = getAcronymsDict()
  doc = nlp(cleanText)
  for x in doc:
    if "NP" in x.pos_:
      print("Found an NP!", x.text)
  for i, w in enumerate(doc):
    if i < len(doc)-1:
      if(w.text not in acronyms_dict and doc[i+1].text not in acronyms_dict):
        if(("NOUN" in w.pos_ or "PROPN" in w.pos_) and "VERB" in doc[i+1].pos_):
          comb1 = w.text + ":" + doc[i + 1].text
          verbNounPair.append(comb1)
  createCSVFromList(verbNounPair, "verbNounPair"+COLLEGE+"_"+ COURSE_TYPE)
  return verbNounPair

def getBloomsLevelVerbs():
  verbs = []
  allBlooms = []
  columnNames = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating", "Remove"]
  df = pd.read_excel(BLOOMS_TAXONOMY_FILE_PATH, sep = ',', header = 0).fillna("")
  f = lambda x: x.lower()
  df_lower = df.applymap(f)
  for i, c in enumerate(columnNames):
    verbs.append(list(df_lower[c]))
    allBlooms.extend(verbs[i])
  return verbs, allBlooms

def classifyToBloomsLevel(verbs):
  level = []
  notInBloomsList = []
  setBlooms = []
  bloomsVerbs, allBlooms = getBloomsLevelVerbs()
  setVerbs = verbs
  for i in range(7):
      setBlooms.append(set(bloomsVerbs[i]))
      if (setVerbs & setBlooms[i]):
          level.append(list(setVerbs & setBlooms[i]))
          mTemp = set(setVerbs).difference(level[i])
          setVerbs = mTemp
      else:
          print("No common elements")
  x = list(set(setVerbs).difference(allBlooms))
  notInBloomsList.extend(x)
  return level, notInBloomsList
