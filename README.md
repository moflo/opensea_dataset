# TFDS Dataset Creation for Opensea NFT Collection

Download a dataset of images and artifacts from Opensea.io NFT collection

## Creation

Use the creation script to download an Opensea Collection

```
cd opensea_dataset/build
python download.py --name NAME --start 0 --end 10
```


## Usage

You can use this from with Colab using the following methods:

```
!pip install git+https://github.com/moflo/opensea_dataset.git
!pip install tfds_nightly

import tensorflow as tf
tf.__version__  # should be 2.7.0

import tensorflow_datasets as tfds
import opensea_dataset
ds = tfds.load('opensea_dataset', split='train')
```
