"""
Created on Wed Sep 18 22:45:30 2019

@author: sefa
"""
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# visualization tools
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
from wordcloud import WordCloud

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.
        
df=pd.read_csv("data.csv")
df.head()
#df.info()
df.drop(columns=['Unnamed: 0','Photo','Flag','Club Logo'],inplace=True)

f,ax = plt.subplots(figsize=(25, 15))
sns.heatmap(df.corr(), annot=True, linewidths=0.5,linecolor="red", fmt= '.1f',ax=ax)
plt.show()

nationalityDf = pd.DataFrame(columns = ['Nationality'])
nationalityDf["Nationality"]=[each for each in df.Nationality.unique()]
nationalityDf["maxOverall"]=[df.Overall[df.Nationality==each].max() for each in nationalityDf.Nationality]
nationalityDf["meanOverall"]=[df.Overall[df.Nationality==each].mean() for each in nationalityDf.Nationality]
nationalityDf["minOverall"]=[df.Overall[df.Nationality==each].min() for each in nationalityDf.Nationality]
nationalityDf.sort_values(by=['maxOverall','meanOverall','minOverall'],ascending=False)
nationalityDf=nationalityDf.head(25)
# visualization
f,ax = plt.subplots(figsize = (15,15))
sns.barplot(x=nationalityDf.maxOverall,y=nationalityDf.Nationality,color='green',alpha = 0.5,label='max Overall' )
sns.barplot(x=nationalityDf.meanOverall,y=nationalityDf.Nationality,color='blue',alpha = 0.7,label='mean Overall')
sns.barplot(x=nationalityDf.minOverall,y=nationalityDf.Nationality,color='cyan',alpha = 0.6,label='min Overall')

ax.legend(loc='lower right',frameon = True)
ax.set(xlabel='Value', ylabel='Nationality',title = "Nationality Player Max - Mean - Min Value")
[Text(0, 0.5, 'Nationality'),
 Text(0.5, 0, 'Value'),
 Text(0.5, 1.0, 'Nationality Player Max - Mean - Min Value')]

ClubDf = pd.DataFrame(columns = ['Club'])
ClubDf["Club"]=[each for each in df.Club.unique()]
ClubDf["maxOverall"]=[df.Overall[df.Club==each].max() for each in ClubDf.Club]
ClubDf["meanOverall"]=[df.Overall[df.Club==each].mean() for each in ClubDf.Club]
ClubDf["minOverall"]=[df.Overall[df.Club==each].min() for each in ClubDf.Club]
ClubDf.sort_values(by=['maxOverall','meanOverall','minOverall'],ascending=False)
ClubDf=ClubDf.head(25)
# create trace1 
trace1 = go.Bar(
                x = ClubDf.Club,
                y = ClubDf.maxOverall,
                name = "Max Overall Value",
                marker = dict(color = 'rgba(55, 114, 55, 1)',
                             line=dict(color='rgb(0,0,0)',width=1.5)),
                text = ClubDf.Club)
# create trace2 
trace2 = go.Bar(
                x = ClubDf.Club,
                y = ClubDf.meanOverall,
                name = "Mean Overall Value",
                marker = dict(color = 'rgba(235, 155, 12, 1)',
                              line=dict(color='rgb(0,0,0)',width=1.5)),
                text = ClubDf.Club)
# create trace3 
trace3 = go.Bar(
                x = ClubDf.Club,
                y = ClubDf.minOverall,
                name = "Min Overall Value",
                marker = dict(color = 'rgba(235, 155, 162, 1)',
                              line=dict(color='rgb(0,0,0)',width=1.5)),
                text = ClubDf.Club)
data = [trace1, trace2, trace3]
layout = go.Layout(barmode = "group")
fig = go.Figure(data = data, layout = layout)
iplot(fig)

#Nationality Text Size = Nationality Player Count

plt.subplots(figsize=(15,15))
wordcloud = WordCloud(
                          background_color='white',
                          width=1920,
                          height=1080
                         ).generate(" ".join(df.Nationality))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('graph.png')

plt.show()

#Effect of preferred foot on position
LeftLabels = df[df["Preferred Foot"]=="Left"].Position.value_counts().head(10).index
LeftValues = df[df["Preferred Foot"]=="Left"].Position.value_counts().head(10).values
RightLabels = df[df["Preferred Foot"]=="Right"].Position.value_counts().head(10).index
RightValues = df[df["Preferred Foot"]=="Right"].Position.value_counts().head(10).values

from plotly.subplots import make_subplots

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=LeftLabels, values=LeftValues, name="Left Foot Preferred"),
              1, 1)
fig.add_trace(go.Pie(labels=RightLabels, values=RightValues, name="Right Foot Preferred"),
              1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='LEFT', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='RİGHT', x=0.82, y=0.5, font_size=20, showarrow=False)])
fig.show()

#Plotly - Box Plots ( interactive )
#Barcelona vs Real Madrid (min,q1,median,q3,max value)
team1 = df[df.Club=="FC Barcelona"].Overall
team2 = df[df.Club=="Real Madrid"].Overall

fig = go.Figure()
# Use x instead of y argument for horizontal plot
fig.add_trace(go.Box(x=team1, name='FC Barcelona'))
fig.add_trace(go.Box(x=team2, name='Real Madrid'))

fig.show()