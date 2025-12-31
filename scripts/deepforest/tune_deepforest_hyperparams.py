from .evaluate_deepforest import load_csvs,evaluate
import argparse
import os
import imageio
import h5py as h5
import optuna
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('txt')
parser.add_argument('input')
parser.add_argument('--ntrials', type=int, default=200, help='number of trials')
parser.add_argument('--max_distance', type=float, default=10, help='max distance from gt to pred tree (in input image pixels)')

args = parser.parse_args()

pred_scores,isects = load_csvs(args.txt,args.input)

def objective(trial):
    score_thresh = trial.suggest_float('score_thresh',0,1)
    precision, recall, fscore = evaluate(
        pred_scores,isects,
        score_thresh=score_thresh)
    return 1 - fscore

study = optuna.create_study()
study.optimize(objective, n_trials=args.ntrials)

print(study.best_params)
with open(os.path.join(args.input,'params.txt'),'w') as f:
    f.write(str(study.best_params['score_thresh']) + '\n')

