import glob
import pandas as pd
import rasterio
import imageio
import os
import cv2
import numpy as np

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images',required=True)
    parser.add_argument('--csv',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--params',required=True)
    args = parser.parse_args()

    score_thresh = float(np.loadtxt(args.params))

    os.makedirs(args.output,exist_ok=True)

    csv_paths = sorted(glob.glob(os.path.join(args.csv,'*.csv')))
    names = [os.path.basename(path).split('.')[0] for path in csv_paths]
    for name in names:  
        image_path = os.path.join('images',f'{name}.tif')
        image = np.array(imageio.imread(image_path)[...,:3])
        print(image.shape,image.dtype)
        csv_path = os.path.join(args.csv,f'{name}.csv')
        df = pd.read_csv(csv_path)
        for i in range(len(df)):
            if df.iloc[i]['score'] < score_thresh: continue
            xmin = int(df.iloc[i]['xmin'])
            ymin = int(df.iloc[i]['ymin'])
            xmax = int(df.iloc[i]['xmax'])
            ymax = int(df.iloc[i]['ymax'])
            cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(255,255,0),1)
        output_path = os.path.join(args.output,f'{name}.png')
        imageio.imwrite(output_path,image)
        

