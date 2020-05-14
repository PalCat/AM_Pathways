from NSF_AM_Pathway import ReadIni
from NSF_AM_Pathway import SyllabiTextProcessing
from NSF_AM_Pathway import SentenceEncoder
from NSF_AM_Pathway import Reports

#SyllabiTextProcessing.sentSimilarity()
#SyllabiTextProcessing.nounChunks_orig("syllabusT")
#SyllabiTextProcessing.getVerbs_Nouns("")
RESULTS_LOC, RESULT_CUR_DIR, COLLEGE_NAME, SYLLABI_ROOT_LOC, SYLLABI_LOC, REPORT_TYPE, COURSE_TYPE = ReadIni.getINIVariables()
print(ReadIni.getINIVariables())
#Text Processing
syllabusT = SyllabiTextProcessing.getTextFromSyllabi(SYLLABI_LOC)
#SyllabiTextProcessing.nounChunks(syllabusT)
#new_verb = SyllabiTextProcessing.getVerbs_Nouns(syllabusT)
#new_dict = SyllabiTextProcessing.getBigrams(syllabusT)

syllabiClean = SyllabiTextProcessing.textCleanUp(syllabusT)
verb, noun = SyllabiTextProcessing.getVerbNounLemma(syllabiClean)
verbNoun = SyllabiTextProcessing.getVerbNounPair(syllabiClean)
classifiedVerbs, notInBlooms = SyllabiTextProcessing.classifyToBloomsLevel(set(verb))

#Get BOK Verbs
syllabusT_BOK = SyllabiTextProcessing.getTextFromSyllabi([SYLLABI_ROOT_LOC +'\\BOK'])
syllabiClean_BOK = SyllabiTextProcessing.textCleanUp(syllabusT_BOK)
verb_BOK, noun_BOK = SyllabiTextProcessing.getVerbNounLemma(syllabiClean_BOK)
verb_new_BOK = SyllabiTextProcessing.getVerbs_Nouns(syllabusT_BOK)
col_bigrams = SyllabiTextProcessing.getBigrams(syllabusT)
col_nouns = col_bigrams.values()
col_verbs = col_bigrams.keys()
col_noun_list = []
for n in col_nouns: col_noun_list.extend(n)
print("Col nouns----------------------------", col_noun_list)
col_levels_verbs, n = SyllabiTextProcessing.classifyToBloomsLevel(set(col_verbs))
col_level_nouns = []
for i in range(len(col_levels_verbs)):
    l = []
    for k in col_levels_verbs[i]:
        val = col_bigrams[k]
        l.extend(val)
    col_level_nouns.append(l)

tier_files = ["C:/Pallavi/NSF_AM_Pathways/BOK_Noun_Tiers/BOK_Tier1.txt", "C:/Pallavi/NSF_AM_Pathways/BOK_Noun_Tiers/BOK_Tier_2.txt",
                "C:/Pallavi/NSF_AM_Pathways/BOK_Noun_Tiers/BOK_Tier_3.txt", "C:/Pallavi/NSF_AM_Pathways/BOK_Noun_Tiers/BOK_Tier_4a.txt",
                    "C:/Pallavi/NSF_AM_Pathways/BOK_Noun_Tiers/BOK_Tier_4b.txt"]
bok_tier_nouns = []
for file in tier_files:
    f = open(file)
    tier = f.read().lower()
    bok_bigrams = SyllabiTextProcessing.getBigrams(tier)
    bok_nouns = bok_bigrams.values()
    bok_verbs = bok_bigrams.keys()
    bok_noun_list = []
    for l in bok_nouns: bok_noun_list.extend(l)
    bok_levels_verbs, n1 = SyllabiTextProcessing.classifyToBloomsLevel(set(bok_verbs))
    bok_level_nouns = []
    for i in range(len(bok_levels_verbs)):
        l = []
        for k in bok_levels_verbs[i]:
            if k != "":
                val = bok_bigrams[k]
                l.extend(val)
        bok_level_nouns.append(l)
    bok_tier_nouns.append(bok_level_nouns)

noun_lvl = SentenceEncoder.sent_similarity(col_level_nouns, bok_tier_nouns)

# Classify nouns
Reports.plotPieChart_new(noun_lvl)


# Plot reports
#Reports.getReport(verb, verb_BOK, REPORT_TYPE)
Reports.getReport(col_levels_verbs, verb_new_BOK, REPORT_TYPE)


################################################################# Word Sense Disambiguation #########################################
'''
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec

# Sent tokenize
sent_tokens = []
for s in sent_tokenize(syllabiClean):
    mTemp = []
    for w in word_tokenize(s):
        mTemp.append(w)
    sent_tokens.append(mTemp)

# CBOW model
model_CBOW = Word2Vec(sent_tokens, min_count=1, size=100, window=5)
print("Cosine similarity between 'CAD' " +"and 'drawings' - CBOW : ", model_CBOW.similarity('computer','drawings'))
# Skip Gram model
model_SkipGram = Word2Vec(sent_tokens, min_count = 1, size = 100, window = 5, sg = 1)
print("Cosine similarity between 'CAD' " +"and 'drawings' - Skip Gram : ", model_SkipGram.similarity('computer','drawings'))
my_dict = dict({})
for idx, key in enumerate(model_SkipGram.wv.vocab):
    my_dict[key] = model_SkipGram.wv.get_vector(key)
print(my_dict.keys())
print(my_dict.values())
    '''







