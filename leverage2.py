import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math
from numpy import diff
from plotly.subplots import make_subplots
from google.colab import data_table
from vega_datasets import data
import scipy.interpolate
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy.interpolate import UnivariateSpline
def shock2wheel(s,r):
  grad2=1/r
  inc2=s[1]
  shock2=[]
  pos2=0
  for a in grad2:
    shock2.append(pos2)  
    x=inc2/a
    pos2=pos2+x
  return shock2

def build_leverage_data(position,ratio,t,name):
  df=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Frame Data/frame_database.csv',index_col=(0,1), header=None)
  columns=df.columns
  b=np.max(position) 
  if b < 80:
    position=np.array(position)
    ratio=np.array(ratio)
    points=shock2wheel(position,ratio) 
  else:
    points=position
  travel2=float(t)
  points2=np.round(np.linspace(0,travel2,100),4) #(use retstep=True to return step)
  spl = UnivariateSpline(points, ratio, k=3)
  lr2= np.round(spl(points2),4)
  

  numbers=[points2,lr2]
  multidex=[[f'{name}',f'{name}'],['position','Ratio']]
  DB=pd.DataFrame(numbers, index=multidex,columns=columns)
  
  return DB 

def make_MIBD_file(position,ratio):
  travel2=position[-1]
  points3=np.round(np.linspace(0,travel2,101),4) #(use retstep=True to return step)
  spl2 = UnivariateSpline(position, ratio)
  lr3= np.round(spl2(points3),4)
  c=np.max(points3)
  if c < 80:
    points4=shock2wheel(points3,lr3) 
  else:
    points4=points3
  numbers2=[lr3,points4]
  l=np.column_stack(numbers2)
  leverage_column=l[::10]
  text=['section, description\n',f'manufacture, {brand}\n',f'model, {model}\n',f'year, {year}\n',f'frame size, {size}\n','suspension, softail\n', 
        f'fork travel, {travel}\n',f'shock travel, {shock_stroke}\n',f'HA, {ha}\n','old-model-name, \n' ,'section, linear sensor\n']
  file1 = open(f'{brand}_{model}.mibd',"a")
  file1.writelines(text)
  np.savetxt(file1, leverage_column, delimiter=',',fmt='%3.1f,%3.2f') 
  file1.write('section, angle sensor')
  file1.close()  
def plot_leverage_ratio(data):
  bike=data.index[0][0]
  x=data.loc[(bike,'position'),:]
  y=data.loc[(bike,'Ratio'),:]

  fig=px.line(x=x, y=y)
  fig.update_layout(title=bike, title_font_size=25,
                    xaxis_title='travel',
                    yaxis_title='ratio' ,
                    yaxis=dict(range=(1.8,3.5
                      )),
                    width=800,
                    height=800)
  fig.show() 


   


# DB=build_leverage_data(position,ratio,travel)
# plot_leverage_ratio(DB)



# make_MIBD_file(position,ratio)
def update_database(DB):
  df=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Frame Data/frame_database.csv',index_col=(0,1), header=None)
  update=pd.concat([df,DB])
  update.to_csv('/content/drive/MyDrive/Colab Notebooks/Frame Data/frame_database.csv',header=False)
