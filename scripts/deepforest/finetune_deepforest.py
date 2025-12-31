import time
import albumentations as A
from deepforest import main 
from deepforest import get_data
from deepforest import utilities
from deepforest import preprocess
import torch
import argparse
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument('--annotations',required=True)
    parser.add_argument('--checkpoint',required=True)
    parser.add_argument('--epochs',type=int,default=1)
    args = parser.parse_args()

    model = main.deepforest()

    def get_transform(augment):
        """This is the new transform"""
        if augment:
            transform = A.Compose([
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.5),
                A.augmentations.geometric.rotate.RandomRotate90(p=0.5),
                ToTensorV2()
            ], bbox_params=A.BboxParams(format='pascal_voc',label_fields=["category_ids"]))
            
        else:
            transform = ToTensorV2()
            
        return transform

    model.config['train']["epochs"] = args.epochs
    #model.config["save-snapshot"] = True
    model.config["accelerator"] = 'gpu'
    model.config["train"]["csv_file"] = args.annotations
    model.config["train"]["root_dir"] = 'images'

    model.create_trainer()

    model.use_release()

    start_time = time.time()
    model.trainer.fit(model)
    print(f"--- Training on GPU: {(time.time() - start_time):.2f} seconds ---")

    torch.save(model.model.state_dict(),args.checkpoint)

