import configparser
import os
from datetime import datetime

INI_FILE_LOC = "C:\\Pallavi\\NSF_AM_Pathways\\AnalysisFramework\\framework.ini"
SYLLABI_ROOT_LOC = ""
SYLLABI_LOC = []
RESULTS_LOC = ""
COLLEGE_NAME = ""
COURSE_TYPE = ""
REPORT_TYPE = ""
CURRENT_DATE_TIME = datetime.now().strftime("%m_%d_%Y_%H%M%S")
RESULT_CUR_DIR = RESULTS_LOC + "\\Results_" + CURRENT_DATE_TIME


def getINIVariables():
    return RESULTS_LOC, RESULT_CUR_DIR, COLLEGE_NAME, SYLLABI_ROOT_LOC, SYLLABI_LOC, REPORT_TYPE, COURSE_TYPE


# Read from ini
iniParser = configparser.ConfigParser()
iniParser.read(INI_FILE_LOC)
if (iniParser['Location'] != None):
    if (iniParser['Location']['Syllabi'] != None):
        SYLLABI_ROOT_LOC = iniParser['Location']['Syllabi']
    if (iniParser['Location']['Results'] != None):
        RESULTS_LOC = iniParser['Location']['Results']
if (iniParser['Combinations'] != None):
    if (iniParser['Combinations']['College'] != None):
        COLLEGE_NAME = iniParser['Combinations']['College']
    if (iniParser['Combinations']['CourseType'] != None):
        COURSE_TYPE = iniParser['Combinations']['CourseType']
    if (iniParser['Combinations']['ReportType'] != None):
        REPORT_TYPE = iniParser['Combinations']['ReportType']

# Build input locations based on choices from ini
if (COLLEGE_NAME == "All" and COURSE_TYPE == 'All'):
    SYLLABI_LOC.append(SYLLABI_ROOT_LOC + '\\Colleges')
elif (COLLEGE_NAME == "All"):
    dirName = [f.path for f in os.scandir(SYLLABI_ROOT_LOC + '\\Colleges') if f.is_dir()]
    for d in dirName:
        if ('+' in COURSE_TYPE):
            cType = COURSE_TYPE.split('+')
            noSpace = lambda x: x.strip()
            for i in range(len(cType)):
                cType[i] = noSpace(cType[i])
                SYLLABI_LOC.append(d + "\\" + cType[i])
        else:
            SYLLABI_LOC.append(d + "\\" + COURSE_TYPE.strip())

elif (COLLEGE_NAME == "Framework" or COLLEGE_NAME == "BOK"):
    SYLLABI_LOC.append(SYLLABI_ROOT_LOC + "\\" + COLLEGE_NAME)
else:
    if (COURSE_TYPE != None):
        if ('+' in COURSE_TYPE):
            cType = COURSE_TYPE.split('+')
            noSpace = lambda x: x.strip()
            for i in range(len(cType)):
                cType[i] = noSpace(cType[i])
                SYLLABI_LOC.append(SYLLABI_ROOT_LOC + "\\Colleges\\" + COLLEGE_NAME + "\\" + cType[i])
        elif (COURSE_TYPE == "All"):
            SYLLABI_LOC.append(SYLLABI_ROOT_LOC + "\\Colleges\\" + COLLEGE_NAME)
        else:
            SYLLABI_LOC.append(SYLLABI_ROOT_LOC + "\\Colleges\\" + COLLEGE_NAME + "\\" + COURSE_TYPE.strip())
