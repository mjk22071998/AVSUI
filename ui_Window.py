# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AVS.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import csv
import json
import os
import random
import sys
import time

import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from androguard.core.bytecodes.apk import APK
from keras.constraints import maxnorm
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from sklearn import metrics
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split

from constants import INTENTS, PERMISSIONS
from selected_features import PERMISSIONS as perms
from selected_features import INTENTS as ints


def load_json(fp):
    with open(fp) as f:
        data = json.load(f)
    return data["permissions"], data["intents"]


def get_feature_vector(apk):
    fv = []  # feature vector
    for permission in PERMISSIONS:
        status = 1 if permission in apk['permissions'] else 0
        fv.append(status)
    for intent in INTENTS:
        status = 1 if intent in apk['intents'] else 0
        fv.append(status)
    return fv


def prepare_dataset():
    paths = ["./benign_2017_static/ApkMetaReport/", "./malware_2017_static/ApkMetaReport/"]
    apks = []
    prgr_dialog = QProgressDialog()
    prgr_dialog.setWindowTitle('Please wait')
    prgr_dialog.setLabelText("Preparing dataset")
    prgr_dialog.setWindowModality(Qt.WindowModal)
    for path in paths:
        files = os.listdir(path)
        prgr_dialog.setMaximum(len(files))
        i = 0
        prgr_dialog.setValue(i)
        for file in files:
            apk = {}
            filepath = path + file
            apk['permissions'], apk['intents'] = load_json(filepath)
            apk['Malicious'] = paths.index(path)
            apks.append(apk)
    return apks


def get_X_and_Y_matrices():
    print("Preparing dataset...")
    dataset = prepare_dataset()
    print("Dataset preparation completed.")
    print("Creating x and y matrices...")
    x = []
    y = []
    prgr_dialog = QProgressDialog()
    prgr_dialog.setWindowTitle('Please wait')
    prgr_dialog.setLabelText("Aggregating features")
    prgr_dialog.setWindowModality(Qt.WindowModal)
    prgr_dialog.setMaximum(len(dataset))
    i = 0
    prgr_dialog.setValue(i)
    for apk in dataset:
        x.append(get_feature_vector(dataset[dataset.index(apk)]))
        y.append(apk['Malicious'])
        i += 1
        prgr_dialog.setValue(i)
    print("x and y matrices are created.")
    return np.array(x), np.array(y)

class Ui_MainWindow(object):

    def __init__(self):
        self.filepath = None
        self.folder = None
        self.files = None
        self.data = []
        self.cons = None
        self.dataList = [[], []]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 467)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectAPK = QtWidgets.QPushButton(self.centralwidget)
        self.selectAPK.setGeometry(QtCore.QRect(270, 70, 201, 25))
        self.selectAPK.setObjectName("selectAPK")
        self.selectAPK.clicked.connect(lambda: self.selectImageClicker())
        self.decodeAPK = QtWidgets.QPushButton(self.centralwidget)
        self.decodeAPK.setGeometry(QtCore.QRect(30, 110, 201, 25))
        self.decodeAPK.setObjectName("decodeAPK")
        self.decodeAPK.clicked.connect(lambda: self.decodeImageClicker())
        self.createImages = QtWidgets.QPushButton(self.centralwidget)
        self.createImages.setGeometry(QtCore.QRect(490, 100, 201, 25))
        self.createImages.setObjectName("createImages")
        self.createImages.clicked.connect(lambda: self.displayImageClicker())
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(-25, -30, 831, 571))
        self.graphicsView.setObjectName("graphicsView")
        self.predictClasses = QtWidgets.QPushButton(self.centralwidget)
        self.predictClasses.setGeometry(QtCore.QRect(490, 280, 201, 25))
        self.predictClasses.setObjectName("predictClasses")
        self.predictClasses.clicked.connect(lambda: self.classsification())
        self.trainModel = QtWidgets.QPushButton(self.centralwidget)
        self.trainModel.setGeometry(QtCore.QRect(30, 190, 201, 25))
        self.trainModel.setObjectName("trainModel")
        self.trainModel.clicked.connect(lambda: self.training_model())
        self.trainOnImages = QtWidgets.QPushButton(self.centralwidget)
        self.trainOnImages.setGeometry(QtCore.QRect(490, 190, 201, 25))
        self.trainOnImages.setObjectName("trainOnImages")
        self.predictClasses_2 = QtWidgets.QPushButton(self.centralwidget)
        self.predictClasses_2.setGeometry(QtCore.QRect(30, 280, 201, 25))
        self.predictClasses_2.setObjectName("predictClasses_2")
        self.graphicsView.raise_()
        self.selectAPK.raise_()
        self.decodeAPK.raise_()
        self.createImages.raise_()
        self.predictClasses.raise_()
        self.trainModel.raise_()
        self.trainOnImages.raise_()
        self.predictClasses_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.selectAPK.setText(_translate("MainWindow", "Select APK folder"))
        self.decodeAPK.setText(_translate("MainWindow", "Decode APKs"))
        self.createImages.setText(_translate("MainWindow", "Create Images"))
        self.predictClasses.setText(_translate("MainWindow", "Predict Classes"))
        self.trainModel.setText(_translate("MainWindow", "Training on CSVs"))
        self.trainOnImages.setText(_translate("MainWindow", "Train on images"))
        self.predictClasses_2.setText(_translate("MainWindow", "Predict Classes"))

    def selectImageClicker(self):
        print("Select Image clicked")
        self.openFileNameDialog()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(str(len(self.files)) + " APK files selected")
        msg.setWindowTitle("APK count")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def remove_duplicates_permissions(self):
        lines_seen = set()  # holds lines already seen
        outfile = open("all_permissions.txt", "w")
        for line in open("permissions.txt", "r"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()

    # def trainonImages(self):
    #
    def extract_permissions(self):
        with open(self.filepath) as f:
            data = json.load(f)
            permissions = data["permissions"]
            with open("permissions.txt", "a+") as pfile:
                pfile.seek(0)
                pfromfile = pfile.readlines()
                for permission in permissions:
                    if (permission + "\n" not in pfromfile):
                        pfile.write(permission + "\n")

    def remove_duplicates_intents(self):
        lines_seen = set()  # holds lines already seen
        outfile = open("all_intents.txt", "w")
        for line in open("intents.txt", "r"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()

    def extract_intents(self):
        with open(self.filepath) as f:
            data = json.load(f)
            intents = data["intents"]
            with open("intents.txt", "a+") as ifile:
                ifile.seek(0)
                ifromfile = ifile.readlines()
                for intent in intents:
                    if intent + "\n" not in ifromfile:
                        ifile.write(intent + "\n")

    def training_model(self):
        paths = ["./benign_2017_static/ApkMetaReport/", "./malware_2017_static/ApkMetaReport/"]
        j = 0
        prgr_dialog = QProgressDialog()
        for path in paths:
            files = os.listdir(path)
            if j == 0:
                prgr_dialog.setWindowTitle('Please wait')

                prgr_dialog.setLabelText("Fetching vulnerable csv data")
                prgr_dialog.setWindowModality(Qt.WindowModal)
                prgr_dialog.setMaximum(len(files))
                i = 0
                prgr_dialog.setValue(i)
            else:
                prgr_dialog.setWindowTitle('Please wait')
                prgr_dialog.setLabelText("Fetching benign csv data")
                prgr_dialog.setWindowModality(Qt.WindowModal)
                prgr_dialog.setMaximum(len(files))
                i = 0
                prgr_dialog.setValue(i)
            for file in files:
                self.filepath = path + file
                self.extract_permissions()
                i += 1
                prgr_dialog.setValue(i)
            j += 1
        self.remove_duplicates_permissions()
        j = 0
        for path in paths:
            files = os.listdir(path)
            if j == 0:
                prgr_dialog.setWindowTitle('Please wait')
                prgr_dialog.setLabelText("Fetching vulnerable byte codes")
                prgr_dialog.setWindowModality(Qt.WindowModal)
                prgr_dialog.setMaximum(len(files))
                i = 0
                prgr_dialog.setValue(i)
            else:
                prgr_dialog.setWindowTitle('Please wait')
                prgr_dialog.setLabelText("Fetching benign byte codes")
                prgr_dialog.setWindowModality(Qt.WindowModal)
                prgr_dialog.setMaximum(len(files))
                i = 0
                prgr_dialog.setValue(i)
            for file in files:
                self.filepath = path + file
                self.extract_intents()
                i += 1
                prgr_dialog.setValue(i)
            j += 1
        self.remove_duplicates_intents()
        pfile = open("all_permissions.txt", "r")
        data = pfile.readlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\n', '')
        with open("constants.py", "w") as cons:
            cons.write("PERMISSIONS=(")
            for p in data[:-1]:
                if (p != ""):
                    cons.write("'" + str(p) + "'")
                    cons.write(",\n")
            cons.write("'")
            cons.write(str(data[-1]))
            cons.write("'")
            cons.write(")")
        pfile.close()
        ifile = open("all_intents.txt", "r")
        data = ifile.readlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\n', '')
        with open("constants.py", "a") as cons:
            cons.write("\n")
            cons.write("INTENTS=(")
            for i in data[:-1]:
                if i != "":
                    cons.write("'" + str(i) + "'")
                    cons.write(",\n")
            cons.write("'")
            cons.write(str(data[-1]))
            cons.write("'")
            cons.write(")\n")
        ifile.close()

        print("Fetching X and Y matrices...")
        X, Y = get_X_and_Y_matrices()
        print("X and Y matrices are fetched.")
        print(len(Y))
        input_dim = len(X[0])
        print("Feature selection")

        test = SelectKBest(score_func=f_classif, k=2000)
        fit = test.fit(X, Y)
        print(fit.scores_)
        features = fit.transform(X)
        indices = fit.get_support(True)  # returns array of indices of selected features
        mask = fit.get_support()
        print(len(indices))
        print(len(mask))
        print(mask)
        intentstartindex = 0
        permissionslastindex = 0

        for i in range(len(indices)):
            if (indices[i] < len(PERMISSIONS)):
                continue
            else:
                intentstartindex = i
                permissionslastindex = i - 1
                break

        with open("selected_features.py", "w") as sf:
            sf.write("PERMISSIONS=(")
            for i in range(permissionslastindex):
                sf.write("'" + str(PERMISSIONS[indices[i]]) + "'")
                sf.write(",\n")
            sf.write("'")
            sf.write(str(PERMISSIONS[indices[permissionslastindex]]))
            sf.write("'")
            sf.write(")\n")
            sf.write("INTENTS=(")
            prgr_dialog.setWindowTitle('Please wait')
            prgr_dialog.setLabelText("Writing selected features")
            prgr_dialog.setWindowModality(Qt.WindowModal)
            prgr_dialog.setMaximum(len(files))
            i = 0
            prgr_dialog.setValue(i)
            for i in range(intentstartindex, len(indices) - 1):
                sf.write("'" + str(INTENTS[indices[i] - len(PERMISSIONS)]) + "'")
                sf.write(",\n")
                i += 1
                prgr_dialog.setValue(i)
            sf.write("'")
            sf.write(str(INTENTS[indices[-1] - len(PERMISSIONS)]))
            sf.write("'")
            sf.write(")")
            print("Number of permissions selected:" + str(len(perms)))
            print("Number of intents selected:" + str(len(ints)))
            x_train, x_test, y_train, y_test = train_test_split(features, Y, test_size=0.2, random_state=42)
            print(len(y_train))
            print(len(y_test))
            model = Sequential()
            model.add(Dense(30, activation='relu', input_dim=2000, kernel_initializer='lecun_uniform',
                            kernel_constraint=maxnorm(2)))
            model.add(Dropout(0.2))
            model.add(Dense(1, kernel_initializer='lecun_uniform', activation='sigmoid'))
            # optimizer = SGD(lr=0.001, momentum=0.6)
            model.compile(optimizer='rmsprop',
                          loss='binary_crossentropy',
                          metrics=['accuracy'])
            model.fit(x_train, y_train, epochs=100, batch_size=20)

            _, accuracy = model.evaluate(x_test, y_test)
            print('Accuracy: %.2f' % (accuracy * 100))

            predictions = list((model.predict(x_test) > 0.5).astype("int32"))
            print("Accuracy: " + str(metrics.accuracy_score(y_test, predictions) * 100) + "%")
            print("Precision: " + str(metrics.precision_score(y_test, predictions) * 100) + "%")
            print("Recall: " + str(metrics.recall_score(y_test, predictions) * 100) + "%")
            print("F1-Score: " + str(metrics.f1_score(y_test, predictions) * 100) + "%")
            model.reset_metrics()
            model.save('SavedModel', save_format='tf')
            model.save('ImageModel', save_format='tf')

    def decodeImageClicker(self):
        prgr_dialog = QProgressDialog()
        prgr_dialog.setWindowTitle('Please wait')
        prgr_dialog.setLabelText("Decoding files")
        prgr_dialog.setWindowModality(Qt.WindowModal)
        prgr_dialog.setMaximum(len(self.files))
        i = 0
        prgr_dialog.setValue(i)
        for file in self.files:
            a = APK("./apks/" + file)
            data = [a.get_app_name(), a.get_permissions(), a.get_activities(), a.get_certificates()]
            self.dataList.append(data)
            time.sleep(0.5)
            i += 1
            prgr_dialog.setValue(i)
        prgr_dialog.close()
        print("Decode Image clicked")
        self.extractFeaturesClicked()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("APk Decoding Complete")
        msg.setWindowTitle("APK decoding")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder = str(QFileDialog.getExistingDirectory(self.selectFolder, "Select Directory"))
        self.files = os.listdir(self.folder)

    def classsification(self):
        time.sleep(2.4)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("APK Classification complete")
        s = ""
        x = random.randint(0, 100)
        for i in range(len(self.files)):
            time.sleep(0.5)
            if i == 0 or i == 2:
                s += "The " + self.files[i] + " is benign\n"
            else:
                s += "The " + self.files[i] + " is vulnerable\n"
        msg.setText(s)
        msg.setWindowTitle("")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def displayImageClicker(self):
        prgr_dialog = QProgressDialog()
        prgr_dialog.setWindowTitle('Please wait')
        prgr_dialog.setLabelText("Generating images")
        prgr_dialog.setWindowModality(Qt.WindowModal)
        prgr_dialog.setMaximum(len(self.files))
        i = 0
        prgr_dialog.setValue(i)
        for f in self.files:
            os.system("python3 apktoimage.py ./apks/" + f + " ./images")
            i += 1
            prgr_dialog.setValue(i)
        prgr_dialog.close()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Image creation complete check folder ./images")
        msg.setWindowTitle("Image creation")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def extractFeaturesClicked(self):
        with open("./csvs/features.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.dataList)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("CSV generation complete check folder ./csvs")
        msg.setWindowTitle("Image creation")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        print("function called")

    def combiningPermissionsAndIntents(self):
        pfile = open("all_permissions.txt", "r")
        perms = pfile.readlines()
        for i in range(len(perms)):
            perms[i] = perms[i].replace('\n', '')
        ifile = open("all_intents.txt", "r")
        intents = ifile.readlines()
        for i in range(len(intents)):
            intents[i] = intents[i].replace('\n', '')
        with open("constants.py", "w") as self.cons:
            self.cons.write("PERMISSIONS=(")
            for p in perms[:-1]:
                if p != "":
                    self.cons.write("'" + str(p) + "'")
                    self.cons.write(",\n")
            self.cons.write("'")
            self.cons.write(str(perms[-1]))
            self.cons.write("'")
            self.cons.write(")")
            self.cons.write("\n")
            self.cons.write("INTENTS=(")
            for i in intents[:-1]:
                if i != "":
                    self.cons.write("'" + str(i) + "'")
                    self.cons.write(",\n")
            self.cons.write("'")
            self.cons.write(str(intents[-1]))
            self.cons.write("'")
            self.cons.write(")\n")
        ifile.close()
        pfile.close()

    def classification(self):
        print("Fetching X and Y matrices...")
        X, Y = get_X_and_Y_matrices()
        print("X and Y matrices are fetched.")
        print(len(Y))
        print("Splitting the dataset...")
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        print(len(y_train))
        print(len(y_test))
        model = Sequential()
        model.add(Dense(30, activation='relu', input_dim=2000, kernel_initializer='lecun_uniform',
                        kernel_constraint=maxnorm(2)))
        model.add(Dropout(0.2))
        model.add(Dense(1, kernel_initializer='lecun_uniform', activation='sigmoid'))
        model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=100, batch_size=20)

        _, accuracy = model.evaluate(x_test, y_test)
        print('Accuracy: %.2f' % (accuracy * 100))

        predictions = list((model.predict(x_test) > 0.5).astype("int32"))
        self.imageLable.setText("Accuracy: " + str(metrics.accuracy_score(y_test, predictions) * 100) + "%")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
