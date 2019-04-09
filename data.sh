#! /bin/bash
set -euo pipefail
. ./env/bin/activate
echo "Please make sure to download the ISIC 2017 data from https://challenge.kitware.com/#challenge/n/ISIC_2017%3A_Skin_Lesion_Analysis_Towards_Melanoma_Detection to ./data/isic2017/"

timestamp=$(date +%s)

for pretrained_model in vgg16 inceptionv3; do
	echo "Processing training data for $pretrained_model networks..."
    mkdir -p ./data/training_"$pretrained_model"_$timestamp/
	python ./src/data.py --images ./data/isic2017/ISIC-2017_Training_Data/ \
                         --descriptions ./data/isic2017/ISIC-2017_Training_Part3_GroundTruth.csv \
                         --output ./data/train_"$pretrained_model"_$timestamp \
                         --pretrained-model $pretrained_model/ \
                         --total-samples 8000
    ln -nsf ./data/train_$pretrained_model/train_"$pretrained_model"_$timestamp.npz ./data/train_$pretrained_model.npz

	echo "Processing validation data for $pretrained_model networks..."
    mkdir -p ./data/validation_"$pretrained_model"_$timestamp/
	python ./src/data.py --images ./data/isic2017/ISIC-2017_Validation_Data/ \
                         --descriptions ./data/isic2017/ISIC-2017_Validation_Part3_GroundTruth.csv \
                         --output ./data/validation_"$pretrained_model"_$timestamp/ \
                         --pretrained-model $pretrained_model
    ln -nsf ./data/validation_$pretrained_model/validation_"$pretrained_model"_$timestamp.npz ./data/validation_$pretrained_model.npz

	echo "Processing test data for $pretrained_model networks..."
    mkdir -p ./data/test_"$pretrained_model"_$timestamp/
	python ./src/data.py --images ./data/isic2017/ISIC-2017_Test_v2_Data/ \
                         --descriptions ./data/isic2017/ISIC-2017_Test_v2_Part3_GroundTruth.csv \
                         --output ./data/test_"$pretrained_model"_$timestamp/ \
                         --pretrained-model $pretrained_model
    ln -nsf ./data/test_$pretrained_model/test_"$pretrained_model"_$timestamp.npz ./data/test_$pretrained_model.npz
done

cd ./data/
python -m http.server 1338