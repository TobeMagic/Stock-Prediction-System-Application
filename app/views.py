from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scatter

import pandas as pd
import numpy as np
import json

import datetime as dt
import qrcode

from .models import Project

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm
from django.contrib.auth.decorators import login_required

# Create your views here.
def handler404(request, exception):
    return render(request, 'error/404.html', status=404)


def handler500(request):
    return render(request, 'error/500.html', status=500)

# The Home page when Server loads up
@login_required
def index(request):
    # ================================================= Left Card Plot =========================================================
    data = pd.read_csv("app/data/train_data.csv", )
    model_name = "股票数据"
    fig_left = go.Figure()
    fig_left.add_trace(
        go.Scatter(x=data['Time'], y=data['MidPrice'], name="订单铺交易卷")
    )
    # fig_left.add_trace(
    #     go.Scatter(x=data['Date'], y=data['MidPrice'], name="订单铺交易卷预测结果")
    # )
    fig_left.update_layout(paper_bgcolor="#eeeeee", plot_bgcolor="#eeeeee", font_color="black")

    plot_div_left = plot(fig_left, auto_open=False, output_type='div')

    # ================================================ To show recent stocks ==============================================
    df = pd.read_csv("app/data/train_data_show.csv")
    json_records = df.reset_index().to_json(orient='records')
    recent_stocks = json.loads(json_records)

    # ========================================== Page Render section =====================================================

    return render(request, 'index.html', {
        'plot_div_left': plot_div_left,
        'model_name': model_name,
        'recent_stocks': recent_stocks,
        'error': ""
    })


# The Predict Function to implement Machine Learning as well as Plotting
@login_required
def predict(request, model_name):
    ori = pd.read_csv("app/data/train_data.csv", )
    data = pd.read_csv("app/data/" + model_name + ".csv", )
    error = ""
    if "LSTM" in model_name:
        error = "评价指标：MSE：0.0050，MAE:0.0698"
    elif "Condition" in model_name:
        error = "评价指标：MSE：0.0002，MAE:0.0116"
    fig_left = go.Figure()
    fig_left.add_trace(
        go.Scatter(x=ori['Time'], y=ori['MidPrice'], name=model_name)
    )
    fig_left.add_trace(
        go.Scatter(x=data['Time'], y=data['MidPrice'], name=model_name + "预测结果")
    )
    fig_left.update_layout(paper_bgcolor="#eeeeee", plot_bgcolor="#eeeeee", font_color="black")

    plot_div_left = plot(fig_left, auto_open=False, output_type='div')
    json_records = data.reset_index().to_json(orient='records')
    recent_stocks = json.loads(json_records)

    return render(request, 'index.html', context={
        'plot_div_left': plot_div_left,
        'model_name': model_name,
        'recent_stocks': recent_stocks,
        'error': error
    })
