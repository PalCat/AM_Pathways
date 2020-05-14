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
BLOOMS_TAXONOMY_FILE_PATH = "C:\\Pallavi\\NSF_AM_Pathways\\PythonScripts\\BloomsTaxonomyVerbs.xlsx"
ACRONYMS_PATH = "C:\\Pallavi\\NSF_AM_Pathways\\Acronyms.xlsx"

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
        level.append([""])
        print("No common elements")
  x = list(set(setVerbs).difference(allBlooms))
  notInBloomsList.extend(x)
  return level, notInBloomsList


'''
def print_table(rows, padding=0):
    """ Print `rows` with content-based column widths. """
    col_widths = [
      max(len(str(value)) for value in col) + padding
      for col in zip(*rows)
    ]
    total_width = sum(col_widths) + len(col_widths) - 1
    fmt = ' '.join('%%-%ds' % width for width in col_widths)
    print(fmt % tuple(rows[0]))
    print('~' * total_width)
    for row in rows[1:]:
      print(fmt % tuple(row))


def nounChunks(text):
  t_doc = nlp(text)
  sent = list(t_doc.sents)
  #print(sent[50])
  #html = displacy.render(sent[50], style="dep", page=True)
  #f = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\dep.html", 'w')
 # f.write(html)
  #ex = nlp("an operating system (os) is system software that manages computer hardware, software resources, and provides common services for computer programs.")
  # Sent Root
  for w in sent[500]:
    print(w.text, w.dep_, w.tag_)
  #for chunk in t_doc.noun_chunks:
   # print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
  s_doc = nlp("Understand the Six Sigma process and its impact on quality, customer satisfaction and costs")
  rows = [['Token', '|', 'Subtree']]
  for token in [s_doc[0]]:
    subtree = [
      ('((%s))' if t is token else '%s') % t.text
      for t in token.subtree
    ]
    rows.append([token.text, '|', ' '.join(subtree)])
  print_table(rows)
  
  '''
def nounChunks_trial(text):
  t_doc = nlp(text)
  verb_noun = []
  for sent in t_doc.sents:
    print(sent)
    html = displacy.render(sent, style="dep", page=True)
    f = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\dep.html", 'w')
    f.write(html)

    for tokens in sent:
      if tokens.pos_ == "VERB":
        for child in tokens.children:
          if "obj" in child.dep_:
            nounPhrase = child.text + " "
          elif "conj" in child.dep_:
            nounPhrase = child.text + " "
          elif (child.dep_ == 'prep'):
            temp_prep = child.text
            for gchild in child.rights:
              if 'obj' in gchild.dep_:
                nounPhrase += temp_prep + " " + gchild.text + " "
    verb_noun.append((tokens.text, nounPhrase))
    print(verb_noun)
  df = pd.DataFrame.from_records(verb_noun, columns=['Verb', 'Noun'])
  print(df)
  df.to_csv('C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\verb_noun.csv')

def nounChunks(text):
  t_doc = nlp(text)
  verb_noun = []
  for sent in t_doc.sents:
    print(sent)
    #print([token.dep_ for token in sent])
    html = displacy.render(sent, style="dep", page=True)
    f = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\dep.html", 'w')
    f.write(html)
    for w in sent.noun_chunks:
      nounPhrase = ''
      #print(w.text, w.dep_)
      print(w.text, w.root.text, w.root.dep_, w.root.head.text, w.root.head.tag_, w.root.head.dep_)
      if(w.root.head.pos_ == 'VERB'):
        nounPhrase = w.text + " "
      # split noun chunk and get the subtree of the last word
        last_word = w.text.split()[-1]
        for t in sent:
          if(t.text == last_word):
            #nounPhrase += [des.text for des in t.subtree if des.dep == 'conjunct']
            for des in t.rights:
              print(des.text, des.dep_)
              if des.dep_ == 'conjunct':
                nounPhrase += des.text + " "
              elif(des.dep_ =='prep'):
                temp_prep = des.text
                for gc in des.rights:
                  if 'obj' in gc.dep_:
                    nounPhrase += temp_prep +" "+ gc.text + " "
    verb_noun.append((w.root.head.text, nounPhrase))
    print(verb_noun)
  df = pd.DataFrame.from_records(verb_noun, columns=['Verb', 'Noun'])
  print(df)
  df.to_csv('C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\verb_noun.csv')

def nounChunks_orig(text):
  t_doc = nlp(text)
  t_doc = nlp("a function")
  t2_doc = nlp("functions")
  #print(nlp.pipeline)
  verb_noun = []
  for sent in t_doc.sents:
    print(sent)
    #print([token.dep_ for token in sent])
    html = displacy.render(sent, style="dep", page=True)
    f = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\dep.html", 'w')
    f.write(html)
    for x in sent.noun_chunks:
      print(x.text)
    for w in sent.noun_chunks:
      for tok in t2_doc:
        print(w.text, tok.text, w.similarity(tok))

      nounPhrase = ''
      #print(w.text, w.dep_)
      print(w.text, w.root.text, w.root.dep_, w.root.head.text, w.root.head.tag_, w.root.head.dep_)
      if(w.root.head.pos_ == 'VERB'):
        #verb_noun.append((w.root.head.text, w.text))
        if "subj" in w.root.dep_:
          root_rights = w.root.head.rights
          for r in root_rights:
            if "obj" in r.dep_:
              nounPhrase = r.text + " "
              for rgc in r.rights:
                if "conj" in rgc.dep_:
                  nounPhrase = rgc.text + " "
                elif (rgc.dep_ == 'prep'):
                  temp_prep = rgc.text
                  for rggc in rgc.rights:
                    if 'obj' in rggc.dep_:
                      nounPhrase += temp_prep + " " + rggc.text + " "
          break
        else:
          nounPhrase = w.text + " "
        # split noun chunk and get the subtree of the last word
          last_word = w.text.split()[-1]
          for t in sent:
            if(t.text == last_word):
              #nounPhrase += [des.text for des in t.subtree if des.dep == 'conjunct']
              for des in t.rights:
                print(des.text, des.dep_)
                if des.dep_ == 'conjunct':
                  nounPhrase += des.text + " "
                elif(des.dep_ =='prep'):
                  temp_prep = des.text
                  for gc in des.rights:
                    if 'obj' in gc.dep_:
                      nounPhrase += temp_prep +" "+ gc.text + " "
    verb_noun.append((w.root.head.text, nounPhrase))
    print(verb_noun)
  df = pd.DataFrame.from_records(verb_noun, columns=['Verb', 'Noun'])
  print(df)
  df.to_csv('C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\verb_noun.csv')
'''
      if(w.dep_ == 'compound'):
        x = w.text
        print([c.dep_ for c in w.head.children])
    
    #ent1, ent2 = get_entities(sent.text)
    #print(ent1, ent2)
  for sent in t_doc.sents:
    edges = []
    for w in sent:
      for c in w.children:
        edges.append(('{0}'.format(w.lower_),
                      '{0}'.format(c.lower_)))
    graph = nx.Graph(edges)
    entity1 = 'course'
    entity2 = 'present'
    print(nx.shortest_path_length(graph, source=entity1, target=entity2))
    print(nx.shortest_path(graph, source=entity1, target=entity2))
  
  print("Done!")

  '''

def getVerbs_Nouns(text):
  s_doc = nlp(text)
  #Remove stop words
  noStopwords = ''
  verbs = []
  nouns = []
  all_nouns_chunk = []
  all_nouns_root = []
  nouns_chunk = []
  noun_old_mth = []
  verb_old_mth = []
  bigram_dict = dict()
  for s in s_doc.sents:
    print(s.text)
    for w in s:
      if(nlp.vocab[w.text].is_stop == False):
        noStopwords += w.text + ' '
  file = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\nostop.txt", 'w')
  file.write(noStopwords)
  print("=========================================================================>>>>>>>>>>>>>>>>>>>>>>>",noStopwords)
  #get verbs
  #v_doc = nlp(noStopwords)
  v_doc = nlp(text)
  for t in v_doc:
    if t.pos_ == "VERB":
      verb_old_mth.append(t.text)
    if t.pos_ == "NOUN":
      noun_old_mth.append(t.text)
  print( "Verbs Old Method",verb_old_mth, " Number: ", len(verb_old_mth))
  print("Nouns Old Method", noun_old_mth, " Number: ", len(noun_old_mth))
  for s1 in v_doc.sents:
    print("Sentence: ", s1)
    print("Old Verb: ", [v.text for v in s1 if v.pos_ == "VERB"])
    html = displacy.render(s1, style="dep", page=True)
    f = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\dep.html", 'w')
    f.write(html)
    verb_child = []
    for n in s1.noun_chunks:
      #print("Chunk: ", n.text, " Chunk root: ", n.root, " Chunk root dep: ", n.root.dep_, " Chunk root head: ", n.root.head, " Chunk root head pos: ", n.root.head.pos_ )
      all_nouns_chunk.append(n.text)
      all_nouns_root.append(n.root)
      if n.root.head.pos_ == 'VERB':
        if "sub" in n.root.dep_ or "obj" in n.root.dep_:
          print("Verb new", n.root.head.text)
          print("Verb new", n.root.head.lemma_)
          #print("New Method ======> Noun root: ", n.root)
          #print("New Method Noun Chunk: ", n.text)
          nouns.append(n.root)
          nouns_chunk.append(n.text)

          #print("Verb: ", n.root.head.text, "Child: ", [child.text for child in n.root.head.children if "sub" in child.dep_ or "obj" in child.dep_])
          if(len(verb_child) <= 1 and n.root.text not in verb_child):
              verbs.append(n.root.head.lemma_)

              if(n.root.text not in verb_child):
                verb_child = [child.text for child in n.root.head.children if "sub" in child.dep_ or "obj" in child.dep_]
          #verb_child = [child.text for child in n.root.head.children if "sub" in child.dep_ or "obj" in child.dep_]

  print("Verbs new method",verbs, " Number: ", len(verbs))
  print("Nouns new method", nouns, " Number: ", len(nouns))
  print("Noun Chunks new method", nouns_chunk, " Number: ", len(nouns_chunk))
  print("All Nouns new method", all_nouns_root, " Number: ", len(all_nouns_root))
  print("All Noun Chunks new method", all_nouns_chunk, " Number: ", len(all_nouns_chunk))
  return verbs


def getBigrams(text):
  #spacyEx()
  bigram_dict = dict()
  v_doc = nlp(text)
  #index = 0
  #nounIndices = []

  '''
  print("length of v doc", len(v_doc))
  for en, token in enumerate(v_doc):
    if(en == 542):
      print("Check")
      # print(token.text, token.pos_, token.dep_, token.head.text)
    if token.pos_ == 'NOUN':
      nounIndices.append(index)
    index = index + 1
  for ind in nounIndices:
    span = v_doc[v_doc[ind].left_edge.i: v_doc[ind].right_edge.i + 1]
    with v_doc.retokenize() as retokenizer:
      retokenizer.merge(span)
    # span.merge()
    '''
  '''
    for s in v_doc.sents:
      #print(s.text)
      new_nouns = []
      for token in s.noun_chunks:
        if token.root.dep_ == 'dobj' or token.root.dep_ == 'pobj' or token.root.pos_ == "PRON":
          new_nouns.append(token.text)
          print(token.text, token.root.head.text, token.root.head.pos_)
    '''
  for s in v_doc.sents:
    html = displacy.render(s, style="dep", page=True)
    f = open("C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\dep.html", 'w')
    f.write(html)
    #nounChunks = []
    for t in s:
      print("t: ", t.text,  " t.dep_: ", t.dep_, " head text:", t.head.text, "head pos: ",t.head.pos_ )
      if "obj" in t.dep_ and t.head.pos_ == 'VERB':
        span = v_doc[t.left_edge.i: t.right_edge.i + 1]
        #print("edges: ", t.left_edge.i, " & ", t.right_edge.i)
        #print("Noun: ", t.text, "Span: ", span.text, " Verb: ", t.head.text)
        verb = t.head.lemma_
        #nounChunks.append(span.text)
        nounChunks = span.text
        if verb in bigram_dict.keys():
          value = bigram_dict[verb]
          value.append(nounChunks)
          bigram_dict[verb] = value
        else:
          bigram_dict[verb] = [nounChunks]
  for x, y in bigram_dict.items():
    print("The verb is: ", x, " and value is: ", y)
  return bigram_dict

'''
def misc():
    for n in s1.noun_chunks:
      nounChunks = []
      if n.root.head.pos_ == 'VERB' and "obj" in n.root.dep_:
        verb = n.root.head.lemma_
        nounChunks.append(n.text)
        if verb in bigram_dict.keys():
          value = bigram_dict[verb]
          nounChunks.extend(value)
          bigram_dict[verb] = nounChunks
        else:
          bigram_dict[verb] = nounChunks
  for x, y in bigram_dict.items():
    print("The verb is: ", x, " and value is: ", y)
  return bigram_dict
'''
def spacyEx():
  nlp = spacy.load("en_core_web_sm")
  doc = nlp("Displaying a willingness to learn and apply new knowledge and skills.")#This course provides the foundation for electronic circuits and measurements.
  span = doc[doc[4].left_edge.i: doc[4].right_edge.i + 1]
  with doc.retokenize() as retokenizer:
    retokenizer.merge(span)
  #for token in doc:
   # print(token.text, token.pos_, token.dep_, token.head.text)

  doc1 = nlp("Displaying a willingness to learn and apply new knowledge and skills. This course provides the foundation for electronic circuits and measurements.")
  for s in doc1.sents:
    for t in s:
      if "obj" in t.dep_ and t.head.pos_ == 'VERB':
        span2 = doc1[t.left_edge.i: t.right_edge.i + 1]
        print("edges: ", t.left_edge.i, " & ", t.right_edge.i)
        print("Noun: ", t.text, "Span: ", span2.text, " Verb: ", t.head.text)
        #span1.merge()
        #with doc.retokenize() as retokenizer:
         # retokenizer.merge(span1)



def sentSimilarity():
  os.environ["TFHUB_CACHE_DIR"] = 'C:/Pallavi/PyCharm/venv/USE_Module/'
  handle = "https://tfhub.dev/google/universal-sentence-encoder/4"
  hashlib.sha1(handle.encode("utf8")).hexdigest()
  emb = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
  phrase1 = "analyze electronic circuits"
  phrase2 = "analyze circuits"
  phrase_vect1 = emb([phrase1])
  phrase_vect2 = emb([phrase2])
  similarity_val = np.inner(phrase_vect1, phrase_vect2)
  print(similarity_val)
  print("done")
