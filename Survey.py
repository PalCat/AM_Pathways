from logging import RootLogger

import pandas as pd

ROOT_DIR = ""

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

                else:
                    survey_dict[student_name].append(row[0])
            else:
                survey_dict[student_name] = row

            student_name_col.append(student_name)
        out = map(lambda x: x.lower(), student_name_col)
        df['Student Name'] = list(out)
        #print(df.head)
        frames.append(df)

    result = pd.concat(frames)

    result.to_csv(ROOT_DIR+"Result.csv")

    for r in survey_dict.values():
        resultRowList.extend(r)
  
extractDataFromExcel_dict()