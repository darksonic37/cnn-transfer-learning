import os
import itertools
import argparse
import csv
import json

import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics

import helpers


CLASSES = ['Non Melanoma', 'Melanoma']


# TODO: refactor this function
def load(predictions):
    data = np.load(predictions)
    y_true = data['y_true']
    y_pred = data['y_pred']
    return y_true, y_pred


def plot_test_confusion_matrix(y_true, y_pred, target_file, classes=CLASSES, title='Confusion matrix', cmap=plt.cm.Blues):
    cm = sklearn.metrics.confusion_matrix(y_true, y_pred)
    print(cm)

    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(CLASSES))
    plt.xticks(tick_marks, CLASSES, rotation=45)
    plt.yticks(tick_marks, CLASSES)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'), horizontalalignment='center', color='white' if cm[i, j] > thresh else 'black')

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(target_file)


def plot_train_loss(train_csv, target_file):
    loss = []

    with open(train_csv, 'r', newline='') as f:
        for i, row in enumerate(csv.DictReader(f)):
            loss.append(float(row['loss']))

    loss = np.array(loss, dtype='float32')
    epochs = range(len(loss))

    plt.figure()
    plt.plot(epochs, loss, 'b', label='Train loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.title('Train loss')
    plt.legend()
    plt.savefig(target_file)


def plot_train_f1(train_csv, target_file):
    f1 = []

    with open(train_csv, 'r', newline='') as f:
        for i, row in enumerate(csv.DictReader(f)):
            f1.append(float(row['f1']))

    f1 = np.array(f1, dtype='float32')
    epochs = range(len(f1))

    plt.figure()
    plt.plot(epochs, f1, 'b', label='Train F1-score')
    plt.ylabel('F1-score')
    plt.xlabel('Epoch')
    plt.title('Train F1-score')
    plt.legend()
    plt.savefig(target_file)


def plot_test_classification_report(y_true, y_pred, target_file):
    report = sklearn.metrics.classification_report(y_true, y_pred, target_names=CLASSES, output_dict=True)
    with open(target_file, 'w') as f:
        json.dump(report, f)


def plot(experiment):
    try:
        y_true, y_pred = load(os.path.join(experiment, 'predictions.npz'))
        plot_train_loss(os.path.join(experiment, 'train.csv'), os.path.join(experiment, 'train_loss.png'))
        plot_train_f1(os.path.join(experiment, 'train.csv'), os.path.join(experiment, 'train_f1.png'))
        plot_test_confusion_matrix(y_true, y_pred, os.path.join(experiment, 'test_confusion_matrix.png'))
        plot_test_classification_report(y_true, y_pred, os.path.join(experiment, 'test_classification_report.json'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment', type=helpers.is_dir, required=True)
    args = parser.parse_args()

    plot(args.experiment)
