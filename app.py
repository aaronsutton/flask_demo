from flask import Flask, render_template, request, redirect
import simplejson as json
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN
import pandas as pd
import numpy as np
import requests
import itertools

app = Flask(__name__)
app.vars = {}
global p
colors = itertools.cycle(['r','b','g','c'])

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['tickerSymbol'] = request.form['tickerSymbol']
        address = 'https://www.quandl.com/api/v3/datasets/WIKI/' + app.vars['tickerSymbol'] + '.json'
        r = requests.get(address)
        j = json.loads(r.content)
        df = pd.DataFrame(j['dataset']['data'], columns=j['dataset']['column_names'])
        df.set_index('Date')
        #return 'The stock symbol is {}'.format(app.vars['tickerSymbol'])
	p = figure(title='Quandl Stock Info for {}'.format(app.vars['tickerSymbol']))
        for i in ['closingPrice', 'adjustedClosingPrice', 'openingPrice', 'adjustedOpeningPrice']:
            if request.form.get(i):
                app.vars['plot'] = request.form[i]
                p.line(np.array(df['Date'], dtype=np.datetime64),df[app.vars['plot']])
                #p.line([1,2,3,4],[5,6,7,8])
        script, div = components(p,CDN) 
        return render_template('plot.html',div=div,script=script)                                      

if __name__ == '__main__':
    app.run(port=33507)
    app.debug=True
