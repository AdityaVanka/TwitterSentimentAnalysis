#Uncomment below import for performing Necessary library Installations
#import library_installations

from flask import Flask, render_template, request, jsonify
import custom_functions as cf
import plotly.express as px
import datetime as dt
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)


import tweepy as tp

auth = tp.OAuthHandler('KoQK70f0XCqCiD1pp9YRDSh2J', 'hbduYYuKXpLo0NCDHcxmV72dIGEKY6mXZLCBXxhcafYjevzIOP')
auth.set_access_token('1483783708817645572-fioHIyRWMObaHT9td6IhkMB9FJqpa7',
                      't4nGcyJFlWKSyCEo02CE3EAWGpCeWKjE0tARutMf2QKg4')

api = tp.API(auth)

file_name = 'tweets.tsv'

master_Data=None

@app.route('/', methods=['GET', 'POST'])
def home_page():  # put application's code here
    if request.method == "POST":
        query = request.form['query']
        print(query)
        query = query + " lang:en"
        tweets = api.search_tweets(q=query, lang='en', count=50)
        cf.write_to_file(api, tweets, file_name)
        data = cf.load_dataFrame(file_name)
        global master_Data
        if master_Data is None:
            master_Data=data
        bar_fig_json=bar_chart_plot(master_Data.copy())
        pie_fig=get_PieChat(master_Data.copy())
        word_fig=get_wordCloud_data()
        bubble_fig=get_bubbleChart(master_Data.copy())
        geo_fig=get_geoChart(master_Data.copy())
        return render_template('analysis.html', load_data=data, barPlot=bar_fig_json, piePlot=pie_fig, bubblePlot=bubble_fig, wordPlot=word_fig, geoPlot=geo_fig)
    else:
        return render_template("index.html")


@app.route('/tweets')
def tweets_page():  # put application's code here
    return 'Tweets here'


@app.route('/tweets/analysis')
def analysisPage():  # put application's code here
    return 'Analysis here'


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)


@app.route('/get_linechart_data')
def get_linechart_data():
    return jsonify({"Response": True})




@app.route("/bar_chart_plotly")
def bar_chart_plot(data):
    df = data[['sentiment','User_followers_count']]
    df= df.groupby('sentiment', as_index =False).count()
    trace1 = go.Bar(x=df['sentiment'], y=df['User_followers_count'])
    layout = go.Layout(title="Followers count", xaxis=dict(title="Polarity"),
                       yaxis=dict(title="Number of followers"))
#   print(layout)
    data = [trace1]
    fig = go.Figure(data=data, layout=layout)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # fig.write_image("static/images/barChart.svg")
    return fig_json


def get_PieChat(data):
    df = data[['sentiment', 'User_followers_count']]
    df = df.groupby('sentiment', as_index=False).count()
    fig = go.Figure(data=[go.Pie(labels=df['sentiment'], values=df['User_followers_count'], hole=.3)])
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

@app.route('/get_wordCloud_data', methods=['GET', 'POST'])
def get_wordCloud_data():
    data=master_Data.copy()
    df = data['clean_tweet']
    words=""
    for i in df:
        words+=i
    return jsonify(words_gen(words))

def words_gen(sentence):
    words={}
    for i in sentence.split(" "):
        #print(i)
        if i in words.keys():
            words[i]+=1
        else:
            words[i]=1
    final_list=[]
    for i in words:
        dat={}
        dat['word'] = i
        dat['size'] = words[i]*50
        final_list.append(dat)
    return(final_list)


@app.route("/sun_chart_plotly")
def get_bubbleChart(data):
    df = px.data.tips()
    data['date'] = data['created_at'].apply(lambda x: dt.datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y').strftime('%d/%m/%Y'))
    df = data[['date', 'sentiment','User_followers_count']]
    df = df.groupby(['date','sentiment'], as_index=False).count()
    fig = px.scatter(df, x="date", y="User_followers_count",
                     size="User_followers_count", color="sentiment",
                    hover_name="sentiment", log_x=True, size_max=60)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json


def get_geoChart(input_data):
    tmp = input_data.groupby(["state","state_name"], as_index=False).count()
    data = dict(type='choropleth',
                locations=tmp['state'],
                locationmode='USA-states', z=tmp['id'],
                text=tmp['state_name'], colorbar={'title': 'Activity'},
                colorscale=[[0, 'rgb(224,255,255)'],
                            [0.01, 'rgb(166,206,227)'], [0.02, 'rgb(31,120,180)'],
                            [0.03, 'rgb(178,223,138)'], [0.05, 'rgb(51,160,44)'],
                            [0.10, 'rgb(251,154,153)'], [0.20, 'rgb(255,255,0)'],
                            [1, 'rgb(227,26,28)']],
                reversescale=False)
    layout = dict(title='Activity at state level',
                  geo=dict(scope='usa',showframe=True, projection={'type': 'albers usa'}))
    choromap = go.Figure(data=[data], layout=layout)
    fig_json = json.dumps(choromap, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json
