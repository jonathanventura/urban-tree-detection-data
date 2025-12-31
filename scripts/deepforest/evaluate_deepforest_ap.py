""" Evaluate average precision metric on prediction. """
import pandas as pd
import os
import numpy as np
import argparse
from .evaluate_deepforest import load_csvs,evaluate
import tqdm
from tqdm import trange

def calc_ap(precisions,recalls):
    return np.sum((recalls[1:]-recalls[:-1])*precisions[1:])
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('txt')
    parser.add_argument('input')
    args = parser.parse_args()

    thresholds = []
    names = [name.rstrip() for name in open(args.txt,'r')]
    for name in names:  
        pred_path = os.path.join(args.input,f'{name}.csv')
        pred = pd.read_csv(pred_path)
        for i in range(len(pred)):
            thresholds.append(pred.iloc[i]['score'])
    
    thresholds = np.sort(np.unique(thresholds))[::-1]
    print(thresholds)

    pred_scores,isects = load_csvs(args.txt,args.input)

    precisions = []
    recalls = []
    fscores = []
    pbar = tqdm.tqdm(total=len(thresholds))
    for thresh in thresholds:
        precision, recall, fscore = evaluate(pred_scores,isects,score_thresh=thresh)
        precisions.append(precision)
        recalls.append(recall)
        fscores.append(fscore)
        pbar.update(1)
    pbar.close()
    
    precisions = np.array(precisions)
    recalls = np.array(recalls)
    fscores = np.array(fscores)

    ap = calc_ap(precisions,recalls)
    
    df = pd.DataFrame({'threshold':thresholds,'precision':precisions,'recall':recalls,'fscore':fscores})
    df.to_csv(os.path.join('pr_curve.csv'),index=False)
    
    #with open(f'{args.prefix}_aps.csv','a') as f:
        #f.write(f'{args.log},{ap}\n')
    #print(f'{args.log}\t{ap}')
    print(f'ap: {ap}')
