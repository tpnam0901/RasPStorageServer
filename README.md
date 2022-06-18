# [Raspberry Pi 4 Storage Server](https://github.com/namphuongtran9196/RasPStorageServer.git)

![Star](https://img.shields.io/github/stars/namphuongtran9196/RasPStorageServer)
![Fork](https://img.shields.io/github/forks/namphuongtran9196/RasPStorageServer)
![License](https://img.shields.io/github/license/namphuongtran9196/RasPStorageServer)

![Teaser](./docs/teaser.gif)


>  The usage for the paper Real-Time High-Resolution Background Matting. Their model requires capturing an additional background image and produces state-of-the-art matting results at 4K 30fps and HD 60fps on an Nvidia RTX 2080 TI GPU.

Project website: &nbsp; [Background Matting](https://grail.cs.washington.edu/projects/background-matting-v2/#/)

Original Paper: &nbsp; [Arxiv](https://arxiv.org/abs/2012.07810)

Offical Implementation: &nbsp; [Pytorch](https://github.com/PeterL1n/BackgroundMattingV2), [Tensorflow](https://github.com/PeterL1n/BackgroundMattingV2-TensorFlow.git)

****

## Contents
:bookmark_tabs:

* [Installation](#Installation)
* [Usage](#Usage)
* [References](#References) <!-- * [License](#License) -->
* [Citation](#Citation)

## Installation
:pizza:

Create a new python virtual environment by [Anaconda](https://www.anaconda.com/) or just use pip in your python environment and then clone this repository as following.

### Clone this repo
```bash
git clone https://github.com/knglab/GreenBack.git
cd GreenBack
```

### Install libraries
* Via conda
```bash
conda env create -f environment.yml
conda activate greenback
```
* Via pip
```bash
pip install -r requirements.txt
```
### Download pretrained models
* Via terminal
```bash
gdown 1zzMjY3gRlTvpKgsxaZO7nzGDg0YTEaId # model.pth
```
* Via link: [Google Drive](https://drive.google.com/file/d/1zzMjY3gRlTvpKgsxaZO7nzGDg0YTEaId/view?usp=sharing)
****

## Usage
:beer:

You can download some samples by following the link below.
* [Google Drive](https://drive.google.com/file/d/1JRmG9NKw2mkDL5Nr_d4ua3bDrTEL7MSI/view?usp=sharing)

### Inference
```bash
python inference.py [-h] [-i INPUT] [-i_bg INPUT_BG] [-o OUTPUT] [-w WEIGHTS] {image,video,webcam}
```
```
positional arguments:
  {image,video,webcam}  mode of inference

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the input image (.jpg, .png), required for image and video mode.
  -i_bg INPUT_BG, --input_bg INPUT_BG
                        Path to input background image (.jpg, .png), required for image and video mode.
  -o OUTPUT, --output OUTPUT
                        Path to the output folder.
  -w WEIGHTS, --weights WEIGHTS
                        Path to the model Pytorch (model.pth).
  --gpu                 Use GPU for inference.
```
* Image inference example
```bash
python inference.py image -i ./path/to/image.jpg -i_bg ./path/to/background.jpg -o ./path/to/output_folder -w ./path/to/model.pth 
```
* Video inference example

You can get the first frame of the video by using the following command. The image will save to the same folder of the video
```bash
python get_first_frame.py -i ./path/to/video.mp4
```
Inference with the background image
```bash
python inference.py video -i ./path/to/video.mp4 -i_bg ./path/to/background.jpg -o ./path/to/output_folder -w ./path/to/model.pth 
```
* Webcam inference example
```bash
python inference_image.py -w ./path/to/model.pth 
```
* Using GPU inference
```bash
python inference.py image --gpu -i input -o output
```

## References
:hamburger:
- https://github.com/PeterL1n/BackgroundMattingV2 (Official)
    - [BackgroundMattingV2](https://arxiv.org/abs/2012.07810) (Real-Time High-Resolution Background Matting)

## Citation
```bash
@article{BGMv2,
  title={Real-Time High-Resolution Background Matting},
  author={Lin, Shanchuan and Ryabtsev, Andrey and Sengupta, Soumyadip and Curless, Brian and Seitz, Steve and Kemelmacher-Shlizerman, Ira},
  journal={arXiv},
  pages={arXiv--2012},
  year={2020}
}
```

<!-- ## License
Copyright &copy; 2021 [K&G Technology](http://www.kng.vn). All rights reserved. -->