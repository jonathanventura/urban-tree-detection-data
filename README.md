## Urban Tree Detection Data ##

This repository provides a dataset for training and evaluating tree detectors in urban environments with aerial imagery.  The dataset includes:

* 256x256 crops of 60 cm aerial imagery from the 2020 NAIP imagery program across six cities in California
* Point annotations for all trees visible in the imagery
* A train/val/test split to replicate or compare against the results in our paper

### Data description ###

The dataset covers five cities in California.  The following table provides a summary:

| City         | Year | Climate Zone              | Number of Tiles | Number of Trees |
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

The dataset is in the `data` directory, with one sub-directory for each city. 
* Images are stored in the `patches` directory as TIFF files.
* Each image has an associated CSV file in the `csv` directory containing tree locations in 2D pixel coordinates.
* Geo-referenced tree locations for each image are stored in the GeoJSON format in the `json` directory.  Coordinates are stored in the local UTM zone.

### Citation ###

NAIP on AWS was accessed on January 28, 2022 from https://registry.opendata.aws/naip.

If you use this data, please cite our paper:

### Acknowledgments ###

This project was funded by CAL FIRE (award number: 8GB18415) the US Forest Service (award number: 21-CS-11052021-201), and an incubation grant from the Data Science Strategic Research Initiative at California Polytechnic State University.

