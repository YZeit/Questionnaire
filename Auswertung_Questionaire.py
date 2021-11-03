import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns


st.set_option('deprecation.showPyplotGlobalUse', False)



table = pd.read_excel('Auswertungsdatensatz mit bereinigten Rohdaten.xlsx', sheet_name='Analysedatensatz_aufbereitet', header=0, index_col=0, keep_default_na=False)
table = table.astype(str)
codebook = pd.read_excel('Auswertungsdatensatz mit bereinigten Rohdaten.xlsx', sheet_name='Codebook_aufbereitet', header=0, index_col=0)
filter=[]
st.sidebar.header('Please select filter')

categorical_questions = [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29,
                         30, 31, 32, 33, 34, 36, 38, 39]

open_questions = [1, 2, 3, 4, 24, 35, 37]

for i in range(40):
    if (i in categorical_questions):
        question_text = codebook[codebook['Fragennummer aus Qualtrix']==table.columns[i]]['Frage']
        question_text = question_text.iloc[0]
        st.sidebar.subheader(question_text)
        answers_text = codebook[codebook['Fragennummer aus Qualtrix']==table.columns[i]]
        potential_answers = answers_text.iloc[:,2:10]
        potential_answers = potential_answers.iloc[0]
        potential_answers = list(potential_answers)
        potential_answers = [x for x in potential_answers if str(x) != 'nan']
        filter.append(st.sidebar.multiselect(table.columns[i], potential_answers, default=potential_answers))
    else:
        filter.append(0)

#st.dataframe(table)
#st.dataframe(codebook)

# apply filters
for i in range(40):
    if (i in categorical_questions):
        question_text = codebook[codebook['Fragennummer aus Qualtrix']==table.columns[i]]['Frage']
        question_text = question_text.iloc[0]
        current_filter = filter[i]
        answers_text = codebook[codebook['Fragennummer aus Qualtrix']==table.columns[i]]
        potential_answers = answers_text.iloc[:,2:10]
        potential_answers = potential_answers.iloc[0]
        potential_answers = list(potential_answers)
        potential_answers = [x for x in potential_answers if str(x) != 'nan']
        index = []
        for j in current_filter:
            index.append(str(potential_answers.index(j)+1))
        table = table[table.iloc[:,i].isin(index)]
        #st.write(table)
        #st.write(len(table.iloc[:,0]))
    else:
        hallo = 2

#st.write(table)

selected_question = st.selectbox('Please select the question you want to analyze', table.columns)

#st.bar_chart(table[selected_question])
unique_values = table[selected_question].unique()
table_to_plot = table[selected_question].sort_values()

selected_question_text = codebook[codebook['Fragennummer aus Qualtrix']==selected_question]['Frage']


answers_text = codebook[codebook['Fragennummer aus Qualtrix']==selected_question]
answers_text = answers_text.iloc[:,2:10]

number_of_potential_answers = int(8-sum(answers_text.isnull().values.ravel()))






#plt.hist(table_to_plot, density=False, bins=number_of_potential_answers, rwidth=0.5, histtype='bar')
#plt.ylabel('Quantity')
#plt.xlabel(selected_question_text.iloc[0])
#plt.title(selected_question)
#plt.xticks([int(i) for i in range(number_of_potential_answers)])
#st.pyplot()

sns.histplot(table_to_plot)
plt.xlabel(selected_question_text.iloc[0])
plt.title(selected_question)
plt.xticks(rotation=90, fontsize=6)
st.pyplot()

st.warning('Irgendwas stimmt nicht mit den Analysedaten - z.B. bei Frage Q9_17 scheint es so als ob alles um eine Zahl verrutscht wäre'
           ' (von 0 bis 5 anstatt von 1 bis 6)')
