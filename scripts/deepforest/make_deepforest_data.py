import os
import glob
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('radius',type=int)
parser.add_argument('output')
args = parser.parse_args()

with open(args.output,'w') as f:
  f.write('image_path,xmin,ymin,xmax,ymax,label\n')
  names = [line.rstrip() for line in open('train.txt','r')]
  for name in names:
    if not os.path.exists(f'csv/{name}.csv'): continue
    df = pd.read_csv(f'csv/{name}.csv')
    for i in range(len(df)):
      x = int(df.iloc[i].x)
      y = int(df.iloc[i].y)
      xmin = max(x-args.radius,0)
      ymin = max(y-args.radius,0)
      xmax = min(x+args.radius,255)
      ymax = min(y+args.radius,255)
      f.write(f'{name}.tif,{xmin},{ymin},{xmax},{ymax},Tree\n')
  
