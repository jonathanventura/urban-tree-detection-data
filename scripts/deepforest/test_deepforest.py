import cProfile,pstats
import time
import torch
import deepforest
import deepforest.main

import rasterio
import os

import argparse
from multiprocessing import freeze_support

import numpy as np

if __name__ == '__main__':
    freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument('txt')
    parser.add_argument('out')
    parser.add_argument('--checkpoint')
    parser.add_argument('--score_thresh',type=int)
    args = parser.parse_args()

    model = deepforest.main.deepforest()
    model.use_release()
    if args.checkpoint is not None:
        model.model.load_state_dict(torch.load(args.checkpoint))

    print('default score thresh:',model.config['score_thresh'])
    if args.score_thresh is not None:
        model.config['score_thresh'] = args.score_thresh
    model.config["accelerator"] = 'gpu'
    print(model.config)

    os.makedirs(args.out,exist_ok=True)

    names = [name.rstrip() for name in open(args.txt,'r')]
    profiler = cProfile.Profile()
    profiler.enable()
    timings = []
    for name in names:  
        image_path = os.path.join('images',f'{name}.tif')
        csv_path = os.path.join(args.out,f'{name}.csv')
        json_path = os.path.join(args.out,f'{name}.json')
        with rasterio.open(image_path,'r') as src:
            transform = src.transform   
            crs = src.crs
        #start = time.time()
        pred = model.predict_image(path=image_path)
        #end = time.time()
        #timings.append(end-start)
        pred.to_csv(csv_path)
        gdf = deepforest.utilities.annotations_to_shapefile(pred, transform, crs)
        gdf.to_file(json_path,driver='GeoJSON')
    #print('average time:',np.mean(timings)*1000,'ms')
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(.1)    
    stats.dump_stats('predict_file.prof')

