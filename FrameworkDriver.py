from NSF_AM_Pathway import ReadIni
from NSF_AM_Pathway import SyllabiTextProcessing
from NSF_AM_Pathway import SentenceEncoder
from NSF_AM_Pathway import Reports

RESULTS_LOC, RESULT_CUR_DIR, COLLEGE_NAME, SYLLABI_ROOT_LOC, SYLLABI_LOC, REPORT_TYPE, COURSE_TYPE = ReadIni.getINIVariables()
print(ReadIni.getINIVariables())
#Text Processing
syllabusT = SyllabiTextProcessing.getTextFromSyllabi(SYLLABI_LOC)
syllabiClean = SyllabiTextProcessing.textCleanUp(syllabusT)
verb, noun = SyllabiTextProcessing.getVerbNounLemma(syllabiClean)
verbNoun = SyllabiTextProcessing.getVerbNounPair(syllabiClean)
classifiedVerbs, notInBlooms = SyllabiTextProcessing.classifyToBloomsLevel(set(verb))

#Get BOK Verbs
syllabusT_BOK = SyllabiTextProcessing.getTextFromSyllabi([SYLLABI_ROOT_LOC +'\\BOK'])
syllabiClean_BOK = SyllabiTextProcessing.textCleanUp(syllabusT_BOK)
verb_BOK, noun_BOK = SyllabiTextProcessing.getVerbNounLemma(syllabiClean_BOK)
# Plot reports
Reports.getReport(verb, verb_BOK, REPORT_TYPE)

