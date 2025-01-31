# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
import talib
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.io import output_file

# 讀取股市數據 (確保包含 Date, Open, High, Low, Close, Volume)
df = pd.read_csv(r'D:\python\data\tw_future\future_data_all_1D.csv')
df['Date'] = df['ts'].copy()

# 計算技術指標
df["MA_10"] = talib.SMA(df["Close"], timeperiod=10)
df["MA_50"] = talib.SMA(df["Close"], timeperiod=50)

df["K"], df["D"] = talib.STOCH(df["High"], df["Low"], df["Close"])
df["J"] = 3 * df["K"] - 2 * df["D"]

df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = talib.MACD(df["Close"])
df["RSI"] = talib.RSI(df["Close"], timeperiod=14)

# 設定 Bokeh 輸出
output_file("stock_analysis.html")

# ========== K 線圖 ==========
p_kline = figure(x_axis_type="datetime", title="Stock Price with MA", width=900, height=300)

inc = df["Close"] > df["Open"]
dec = ~inc

p_kline.segment(df["Date"], df["High"], df["Date"], df["Low"], color="black")
p_kline.vbar(df["Date"][inc], 12*60*60*1000, df["Open"][inc], df["Close"][inc], fill_color="green", line_color="green")
p_kline.vbar(df["Date"][dec], 12*60*60*1000, df["Open"][dec], df["Close"][dec], fill_color="red", line_color="red")

p_kline.line(df["Date"], df["MA_10"], legend_label="MA 10", line_width=2, color="blue")
p_kline.line(df["Date"], df["MA_50"], legend_label="MA 50", line_width=2, color="orange")

p_kline.legend.location = "top_left"

# ========== 成交量圖 ==========
p_volume = figure(x_axis_type="datetime", title="Volume", width=900, height=150)
p_volume.vbar(df["Date"], width=12*60*60*1000, top=df["Volume"], fill_color="blue", line_color="blue")

# ========== KDJ 指標 ==========
p_kdj = figure(x_axis_type="datetime", title="KDJ Indicator", width=900, height=150)
p_kdj.line(df["Date"], df["K"], legend_label="K", color="blue", line_width=2)
p_kdj.line(df["Date"], df["D"], legend_label="D", color="orange", line_width=2)
p_kdj.line(df["Date"], df["J"], legend_label="J", color="red", line_width=2)
p_kdj.legend.location = "top_left"

# ========== MACD 指標 ==========
p_macd = figure(x_axis_type="datetime", title="MACD Indicator", width=900, height=150)
p_macd.line(df["Date"], df["MACD"], legend_label="MACD", color="blue", line_width=2)
p_macd.line(df["Date"], df["MACD_Signal"], legend_label="Signal", color="red", line_width=2)
p_macd.vbar(df["Date"], width=12*60*60*1000, top=df["MACD_Hist"], fill_color="gray", line_color="gray")
p_macd.legend.location = "top_left"

# ========== RSI 指標 ==========
p_rsi = figure(x_axis_type="datetime", title="RSI Indicator", width=900, height=150)
p_rsi.line(df["Date"], df["RSI"], legend_label="RSI", color="purple", line_width=2)
p_rsi.line(df["Date"], [70] * len(df), line_dash="dashed", color="red")  # 超買線
p_rsi.line(df["Date"], [30] * len(df), line_dash="dashed", color="green")  # 超賣線
p_rsi.legend.location = "top_left"

# 將圖表排列在一起
layout = column(p_kline, p_volume, p_kdj, p_macd, p_rsi)

# 顯示圖表
show(layout)

