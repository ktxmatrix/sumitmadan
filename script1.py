# Importing the Flask object from the flask library
from flask import Flask, render_template

# Instantiating the Flask class using the app object
app=Flask(__name__)
# __name__ is a special variable you get for the name of the python script

@app.route('/')
def home(): # defines what our web home page will do
    return render_template("home.html")

@app.route('/about/')
def about(): # About the website
    return render_template("about.html")

@app.route('/projects/')
def projects(): # Shows off a list of projects - past and future
    return render_template("projects.html")

@app.route('/plot/')
def plot(): # Show a sample Bokeh chart plotted for a sample stock
    import pandas as pd

    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader as web

    from datetime import datetime
    from bokeh.models.annotations import Title
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    today = datetime.today().strftime("%m/%d/%Y")
    start = datetime(2015, 11, 1)
    end = datetime(2016, 3, 10)
    df = web.DataReader(name="GOOG", data_source="yahoo", start=start, end=end)
    df

    def inc_dec(c,o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c,o) for (c,o) in zip (df.Close, df.Open)]

    df["Middle"] = (df.Open + df.Close)/2
    df["Height"] = abs(df.Close-df.Open)

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
    p.grid.grid_line_alpha = 0.3

    t = Title()
    t.text = "CandleStick Chart"
    p.title = t
    hours_12 = 12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="Blue")

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
           hours_12, df.Height[df.Status=="Increase"], fill_color='#98FB98', line_color='black')

    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
           hours_12, df.Height[df.Status=="Decrease"], fill_color='#F08080', line_color='black')

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js)


# When you execite the script, python assigns the name __main__
if __name__ == "__main__":
    app.run(debug=True) # Would not be executed if the script was imported from somewhere else
