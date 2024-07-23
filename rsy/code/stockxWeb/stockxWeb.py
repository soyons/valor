import pandas as pd 
import DBServer
from loguru import logger
import argparse

from flask import request, url_for
from flask import Flask, render_template
from flask import redirect, send_file
from flask import jsonify

import pdb 
from datetime import datetime
from tools.export_file import export
import math 

from utils import get_detail_data, count_detail_data

app = Flask(__name__)
dbserver =  DBServer.dbServer()


@app.route('/')
def home():
    '''
    :return logo界面渲染
    '''
    return render_template('home.html')


@app.route('/download')
def download_file():
    df, df_express = export(dbserver.ori_data)
    with pd.ExcelWriter("stockx_data.xlsx") as writer:
        df_express.to_excel(writer, sheet_name="express data")
        df.to_excel(writer, sheet_name="total data")
    return send_file("./stockx_data.xlsx", as_attachment=True)

@app.route('/main')
def show_page():
    '''
    :return 主页面, 各SKU概况
    '''
    per_page = 20
    cur_data = dbserver.data
    logger.info("Total skus is {}".format(len(cur_data)))
    total_page = math.ceil(len(cur_data) / 20)
    page = request.args.get('page', default=1, type=int) # 使用查询参数获取页码，默认为1
    start = (page - 1) * per_page               # 计算索引的起始值
    end = start + per_page                      # 计算索引的结束值

    df_page = cur_data.iloc[start:end]             # 拆分数据
    # html_table = df_page.to_html(index=False)    # 转换为HTML表格
    return render_template('main.html', data=df_page, page=page, total_page=total_page)

@app.route('/search_SKU', methods=["GET"])
def search_sku():
    sku = request.args.get('sku')
    return redirect(url_for('shoe_page', sku=sku))

@app.route("/shoe")
def shoe_page():
    sku, shoename = "NULL", "NULL"
    sku = request.args.get("sku")
    shoename = request.args.get('shoename')
    sales_data, shoename, invalid = get_detail_data(dbserver, sku, shoename)
    if invalid:
        return render_template("shoe.html", sales_data=None, shoename=shoename, invalid=invalid, error=f"INVALID SKU:{sku}")
    else:
        count_data = count_detail_data(sales_data)
        return render_template("shoe.html", sales_data=count_data.to_dict('records'), shoename=shoename, invalid=invalid)

@app.route("/shoe_detail")
def detail_page():
    sku, shoename = "NULL", "NULL"
    sku = request.args.get("sku")
    shoename = request.args.get('shoename')
    sales_data, shoename, invalid = get_detail_data(dbserver, sku, shoename)
    if invalid:
        return render_template("shoeDetail.html", sales_data=None, shoename=shoename, invalid=invalid, error=f"INVALID SKU:{sku}")
    else:
        return render_template("shoeDetail.html", sales_data=sales_data.to_dict('records'), shoename=shoename, invalid=invalid)
    
@app.route('/shoefilterExpressData')
def filter_data():
    sku, shoename = "NULL", "NULL"
    sku = request.args.get("sku")
    shoename = request.args.get('shoename')
    sales_data, shoename, invalid = get_detail_data(dbserver, sku, shoename)
    filter_type = request.args.get('filter', None)  # 从请求参数中获取 'filter'
    if filter_type and filter_type != "ALL":
        filtered_data = sales_data[sales_data['orderType'] == filter_type]  # 根据条件过滤数据
        return [filtered_data.to_dict('records'), shoename]   # 以HTML形式返回数据
    return [sales_data.to_dict('records'), shoename]  # 如果未指定过滤条件，返回原始数据


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    args = parser.parse_args()
    
    app.run(host="0.0.0.0", debug=args.debug, port=32500)
