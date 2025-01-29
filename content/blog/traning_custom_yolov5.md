+++
title = "Training a custom yolov5 model"
date = 2024-12-19
draft = false

[taxonomies]
categories = ["AI", "Software"]
tags = ["Coding", "Yolo", "Python"]

[extra]
lang = "en"
+++

## Training a custom YOLOv5 model

Recently I have been working on creating a chrome extension for a GooglexMLB hackathon for which I have been using a deep learning model called `yolo` to track baseballs, pitchers, catchers and bats. I figured I will document how this process works so, these are the steps you need to follow to train your YOLOv5s model.

1. Clone the YOLOv5 repository

```sh
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
```
2. Install the dependencies

```sh
pip install -r requirements.txt
```

Head over to a [roboflow dataset](https://universe.roboflow.com/yolotest1/yolov5test2). Download the dataset in the `YOLO v5 PyTorch` format. You might get a download link as below. 

Execute the script where you want to save your dataset. Mostly do this inside the `yolov5` directory itself (that we cloned above)

```sh
curl -L "https://universe.roboflow.com/ds/lPAYhwr8hN?key=o2ef7xqXid" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
```

Ensure that it has a `train` and `test` directories with **images** and **labels** inside them.

Then edit the `data.yaml` file and update the paths to the training and testing datasets

> You can remove the `val` header in there. Also, if the dataset contains more than 1 objects that it can detect, then insure that you're filtering for baseballs only.

Example `data.yaml`

```yaml
        train: ../train/images
        val: ../valid/images
        test: ../test/images

        nc: 3
        names: ['ball', 'bat', 'glove']

        roboflow:
          workspace: yolotest1
          project: yolov5test2
          version: 1
          license: CC BY 4.0
          url: https://universe.roboflow.com/yolotest1/yolov5test2/dataset/1
```
---

Now, comes the crucial part. Read the `README.roboflow.txt` it will look something like this

        yolov5test2 - v1 2024-03-13 9:56am
        ==============================

        This dataset was exported via roboflow.com on March 13, 2024 at 1:57 AM GMT

        Roboflow is an end-to-end computer vision platform that helps you
        * collaborate with your team on computer vision projects
        * collect & organize images
        * understand and search unstructured image data
        * annotate, and create datasets
        * export, train, and deploy computer vision models
        * use active learning to improve your dataset over time

        For state of the art Computer Vision training notebooks you can use with this dataset,
        visit https://github.com/roboflow/notebooks

        To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

        The dataset includes 895 images.
        Baseball are annotated in YOLO v5 PyTorch format.

        The following pre-processing was applied to each image:
        * Auto-orientation of pixel data (with EXIF-orientation stripping)
        * Resize to 640x640 (Stretch)

        The following augmentation was applied to create 3 versions of each source image:
        * 50% probability of horizontal flip
        * Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise

This is important because 

1. We want to enter the image size when we are training it (in this case 640x640 pixels). 
2. We want to create the exact same situation when we are testing it in our use case (that is, before running this model, we'll edit the image similarly and resize it)

---

Inside the `yolov5` directory then run the following code

        python3 train.py --img 640 --batch 16 --epochs 50 --data ./data.yaml --weights yolov5s.pt --name baseball_detection

This will start training the model. The new weights will be saved in `runs/train/baseball_detection/weights/best.pt`

So, in order to use the model, we'll have to use the `best.pt` weights. Refer to the using codes for that. 
