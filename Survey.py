from logging import RootLogger

import pandas as pd
import numpy as np


def extractDataFromExcel():

    survey_dict = dict()
    df_2015 = pd.read_excel("C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\13-14 Alumni Responses for 2016 report 6.29.xls").fillna("missing")
    #df_13_14 = df_13_14_temp[1:]
    df_2016 = pd.read_excel("C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\14-15 CH Responses as of 6.29.16.xls").fillna("missing")
    df_15_16 = pd.read_excel("C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\FITC Alumni Survey 2017 (15-16)_June 28, 2017_10.29 Used for Report July 2107.xls")
    df_16_17 = pd.read_csv("C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\7.10.18 AS CH16-17 FINAL DOWNLOAD.csv")
    #print(df_13_14.head)
    print(len(df_2015.index))
    row_66 = df_2015.iloc[66]['Name'].split(",") #+ " " + df_13_14.iloc[66]['Last Name']
    print(row_66)
    for i in range(len(df_2015.index)):
        row = []
        student_name = ""
        fN = df_2015.iloc[i]['First Name']
        lN = df_2015.iloc[i]['Last Name']
        #print("at the row: ", i, " FN: ", fN, " LN: ", lN)
        if fN != "missing" and lN != "missing":
            student_name = df_2015.iloc[i]['First Name'] + " " + df_2015.iloc[i]['Last Name']
        else:
            name = df_2015.iloc[i]['Name'].split(",")
            if len(name) == 2:
                student_name = name[1].strip() + " " + name[0].strip()
        row.append(df_2015.iloc[i].tolist())
        if student_name in survey_dict.keys():
            survey_dict.get(student_name).append(row)
        else:
            survey_dict[student_name] = row

#    survey = pd.DataFrame.from_dict(survey_dict)
   # print(survey.head())
    #survey.to_csv("C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\13_14_2016_report_6.29.xls")
    for x, y in survey_dict.items():
        if len(y) > 1:
            print("Student Name: ", x, "Row: ", len(y), y)
# 2016 Survey
    for j in range(len(df_2016.index)):
        row = []
        student_name = ""
        fN = df_2016.iloc[j]['First Name']
        lN = df_2016.iloc[j]['Last Name']
        if fN != "missing" and lN != "missing":
            student_name = df_2016.iloc[j]['First Name'] + " " + df_2016.iloc[j]['Last Name']
        else:
            name = df_2016.iloc[j]['Name'].split(",")
            if len(name) == 2:
                student_name = name[0].strip() + " " + name[1].strip()
        row.append(df_2016.iloc[j].tolist())
        if student_name in survey_dict.keys():
            survey_dict.get(student_name).append(row)
        else:
            survey_dict[student_name] = row
    for q, r in survey_dict.items():
        if len(r) > 1:
            print("Student Name: ", q, "Row: ", len(r), r)
    print("Done")

ROOT_DIR = "C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\Updated_Columns\\"

def extractDataFromExcel_combined():
    survey_dict = dict()
    df_2015 = pd.read_excel(ROOT_DIR + "2015.xls").fillna("missing")
    df_2016 = pd.read_excel(ROOT_DIR + "2016.xlsx").fillna("missing")
    df_2017 = pd.read_csv(ROOT_DIR + "2017.csv").fillna("missing")
    df_2018 = pd.read_excel(ROOT_DIR + "2018.xlsx").fillna("missing")

    list_df = [df_2015, df_2016, df_2017, df_2018]
    frames = []

    for index, df in enumerate(list_df):
        student_name_col = []
        for i in range(len(df.index)):
            row = []
            student_name = ""
            fN = df.iloc[i]['First Name']
            lN = df.iloc[i]['Last Name']
            if fN != "missing" and lN != "missing":
                student_name = df.iloc[i]['First Name'] + " " + df.iloc[i]['Last Name']
            else:
                if index != 3:
                    if "," in df.iloc[i]['Name']:
                        name = df.iloc[i]['Name'].split(",")
                        if len(name) == 2:
                            if index == 0:
                                student_name = name[1].strip() + " " + name[0].strip()
                            else:
                                student_name = name[0].strip() + " " + name[1].strip()
                    else:
                        student_name = df.iloc[i]['Name']
                else:
                    student_name = df.iloc[i]['FN'] + " " + df.iloc[i]['LN']
            student_name_col.append(student_name)
            df_del_dup = df.loc[df[df['Student Name'] == student_name]]
            if len(df_del_dup.index) > 1:
                np_year = df['Year'].to_numpy()
                if((np_year[0] == np_year[1:]).all()):
                    indx = df.loc[df['EndDate'].idxmax()]
                    row.append(df.iloc[indx].tolist())
        df['Student Name'] = student_name_col
        #print(df.head)
        frames.append(df)

    result = pd.concat(frames)

    result.to_csv(ROOT_DIR+"Result.csv")
    #grouped = result.groupby('Student Name')
    #grouped.get_group('Katrina Fishman').to_csv(ROOT_DIR+"Result.csv")
    #print(grouped.first())
    #first = grouped.first()

    for key, group_df in result.groupby('Student Name'):
        survey_dict[key] = group_df

    survey = pd.DataFrame.from_dict(survey_dict, orient='index')
    #print(survey.head())
    survey.to_csv(ROOT_DIR + "Result.xls")

    # r1.reset_index().to_csv(ROOT_DIR+"Result.csv")

    for q, r in survey_dict.items():
        if len(r) > 1:
            print("Student Name: ", q, "Row: ", len(r), r)
    print("Done")


def extractDataFromExcel_dict():
    survey_dict = dict()
    student_record = dict()
    only_survey = []
    df_2015 = pd.read_excel(ROOT_DIR + "2015.xls").fillna("missing")
    df_2016 = pd.read_excel(ROOT_DIR + "2016.xlsx").fillna("missing")
    df_2017 = pd.read_csv(ROOT_DIR + "2017.csv").fillna("missing")
    df_2018 = pd.read_excel(ROOT_DIR + "2018.xlsx").fillna("missing")
    df_1 = pd.read_csv(ROOT_DIR + "Matching_Student_Records.csv", encoding = "Latin-1").fillna("missing")
    df_2 = pd.read_excel(ROOT_DIR + "Matching_Student_Records_2.xlsx", encoding = "Latin-1").fillna("missing")
    df_student_rec = df_1.append(df_2)
    df_survey_cols = pd.read_excel("C:\\Pallavi\\NSF_AM_Pathways\\AlumniSurvey\\" + "SurveyColumns.xlsx")

    for x in range(len(df_student_rec.index)):
        sname = ""
        fN = df_student_rec.iloc[x]['Student First Name']
        lN = df_student_rec.iloc[x]['Student Last Name']
        if fN != "missing" and lN != "missing":
            # student_name = df.iloc[i]['First Name'] + " " + df.iloc[i]['Last Name']
            sname = (fN.strip() + " " + lN.strip()).lower()
        else:
            print("First last name missing! in df_student_rec")
        temp_list = df_student_rec.iloc[x].tolist()
        student_record[sname] = temp_list

    index_year = df_2015.columns.get_loc("Year")
    index_endDate = df_2015.columns.get_loc("EndDate")
    resultRowList = []
    col_headers = list(df_survey_cols.columns)
    #col_headers.append('Student Name')

    list_df = [df_2015, df_2016, df_2017, df_2018]
    frames = []

    for index, df in enumerate(list_df):
        print("Index ::::::::", index)
        student_name_col = []
        for i in range(len(df.index)):
            row = []
            student_name = ""
            fN = df.iloc[i]['First Name']
            lN = df.iloc[i]['Last Name']
            if fN != "missing" and lN != "missing":
                #student_name = df.iloc[i]['First Name'] + " " + df.iloc[i]['Last Name']
                student_name = (fN.strip() + " " + lN.strip()).lower()
            else:
                if index != 3:
                    if "," in df.iloc[i]['Name']:
                        name = df.iloc[i]['Name'].split(",")
                        if len(name) == 2:
                            if index == 0:
                                student_name = (name[1].strip() + " " + name[0].strip()).lower()
                            else:
                                student_name = (name[0].strip() + " " + name[1].strip()).lower()
                    else:
                        student_name = (df.iloc[i]['Name'].strip()).lower()
                else:
                    student_name = (df.iloc[i]['FN'].strip() + " " + df.iloc[i]['LN'].strip()).lower()
            temp_list = df.iloc[i].tolist()
            temp_list.append(student_name)
            row.append(temp_list)
            if student_name in student_record.keys():
                temp_val = student_record[student_name]
                row[0].extend(temp_val)
            else:
                only_survey.append(student_name)
            if student_name in survey_dict.keys():
                lst_indx = -1
                rec_prev = survey_dict.get(student_name)
                curr_date = df.iloc[i]['EndDate']
                curr_year = df.iloc[i]['Year']
                for x in range(len(rec_prev)):
                    if rec_prev[x][index_year] == curr_year:
                        lst_indx = x
                if lst_indx != -1:
                    prev_date = rec_prev[lst_indx][index_endDate]
                    if (prev_date == 'missing' and curr_date != 'missing') or (curr_date != 'missing' and prev_date != 'missing' and curr_date > prev_date):
                        value = survey_dict[student_name]
                        value[lst_indx] = row[0]
                        survey_dict[student_name] = value
                    '''
                    elif curr_date != 'missing' and prev_date != 'missing' and curr_date > prev_date:
                        value = survey_dict[student_name]
                        value[index] = row[0]
                        survey_dict[student_name] = value
                        '''
                else:
                    survey_dict[student_name].append(row[0])
            else:
                survey_dict[student_name] = row

            student_name_col.append(student_name)
            '''
            df_del_dup = df.loc[df[df['Student Name'] == student_name]]
            if len(df_del_dup.index) > 1:
                np_year = df['Year'].to_numpy()
                if((np_year[0] == np_year[1:]).all()):
                    indx = df.loc[df['EndDate'].idxmax()]
                    row.append(df.iloc[indx].tolist())
                '''
        out = map(lambda x: x.lower(), student_name_col)
        df['Student Name'] = list(out)
        #print(df.head)
        frames.append(df)

    result = pd.concat(frames)

    result.to_csv(ROOT_DIR+"Result.csv")
    #grouped = result.groupby('Student Name')
    #grouped.get_group('Katrina Fishman').to_csv(ROOT_DIR+"Result.csv")
    #print(grouped.first())
    #first = grouped.first()

    for r in survey_dict.values():
        resultRowList.extend(r)
    '''
    for key, group_df in result.groupby('Student Name'):
        survey_dict[key] = group_df
        '''
    #survey = pd.DataFrame.from_dict(survey_dict, orient='index')
    survey = pd.DataFrame(resultRowList, columns=col_headers)
    #print(survey.head())
    survey.to_csv(ROOT_DIR + "Result_dict.csv")

    print("Only Survey", only_survey)
    df_only = pd.DataFrame(only_survey)
    df_only.to_csv(ROOT_DIR+"Only.csv")
    # r1.reset_index().to_csv(ROOT_DIR+"Result.csv")


    for q, r in survey_dict.items():
        if len(r) > 1:
            print("Student Name: ", q, "Row: ", len(r), r)
    print("Done")

#extractDataFromExcel()
#extractDataFromExcel_combined()
extractDataFromExcel_dict()