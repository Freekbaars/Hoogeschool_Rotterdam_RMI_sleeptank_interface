import pandas as pd
import plotly


data_1 = pd.read_csv('test.csv')
data_2 = pd.read_csv('test_1.csv')
data_3 = pd.read_csv('test_2.csv')
data_4 = pd.read_csv('test_3.csv')

tijd_1 = data_1['ime [S]']
tijd_2 = data_2['time [S]']
tijd_3 = data_3['time [S]']
tijd_4 = data_4['time [S]']

force_1 = data_1['force [G]']
force_2 = data_2['force [G]']
force_3 = data_3['force [G]']
force_4 = data_4['force [G]']

hoek_x_1 = data_1['Angle X [deg]']
hoek_x_2 = data_2['Angle X [deg]']
hoek_x_3 = data_3['Angle X [deg]']
hoek_x_4 = data_4['Angle X [deg]']

hoek_y_1 = data_1['Angle Y [deg]']
hoek_y_2 = data_2['Angle Y [deg]']
hoek_y_3 = data_3['Angle Y [deg]']
hoek_y_4 = data_4['Angle Y [deg]']


fig = plotly.subplots.make_subplots(rows=2, cols=2, subplot_titles=("Force", "Angle X", "Angle Y", "Force"))
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_1, y=force_1, name='Force 1'), row=1, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_2, y=force_2, name='Force 2'), row=1, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_3, y=force_3, name='Force 3'), row=1, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_4, y=force_4, name='Force 4'), row=1, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_1, y=hoek_x_1, name='Angle X 1'), row=1, col=2)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_2, y=hoek_x_2, name='Angle X 2'), row=1, col=2)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_3, y=hoek_x_3, name='Angle X 3'), row=1, col=2)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_4, y=hoek_x_4, name='Angle X 4'), row=1, col=2)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_1, y=hoek_y_1, name='Angle Y 1'), row=2, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_2, y=hoek_y_2, name='Angle Y 2'), row=2, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_3, y=hoek_y_3, name='Angle Y 3'), row=2, col=1)
fig.add_trace(plotly.graph_objs.Scatter(x=tijd_4, y=hoek_y_4, name='Angle Y 4'), row=2, col=1)
fig.update_layout(height=600, width=800, title_text="Force and Angle")

plotly.offline.plot(fig, filename='test_plot.html')



