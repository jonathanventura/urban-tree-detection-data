## Urban Tree Detection Data ##

This repository provides a dataset for training and evaluating tree detectors in urban environments with aerial imagery.  The dataset includes:

* 256x256 crops of 60 cm aerial imagery from the 2020 NAIP imagery program across six cities in California
* Point annotations for all trees visible in the imagery
* A train/val/test split to replicate or compare against the results in our paper

### Data description ###

The dataset covers five cities in California.  The following table provides a summary:

| City         | Year | Climate Zone              | Number of Crops | Number of Trees |
|--------------|------|---------------------------|-----------------|-----------------|
| Chico        | 2018 | Inland Valleys            |              99 |           9,232 |
| Claremont    | 2020 | Inland Empire             |              92 |           4,680 |
| Long Beach   | 2020 | Southern California Coast |             100 |           5,846 |
| Palm Springs | 2020 | Southwest Desert          |             100 |           8,374 |
| Riverside    | 2020 | Inland Empire             |              90 |           6,019 |
| Santa Monica | 2020 | Southern California Coast |              92 |           5,842 |

The bands in the imagery are as follows:

| Band | Description |
|------|-------------|
|    0 | Red         |
|    1 | Green       |
|    2 | Blue        |
|    3 | Near-IR     |

### Data organization ###

* Images are stored in the `images` directory as TIFF files.
* Each image has an associated CSV file in the `csv` directory containing tree locations in 2D pixel coordinates.
* Each image has an associated GeoJSON file in the `json` directory containing geo-referenced tree locations.  Coordinates are stored in the local UTM zone.
* A missing .csv or .json file means that there are no trees in the image.

The files `train.txt`, `val.txt`, and `test.txt` specify the splits that were used in our paper.

### Citation ###

NAIP on AWS was accessed on January 28, 2022 from https://registry.opendata.aws/naip.

If you use this data, please cite our paper:

J. Ventura, M. Honsberger, C. Gonsalves, J. Rice, C. Pawlak, N.L.R. Love, S. Han, V. Nguyen, K. Sugano, J. Doremus, G.A. Fricker, J. Yost, and M. Ritter. ["Individual Tree Detection in Large-Scale Urban Environments using High-Resolution Multispectral Imagery."](https://doi.org/10.48550/arXiv.2208.10607)  arXiv:2208.10606 [cs], Aug. 2022.

### Acknowledgments ###

This project was funded by CAL FIRE (award number: 8GB18415) the US Forest Service (award number: 21-CS-11052021-201), and an incubation grant from the Data Science Strategic Research Initiative at California Polytechnic State University.

### License ###

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
