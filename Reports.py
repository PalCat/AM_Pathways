import matplotlib.pyplot as plt
from NSF_AM_Pathway import SyllabiTextProcessing
from NSF_AM_Pathway import ReadIni
import numpy as np
import nltk
from collections import OrderedDict
import plotly.graph_objects as go
import pylab as plb


RESULT_DIR, RESULT_CUR_DIR, COLLEGE, ROOT_DIR, SYLLABI_LOC, REPORT_TYPE, COURSE_TYPE = ReadIni.getINIVariables()
BOK_DIR = [ROOT_DIR +'\\BOK']

def getReport(verb, verb_bok, reportType):
    if (reportType == "Line"):
        plotLineGraph(verb)
    elif reportType == "Pie":
        plotPieChart(verb)
    elif reportType == "Radar":
        plotRadarChart_verbs(verb)
    elif reportType == "Bar":
        plotBarGraph(verb)
    elif reportType == "StackedBar":
        plotStackedBar(verb, verb_bok)
    elif reportType == "All":
        plotLineGraph(verb)
        plotPieChart(verb)
        plotRadarChart_verbs(verb)
        plotBarGraph(verb)
        plotStackedBar(verb, verb_bok)

def sort_dict(s_dict):
    dd = OrderedDict(sorted(s_dict.items(), key=lambda x: x[1], reverse=True))
    return dd

def getPercentageOfBloomVerbs(verbList):
    #mFreq = [[], [], [], [], [], [],[]]
    mFreq = []
    #level = [{}, {}, {}, {}, {}, {},{}]
    level =[]
    #mClass = [[], [], [], [], [], [], []]
    mClass = []
    #mVCount = [[], [], [], [], [], [], []]
    mVCount = []

    f_verbList = nltk.FreqDist(verbList)
    sort_L1_dict = OrderedDict(sorted(nltk.FreqDist(f_verbList).items(), key=lambda x: x[1], reverse=True))
    classVerbList, n1 = SyllabiTextProcessing.classifyToBloomsLevel(set(verbList))
    for i in range(len(classVerbList)):
        mTemp = {}
        freq_temp = []
        level_temp = []
        class_temp = []
        vcount_temp = []
        for v in classVerbList[i]:
            freq = sort_L1_dict[v]
            #mFreq[i] = (freq)
            freq_temp.append(freq)
            mTemp[v] = freq

        mFreq.append(freq_temp)
        #level[i] = OrderedDict(sorted(nltk.FreqDist(mTemp).items(), key=lambda x: x[1], reverse=True))
        sorted_order_level = OrderedDict(sorted(nltk.FreqDist(mTemp).items(), key=lambda x: x[1], reverse=True))
        level_temp.append(sorted_order_level)
        level.append(level_temp)
        #mClass[i] = list(level[i].keys())
        #class_temp.append(list(level[i][0].keys()))
        class_temp.append(list(level[i][0].keys()))
        mClass.append(class_temp[0])
        #mVCount[i] = list(level[i].values())
        #vcount_temp.append(list(level[i][0].values()))
        vcount_temp.append(list(level[i][0].values()))
        mVCount.append(vcount_temp[0])
    #Calculate Percentage of verbs in each Bloom's Level
    length = [sum(mVCount[0]), sum(mVCount[1]), sum(mVCount[2]), sum(mVCount[3]), sum(mVCount[4]), sum(mVCount[5])]
    totalVerbs = sum(length)
    #percentageVerbLevels = [0, 0, 0, 0, 0, 0]
    percentageVerbLevels = []
    for index, c in enumerate(length):
        if(c != 0):
            #percentageVerbLevels[index] = (c / totalVerbs) * 100
            percentageVerbLevels.append(round(((c / totalVerbs) * 100), 2))
        else:
            percentageVerbLevels[index] = 0

    return mClass, mVCount, percentageVerbLevels

def plotPieChart(verbList):
    c, f, sizes = getPercentageOfBloomVerbs(verbList)
    mLabels = 'Remembering', 'Understanding', 'Applying', 'Analyzing', 'Evaluating', 'Creating'
    # Plot
    patches, text = plt.pie(sizes, labels=mLabels)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(mLabels, sizes)]
    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, sizes), key=lambda x: x[2], reverse=True))
    plt.legend(patches, labels, loc='upper right', bbox_to_anchor=(-0.1, 1.), fontsize=12)
    plt.savefig(RESULT_DIR+RESULT_CUR_DIR+'\\piechart_' + COLLEGE + "_"+ COURSE_TYPE +'.png',bbox_inches='tight')
    plt.axis('equal')
    plt.show()

def plotPieChart_new(noun_level):
    #c, f, sizes = getPercentageOfBloomVerbs(verbList)
    mLabels = 'Tier1', 'Tier2', 'Tier3'
    # Plot
    length = [len(noun_level[5][0]), len(noun_level[5][1]), len(noun_level[5][2])]
    totalnouns = sum(length)
    sizes = []
    for index, c in enumerate(length):
        if(c != 0):
            #percentageVerbLevels[index] = (c / totalVerbs) * 100
            sizes.append(round(((c / totalnouns) * 100), 2))
        else:
            sizes[index] = 0

    patches, text = plt.pie(sizes, labels=mLabels)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(mLabels, sizes)]
    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, sizes), key=lambda x: x[2], reverse=True))
    plt.legend(patches, labels, loc='upper right', bbox_to_anchor=(-0.1, 1.), fontsize=12)
    plt.savefig(RESULT_DIR+RESULT_CUR_DIR+'\\piechart_' + COLLEGE + "_"+ COURSE_TYPE +'.png',bbox_inches='tight')
    plt.axis('equal')
    plt.title("Chipola CNT - Creating")
    plt.show()

def plotLineGraph(verbList):
    verb, freq, p = getPercentageOfBloomVerbs(verbList)
    fig, ax = plt.subplots()
    ax.plot(np.array(verb[0]), np.array(freq[0]), label='Remembering')
    ax.plot(np.array(verb[1]), np.array(freq[1]), label='Understanding')
    ax.plot(np.array(verb[2]), np.array(freq[2]), label='Applying')
    ax.plot(np.array(verb[3]), np.array(freq[3]), label='Analyzing')
    ax.plot(np.array(verb[4]), np.array(freq[4]), label='Evaluating')
    ax.plot(np.array(verb[5]), np.array(freq[5]), label='Creating')
    handles, labels = ax.get_legend_handles_labels()
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    plt.xlabel('Verbs')
    plt.ylabel('Frequency')
    plt.title("Variance of verbs in each level of Bloom's Taxonomy.")
    ax.legend(handles, labels)
    plt.savefig(RESULT_DIR+RESULT_CUR_DIR + '\\lineGraph_' + COLLEGE + "_"+ COURSE_TYPE +'.png',bbox_inches='tight')
    plt.show()

def plotRadarChart_verbs(verbList):
    # Set data
    BOK_T = SyllabiTextProcessing.getTextFromSyllabi(BOK_DIR)
    BOKClean = SyllabiTextProcessing.textCleanUp(BOK_T)
    mAllBOKVerbs, allNouns = SyllabiTextProcessing.getVerbNounLemma(BOKClean)
    c1, f1, percentageVBOK = getPercentageOfBloomVerbs(mAllBOKVerbs)
    c2, f2, percentageVCollege = getPercentageOfBloomVerbs(verbList)
    percentageVBOK = [round(x) for x in percentageVBOK]
    percentageVCollege = [round(y) for y in percentageVCollege]
    mColleges = ['AM Competency Model', COLLEGE]
    val1 = np.array(percentageVBOK)
    val2 = np.array(percentageVCollege)
    mMaxVal = 0
    if (np.max(val1) > np.max(val2)):
        mMaxVal = np.max(val1)
    else:
        mMaxVal = np.max(val2)
    # number of variable
    mCat = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating"]
    categories = np.array(mCat)
    N = categories.size
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

    angles = np.concatenate((angles, [angles[0]]))
    val1 = np.concatenate((val1, [val1[0]]))
    val2 = np.concatenate((val2, [val2[0]]))
    # Initialise the spider plot

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # first axis on top:
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    # One axe per variable + labels
    ax.set_xticks(angles)
    ax.set_xticklabels(categories)
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    # ylabels
    ax.set_rlabel_position(135)
    plt.yticks([10, 20, 30, 40, 50, mMaxVal], ["10", "20", "30", "40", "50", str(mMaxVal)], color="grey", size=7)
    plt.ylim(0, mMaxVal)
    #Ind1
    ax.plot(angles, val2, linewidth=1, linestyle='solid', label=mColleges[1])
    ax.fill(angles, val2, 'b', alpha=0.1)
    # Ind2
    ax.plot(angles, val1, linewidth=1, linestyle='solid', label=mColleges[0])
    ax.fill(angles, val1, 'r', alpha=0.1)
    ax.grid(True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
    plt.savefig(RESULT_DIR+RESULT_CUR_DIR+ '\\radarchart_' + COLLEGE +"_"+ COURSE_TYPE + '.png', bbox_inches='tight')
    plt.show()

def plotBarGraph(verbList):
    f_verb = nltk.FreqDist(verbList)
    top_20 = f_verb.most_common(20)
    mVerbs = [x[0] for x in top_20]
    mFreq = [y[1] for y in top_20]
    fig, ax = plt.subplots()
    ax.bar(mVerbs, mFreq)
    plt.xticks(mVerbs, fontsize=12, rotation=90)
    plt.ylabel("Freq", fontsize=12)
    plt.savefig(RESULT_DIR + RESULT_CUR_DIR + '\\barGraph_' + COLLEGE +"_"+ COURSE_TYPE +'.png', bbox_inches='tight')
    plt.show()


def plotStackedBar(verbList_col, verbList_bok):
    series_labels = [COLLEGE, 'AM Competency Model']
    c, f, sizes_COL = getPercentageOfBloomVerbs(verbList_col)
    c1, f1, sizes_BOK = getPercentageOfBloomVerbs(verbList_bok)
    category_labels = ['Remembering', 'Understanding', 'Applying', 'Analyzing', 'Evaluating', 'Creating']
    percentage = [np.array(sizes_COL), np.array(sizes_BOK)]

    fig = go.Figure(data=[go.Bar(name=category_labels[0], x=series_labels, y=[percentage[0][0],percentage[1][0]],
                                 width=[0.3, 0.3], text = [str(percentage[0][0])+"%",str(percentage[1][0])+"%"],textposition='inside', hoverinfo = 'text'),
                          go.Bar(name=category_labels[1], x=series_labels, y=[percentage[0][1], percentage[1][1]],
                                 width=[0.3, 0.3], text = [str(percentage[0][1])+"%",str(percentage[1][1])+"%"],textposition='inside'),
                          go.Bar(name=category_labels[2], x=series_labels, y=[percentage[0][2], percentage[1][2]],
                                 width=[0.3, 0.3], text = [str(percentage[0][2])+"%",str(percentage[1][2])+"%"],textposition='inside'),
                          go.Bar(name=category_labels[3], x=series_labels, y=[percentage[0][3],percentage[1][3]],
                                 width=[0.3, 0.3], text = [str(percentage[0][3])+"%",str(percentage[1][3])+"%"],textposition='inside'),
                          go.Bar(name=category_labels[4], x=series_labels, y=[percentage[0][4], percentage[1][4]],
                                 width=[0.3, 0.3], text = [str(percentage[0][4])+"%",str(percentage[1][4])+"%"],textposition='inside'),
                          go.Bar(name=category_labels[5], x=series_labels, y=[percentage[0][5], percentage[1][5]],
                                 width=[0.3, 0.3], text = [str(percentage[0][5])+"%",str(percentage[1][5])+"%"],textposition='inside')])
    # Change the bar mode
    fig.update_layout(barmode='stack')
    #fig.savefig(RESULT_DIR + RESULT_CUR_DIR + '\\barGraph_' + COLLEGE + "_" + COURSE_TYPE + '.png', bbox_inches='tight')
    fig.show()
