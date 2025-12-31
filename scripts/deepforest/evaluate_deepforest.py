import pandas as pd
import geopandas as gpd
import os
import numpy as np
import scipy
import scipy.optimize
import argparse
import tqdm
import numpy as np

def load_csvs(txt_path,input_path):
    names = [name.rstrip() for name in open(txt_path,'r')]
    pred_scores = []
    isects = []
    dists = []
    pbar = tqdm.tqdm(total=len(names))
    for name in names:  
        gt_path = os.path.join('csv',f'{name}.csv')
        pred_path = os.path.join(input_path,f'{name}.csv')
        if not os.path.exists(gt_path):
            gt = []
        else:
            gt = pd.read_csv(gt_path)
        pred = pd.read_csv(pred_path)
        isect = np.zeros((len(gt),len(pred)))
        dist = np.zeros((len(gt),len(pred)))
        for i in range(len(gt)):
            x = gt.iloc[i].x
            y = gt.iloc[i].y
            xmin = pred.xmin
            ymin = pred.ymin
            xmax = pred.xmax
            ymax = pred.ymax
            xmean = (xmin+xmax)/2
            ymean = (ymin+ymax)/2
            dist[i] = np.sqrt((xmean-x)**2+(ymean-y)**2)
            isect[i] = (x >= xmin) & (y >= ymin) & (x <= xmax) & (y <= ymax)
            """
            for j in range(len(pred)):
                x = gt.iloc[i].x
                y = gt.iloc[i].y
                xmin = pred.iloc[j].xmin
                ymin = pred.iloc[j].ymin
                xmax = pred.iloc[j].xmax
                ymax = pred.iloc[j].ymax
                xmean = (xmin+xmax)/2
                ymean = (ymin+ymax)/2
                dist[i,j] = np.sqrt((xmean-x)**2+(ymean-y)**2)
                isect[i,j] = (x >= xmin) and (y >= ymin) and \
                             (x <= xmax) and (y <= ymax)
            """
        pred_scores.append(np.array(pred['score']))
        isects.append(isect)
        dists.append(dist)
        pbar.update(1)
    return pred_scores, isects, dists

#def evaluate(txt_path,input_path,score_thresh=0):
def evaluate(pred_scores,isects,dists,score_thresh=0):
    all_tp = 0
    all_fp = 0
    all_fn = 0
    
    total_dist = 0
    count = 0

    #names = [name.rstrip() for name in open(txt_path,'r')]
    #pbar = tqdm.tqdm(total=len(names))
    #for name in names:  
    for pred_score,isect,dist in zip(pred_scores,isects,dists):
        #gt_path = os.path.join('csv',f'{name}.csv')
        #pred_path = os.path.join(input_path,f'{name}.csv')
        #gt = pd.read_csv(gt_path)
        #pred = pd.read_csv(pred_path)
        #pred = pred.loc[pred.score>=score_thresh]
        #isect = np.zeros((len(gt),len(pred)))
        #for i in range(len(gt)):
            #for j in range(len(pred)):
                #x = gt.iloc[i].x
                #y = gt.iloc[i].y
                #xmin = pred.iloc[j].xmin
                #ymin = pred.iloc[j].ymin
                #xmax = pred.iloc[j].xmax
                #ymax = pred.iloc[j].ymax
                #isect[i,j] = (x >= xmin) and (y >= ymin) and \
                             #(x <= xmax) and (y <= ymax)
        isect = isect[:,pred_score>=score_thresh]
        dist = dist[:,pred_score>=score_thresh]
        rows,cols = scipy.optimize.linear_sum_assignment(isect,maximize=True)
        val = isect[rows,cols]
        rows = rows[val>0] 
        cols = cols[val>0] 

        d = dist[rows,cols]
        total_dist += np.sum(d**2)
        count += len(rows)
        
        tp = len(rows)
        fp = isect.shape[1]-tp
        fn = isect.shape[0]-tp
         
        all_tp += tp
        all_fp += fp
        all_fn += fn
        
        #pbar.update(1)

    rmse = np.sqrt(total_dist / count)
    if all_tp+all_fp>0:
        precision = all_tp/(all_tp+all_fp)
    else:
        precision = 0
    if all_tp+all_fn>0:
        recall = all_tp/(all_tp+all_fn)
    else:
        recall = 0
    if precision+recall>0:
        fscore = 2*(precision*recall)/(precision+recall)
    else:
        fscore = 0
    
    return precision, recall, fscore, rmse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('txt')
    parser.add_argument('input')
    parser.add_argument('--params')
    args = parser.parse_args()
    
    score_thresh = 0.1
    if args.params is not None:
        score_thresh = float(np.loadtxt(args.params))
    print(score_thresh)
    pred_scores,isects,dists = load_csvs(args.txt,args.input)
    precision, recall, fscore, rmse = evaluate(pred_scores,isects,dists,score_thresh=score_thresh)

    print('precision:',precision)
    print('recall:',recall)
    print('fscore:',fscore)
    print('rmse:',rmse)
    with open('deepforest_results.csv','a') as f:
        f.write(args.input+',')
        f.write(str(precision)+',')
        f.write(str(recall)+',')
        f.write(str(fscore)+',')
        f.write(str(rmse)+'\n')

