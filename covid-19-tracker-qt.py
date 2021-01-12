# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget,GraphicsLayoutWidget,plot
import pyqtgraph as pg
import pandas as pd
import random
import numpy as np
import os; os.environ["QT_API"] = "pyqt5"
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
import speech_recognition as sr
import sys
import datetime
import requests
import time
import urllib.request
import json


# get the data from web
url_csv = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
# readinf dropping all NAN values
df_covid_2019 = pd.read_csv(url_csv)
df_covid_2019 = df_covid_2019.dropna()
#df_covid_2019['cases_weekly'] = df_covid_2019['cases_weekly_weekly']
#df_covid_2019['deaths_weekly'] = df_covid_2019['deaths_weekly_weekly']
#df_covid_2019['notification_rate_per_100000_population_14-days'] = df_covid_2019['notification_rate_per_100000_population_14-days']


class Ui_CovidTracker(object):
    def setupUi(self, CovidTracker):
        CovidTracker.setObjectName("CovidTracker")
        CovidTracker.resize(988, 823)
        self.centralwidget = QtWidgets.QWidget(CovidTracker)
        self.centralwidget.setObjectName("centralwidget")

        #plot tab
        self.plot_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.plot_tab.setGeometry(QtCore.QRect(10, 310, 971, 451))
        self.plot_tab.setObjectName("plot_tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.graphicsView = PlotWidget(self.tab)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 961, 421))
        self.graphicsView.setObjectName("graphicsView")
        self.plot_tab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView_2 = PlotWidget(self.tab_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 0, 961, 421))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.plot_tab.addTab(self.tab_2, "")

        # self.plot_tab.addTab(self.tab, "")
        # self.tab_3 = QtWidgets.QWidget()
        # self.tab_3.setObjectName("tab_3")
        # self.graphicsView_3 = GraphicsLayoutWidget(self.tab_3)
        # self.graphicsView_3.setGeometry(QtCore.QRect(0, 0, 961, 421))
        # self.graphicsView_3.setObjectName("graphicsView_3")
        # self.plot_tab.addTab(self.tab_3, "")
        
        #country name
        self.country_name = QtWidgets.QLineEdit(self.centralwidget)
        self.country_name.setGeometry(QtCore.QRect(850, 150, 113, 22))
        self.country_name.setObjectName("country_name")

        #track button
        self.track_button = QtWidgets.QPushButton(self.centralwidget)
        self.track_button.setGeometry(QtCore.QRect(850, 180, 111, 31))
        self.track_button.setObjectName("track_button")
        self.track_button.clicked.connect(self.get_covid)

        #speak button
        self.speak_button = QtWidgets.QPushButton(self.centralwidget)
        self.speak_button.setGeometry(QtCore.QRect(850, 220, 111, 28))
        self.speak_button.setObjectName("speak_button")
        self.speak_button.clicked.connect(self.start_record)

        #reset button
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(850, 260, 111, 28))
        self.reset_button.setObjectName("reset_button")
        self.reset_button.clicked.connect(self.reset_covid)

        #data_table
        self.data_table = QtWidgets.QTableWidget(self.centralwidget)
        self.data_table.setGeometry(QtCore.QRect(10, 150, 441, 141))
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(4)
        self.data_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(3, item)

        #progress bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 770, 961, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximum(100)

        # plot type combo
        self.plot_type = QtWidgets.QComboBox(self.centralwidget)
        self.plot_type.setGeometry(QtCore.QRect(850, 120, 111, 22))
        self.plot_type.setObjectName("plot_type")
        self.plot_type.addItem("")
        self.plot_type.addItem("")
        self.plot_type.addItem("")
        self.plot_type.addItem("")


        #dark_light combo
        self.dark_light = QtWidgets.QComboBox(self.centralwidget)
        self.dark_light.setGeometry(QtCore.QRect(850, 90, 111, 22))
        self.dark_light.setObjectName("dark_light")
        self.dark_light.addItem("")
        self.dark_light.addItem("")
        self.dark_light.currentIndexChanged.connect(self.mode_change)

        #animated checkbox
        self.animated_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.animated_checkbox.setGeometry(QtCore.QRect(870, 300, 101, 20))
        self.animated_checkbox.setObjectName("animated_checkbox")
        #self.animated_checkbox.stateChanged.connect(self.check_box_state_change)
        # simple horizontal line
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 290, 951, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # history log box
        self.text_holder = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_holder.setGeometry(QtCore.QRect(465, 151, 371, 141))
        self.text_holder.setObjectName("text_holder")

        # main label
        self.main_label = QtWidgets.QLabel(self.centralwidget)
        self.main_label.setGeometry(QtCore.QRect(400, 30, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Jokerman")
        font.setPointSize(14)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")

        # history label
        self.history_label = QtWidgets.QLabel(self.centralwidget)
        self.history_label.setGeometry(QtCore.QRect(500, 130, 71, 16))
        self.history_label.setObjectName("history_label")

        # data label
        self.data_label = QtWidgets.QLabel(self.centralwidget)
        self.data_label.setGeometry(QtCore.QRect(10, 130, 71, 16))
        self.data_label.setObjectName("data_label")

        CovidTracker.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CovidTracker)
        self.statusbar.setObjectName("statusbar")
        CovidTracker.setStatusBar(self.statusbar)

        self.retranslateUi(CovidTracker)
        self.plot_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CovidTracker)

        self.df = df_covid_2019
        self.country_list = self.df['countriesAndTerritories']
        self.color_list = ((255,255,255),(255,0,0),(0,255,0),
        (0,0,255),(255,255,0),(0,255,255),(255,0,255))
        self.num_iter = 0
        self.data_table_num=0
        self.start_covid()
        
    def retranslateUi(self, CovidTracker):
        _translate = QtCore.QCoreApplication.translate
        CovidTracker.setWindowTitle(_translate("CovidTracker", "Covid Tracker"))
        self.plot_tab.setTabText(self.plot_tab.indexOf(self.tab), _translate("CovidTracker", "Plot 1"))
        self.plot_tab.setTabText(self.plot_tab.indexOf(self.tab_2), _translate("CovidTracker", "Plot 2"))
        #self.plot_tab.setTabText(self.plot_tab.indexOf(self.tab_3), _translate("CovidTracker", "Chart"))
        self.track_button.setText(_translate("CovidTracker", "Track!"))
        self.speak_button.setText(_translate("CovidTracker", "Speak!"))
        self.reset_button.setText(_translate("CovidTracker", "Reset!"))
        self.plot_type.setItemText(0, _translate("CovidTracker", "Infections"))
        self.plot_type.setItemText(1, _translate("CovidTracker", "deaths_weekly"))
        self.plot_type.setItemText(2, _translate("CovidTracker", "Cumulative"))
        self.plot_type.setItemText(3, _translate("CovidTracker", "Comparison"))
        self.dark_light.setItemText(0, _translate("CovidTracker", "Dark"))
        self.dark_light.setItemText(1, _translate("CovidTracker", "Light"))
        # item = self.data_table.horizontalHeaderItem(0)
        # item.setText(_translate("CovidTracker", "Date"))
        # item = self.data_table.horizontalHeaderItem(1)
        # item.setText(_translate("CovidTracker", "Number"))
        # item = self.data_table.horizontalHeaderItem(2)
        # item.setText(_translate("CovidTracker", "Date"))
        # item = self.data_table.horizontalHeaderItem(3)
        # item.setText(_translate("CovidTracker", "Number"))
        self.animated_checkbox.setText(_translate("CovidTracker", "Animated"))
        self.main_label.setText(_translate("CovidTracker", "COVID-19 Tracker"))
        self.history_label.setText(_translate("CovidTracker", "History Log :"))
        self.data_label.setText(_translate("CovidTracker", "Data"))

    def covid_plot(self):
        ui.progressBar.setValue(0)
        self.num_iter = self.num_iter+1
        self.data_table_num = self.data_table_num+2
        if self.num_iter > 6:
            self.num_iter =0
        self.country_input = self.country_name.text()
        if self.country_input == None or self.country_input == '' or self.country_input == 'None Selected':
            self.country_input = random.choice(np.array(self.country_list))
        self.country_input = self.country_input.replace(' ','_')
        
        if self.country_input in set(self.country_list):
            pass
        else:
            self.text_holder.append('Country Not found. Choosing Random Country.')
            self.country_input = random.choice(np.array(self.country_list))
        self.country_name.setText(self.country_input.replace('_',' '))
        self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Selected country is '+self.country_input)
        self.cases_weekly = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['cases_weekly'])[::-1]
        self.dates = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['dateRep'])[::-1]
        self.deaths_weekly = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['deaths_weekly'])[::-1]
        self.cumulative = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['notification_rate_per_100000_population_14-days'])[::-1]
        
        if self.plot_type.currentIndex() == 0:
            
            #main_plot
            axis_bottom = self.graphicsView.getAxis('bottom')
            self.graphicsView.addLegend()
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting Infections')
            self.graphicsView.clear()
            self.x_cases_weekly = np.arange(0,len(self.cases_weekly))
            axis_bottom = self.graphicsView.getAxis('bottom')
            axis_bottom.setTicks([[(i,j) for i,j in zip(self.x_cases_weekly[0:len(self.x_cases_weekly):20],self.dates[0:len(self.cases_weekly):20])],[(i,'') for j,i in enumerate(self.x_cases_weekly[0:len(self.cases_weekly):10])]])

            self.graphicsView.plot(self.x_cases_weekly,self.cases_weekly,pen=pg.mkPen(color=(255,0,0),width=2),name='cases_weekly in '+self.country_input,symbol='o',
            symbolSize=7,symbolBrush=(255,0,0))
            ui.progressBar.setValue(100)
            #data_table
            
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('cases_weekly('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-2)
            for i in range(len(self.cases_weekly)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.cases_weekly[i])))

            #second_plot
            color = self.color_list[self.num_iter]
            axis_bottom1 = self.graphicsView_2.getAxis('bottom')
            axis_bottom1.setTicks([[(i,j) for i,j in zip(self.x_cases_weekly[0:len(self.x_cases_weekly):20],self.dates[0:len(self.cases_weekly):20])],[(i,'') for j,i in enumerate(self.x_cases_weekly[0:len(self.cases_weekly):10])]])
            self.graphicsView_2.addLegend()
            self.graphicsView_2.plot(self.x_cases_weekly,self.cases_weekly,pen=pg.mkPen(color=color,width=2),name='cases_weekly in '+self.country_input,symbol='o',symbolBrush=color)
        
        if self.plot_type.currentIndex() == 1:

            #main plot
            self.graphicsView.addLegend()
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting deaths_weekly')
            self.graphicsView.clear()
            self.x_deaths_weekly = np.arange(0,len(self.deaths_weekly))

            axis_bottom = self.graphicsView.getAxis('bottom')
            axis_bottom.setTicks([[(i,j) for i,j in zip(self.x_deaths_weekly[0:len(self.x_deaths_weekly):20],self.dates[0:len(self.deaths_weekly):20])],[(i,'') for j,i in enumerate(self.x_deaths_weekly[0:len(self.deaths_weekly):10])]])
            
            self.graphicsView.plot(self.x_deaths_weekly,self.deaths_weekly,pen=pg.mkPen(color=(200,200,200), width=2),name='deaths_weekly in '+self.country_input,symbol='o',
            symbolSize=7,symbolBrush=(200,200,200))
            ui.progressBar.setValue(100)
            #data_table
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('deaths_weekly('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-2)
            for i in range(len(self.deaths_weekly)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.deaths_weekly[i])))
            
            #second plot
            color = self.color_list[self.num_iter]
            axis_bottom1 = self.graphicsView_2.getAxis('bottom')
            axis_bottom1.setTicks([[(i,j) for i,j in zip(self.x_deaths_weekly[0:len(self.x_deaths_weekly):20],self.dates[0:len(self.deaths_weekly):20])],[(i,'') for j,i in enumerate(self.x_deaths_weekly[0:len(self.deaths_weekly):10])]])
            self.graphicsView_2.addLegend()
            self.graphicsView_2.plot(self.x_deaths_weekly,self.deaths_weekly,pen=pg.mkPen(color=color,width=2),name='deaths_weekly in '+self.country_input,symbol='o',symbolBrush=color)
        
        if self.plot_type.currentIndex() == 2:

            #main plot
            self.graphicsView.addLegend()
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting Cumulative Average of 14 days per 100000 cases_weekly')
            self.graphicsView.clear()
            self.x_cumulative = np.arange(0,len(self.cumulative))

            axis_bottom = self.graphicsView.getAxis('bottom')
            axis_bottom.setTicks([[(i,j) for i,j in zip(self.x_cumulative[0:len(self.x_cumulative):20],self.dates[0:len(self.cumulative):20])],[(i,'') for j,i in enumerate(self.x_cumulative[0:len(self.cumulative):10])]])
            self.graphicsView.plot(self.x_cumulative,self.cumulative,pen=pg.mkPen(color=(0,0,255),width=2),name='Cumulative in '+self.country_input,symbol='o',
            symbolSize=7,symbolBrush=(0,255,255))
            ui.progressBar.setValue(100)
            #data_table
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('Cumulative('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-2)
            for i in range(len(self.cumulative)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.cumulative[i])))

            #second plot
            color = self.color_list[self.num_iter]
            axis_bottom1 = self.graphicsView_2.getAxis('bottom')
            axis_bottom1.setTicks([[(i,j) for i,j in zip(self.x_cumulative[0:len(self.x_cumulative):20],self.dates[0:len(self.cumulative):20])],[(i,'') for j,i in enumerate(self.x_cumulative[0:len(self.cumulative):10])]])
            self.graphicsView_2.addLegend()
            self.graphicsView_2.plot(self.x_cumulative,self.cumulative,pen=pg.mkPen(color=color,width=2),name='Cumulative in '+self.country_input,symbol='o',symbolBrush=color)

        if self.plot_type.currentIndex() == 3:
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting comparison')
            self.graphicsView.clear()
            self.graphicsView.addLegend()
            self.x_cases_weekly = np.arange(0,len(self.cases_weekly))
            self.graphicsView.showGrid(x=True,y=True)

            axis_bottom = self.graphicsView.getAxis('bottom')
            axis_bottom.setTicks([[(i,j) for i,j in zip(self.x_cases_weekly[0:len(self.x_cases_weekly):20],self.dates[0:len(self.cases_weekly):20])],[(i,'') for j,i in enumerate(self.x_cases_weekly[0:len(self.cases_weekly):10])]])
            
            self.graphicsView.plot(self.x_cases_weekly,abs(self.cases_weekly),pen=(255,0,0),name='cases_weekly in '+self.country_input,symbol='o',
            symbolSize=7,symbolBrush=(255,0,0))
            self.graphicsView.plot(self.x_cases_weekly,abs(self.deaths_weekly),pen=(200,200,200),name='deaths_weekly in '+self.country_input,symbol='o',
            symbolSize=7,symbolBrush=(200,200,200))
            self.graphicsView.plot(self.x_cases_weekly,abs(self.cumulative),pen=(0,0,255),name='Cumulative in '+self.country_input,symbol='o',
            symbolSize=7,symbolBrush=(0,0,255))
            ui.progressBar.setValue(100)

            #data_table
            self.data_table_num = self.data_table_num+2
            self.data_table.insertColumn(self.data_table_num-4)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-4,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-3)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-3,QtWidgets.QTableWidgetItem('cases_weekly('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('deaths_weekly('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('Cumulative('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-4)
            for i in range(len(self.cumulative)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-4,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-3,QtWidgets.QTableWidgetItem(str(self.cases_weekly[i])))
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.deaths_weekly[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.cumulative[i])))
            #self.graphicsView.setLogMode(x=False,y=True)
        
        # if self.plot_type.currentIndex() == 4:
        #     self.graphicsView_3.clear()
        #     win = self.graphicsView_3
        #     pg.setConfigOptions(antialias=True)
            
        #     p1 = win.addPlot(title='cases_weekly')
            
        #     self.x_cases_weekly = np.arange(0,len(self.cases_weekly))
        #     p1.plot(self.x_cases_weekly,self.cases_weekly,pen=pg.mkPen(color=(255,0,0),width=2),name='cases_weekly in '+self.country_input,symbol='o',
        #     symbolSize=7,symbolBrush=(255,0,0))

        #     p2 = win.addPlot(title='deaths_weekly')
        #     self.x_deaths_weekly = np.arange(0,len(self.deaths_weekly))
        #     p2.plot(self.x_deaths_weekly,self.deaths_weekly,pen=pg.mkPen(color=(200,200,200), width=2),name='deaths_weekly in '+self.country_input,symbol='o',
        #     symbolSize=7,symbolBrush=(200,200,200))

        #     p3 = win.addPlot(title='Cumulative Average')
        #     self.x_cumulative = np.arange(0,len(self.cumulative))
        #     p3.plot(self.x_cumulative,self.cumulative,pen=pg.mkPen(color=(0,0,255),width=2),name='Cumulative in '+self.country_input,symbol='o',
        #     symbolSize=7,symbolBrush=(0,255,255))
        #     win.nextRow()

        #     p4 = win.addPlot(title = 'Covid Histogram')
        #     y1,x1 = np.histogram(np.hstack(self.cases_weekly),bins=int(len(self.cases_weekly)/10))
        #     p4.plot(x1,y1,stepMode=True, fillLevel=1, fillOutline=True, brush=(255,0,0,150))

    def covid_plot_anim(self):
        ui.progressBar.setValue(0)
        self.num_iter = self.num_iter+1
        if self.num_iter > 6:
            self.num_iter =0
        self.data_table_num = self.data_table_num+2
        self.country_input = self.country_name.text()
        if self.country_input == None or self.country_input == '':
            self.country_input = random.choice(np.array(self.country_list))
        self.country_input = self.country_input.replace(' ','_')
        
        if self.country_input in set(self.country_list):
            pass
        else:
            self.text_holder.append('Country Not found. Choosing Random Country.')
            self.country_input = random.choice(np.array(self.country_list))
        self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Selected country is '+self.country_input)
        self.cases_weekly = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['cases_weekly'])[::-1]
        self.dates = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['dateRep'])[::-1]
        self.deaths_weekly = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['deaths_weekly'])[::-1]
        self.cumulative = np.array(self.df[self.df['countriesAndTerritories']==self.country_input]['notification_rate_per_100000_population_14-days'])[::-1]
        self.graphicsView.clear()

        if self.plot_type.currentIndex() == 0:
            
            self.graphicsView.addLegend()
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting Infections')
            self.graphicsView.clear()
            self.x_cases_weekly = np.arange(0,len(self.cases_weekly))
            self.x=[]
            self.y=[]
            #data table
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('deaths_weekly('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-2)
            for i in range(len(self.deaths_weekly)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.deaths_weekly[i])))
            for i in range(len(self.cases_weekly)):
                ui.progressBar.setValue(np.linspace(0,100,len(self.cases_weekly))[i])
                self.graphicsView.clear()
                self.x.append(self.x_cases_weekly[i])
                self.y.append(self.cases_weekly[i])
                self.graphicsView.plot(self.x,self.y,pen=pg.mkPen(color=(255,0,0),width=2),name='cases_weekly in '+self.country_input,symbol='o',
                symbolSize=7,symbolBrush=(255,0,0))
                pg.QtGui.QApplication.processEvents()
            #second_plot
            color = self.color_list[self.num_iter]
            axis_bottom1 = self.graphicsView_2.getAxis('bottom')
            axis_bottom1.setTicks([[(i,j) for i,j in zip(self.x_cases_weekly[0:len(self.x_cases_weekly):20],self.dates[0:len(self.cases_weekly):20])],[(i,'') for j,i in enumerate(self.x_cases_weekly[0:len(self.cases_weekly):10])]])
            self.graphicsView_2.addLegend()
            self.graphicsView_2.plot(self.x_cases_weekly,self.cases_weekly,pen=pg.mkPen(color=color,width=2),name='cases_weekly in '+self.country_input,symbol='o',symbolBrush=color)
        
            
        
        if self.plot_type.currentIndex() == 1:
            self.graphicsView.addLegend()
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting deaths_weekly')
            self.graphicsView.clear()
            self.x_deaths_weekly = np.arange(0,len(self.deaths_weekly))
            self.x=[]
            self.y=[]

            #data_table
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('deaths_weekly('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-2)
            for i in range(len(self.deaths_weekly)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.deaths_weekly[i])))

            #main_anim_plot
            for i in range(len(self.deaths_weekly)):
                ui.progressBar.setValue(np.linspace(0,100,len(self.deaths_weekly))[i])
                self.graphicsView.clear()
                self.x.append(self.x_deaths_weekly[i])
                self.y.append(self.deaths_weekly[i])
                self.graphicsView.plot(self.x,self.y,pen=pg.mkPen(color=(200,200,200), width=2),name='deaths_weekly in '+self.country_input,symbol='o',
                symbolSize=7,symbolBrush=(200,200,200))
                pg.QtGui.QApplication.processEvents()
            
            #second plot
            color = self.color_list[self.num_iter]
            axis_bottom1 = self.graphicsView_2.getAxis('bottom')
            axis_bottom1.setTicks([[(i,j) for i,j in zip(self.x_deaths_weekly[0:len(self.x_deaths_weekly):20],self.dates[0:len(self.deaths_weekly):20])],[(i,'') for j,i in enumerate(self.x_deaths_weekly[0:len(self.deaths_weekly):10])]])
            self.graphicsView_2.addLegend()
            self.graphicsView_2.plot(self.x_deaths_weekly,self.deaths_weekly,pen=pg.mkPen(color=color,width=2),name='deaths_weekly in '+self.country_input,symbol='o',symbolBrush=color)

        if self.plot_type.currentIndex() == 2:
            self.graphicsView.addLegend()
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting Cumulative Average of 14 days per 100000 cases_weekly')
            self.graphicsView.clear()
            self.x_cumulative = np.arange(0,len(self.cumulative))
            self.x=[]
            self.y=[]
            #data_table
            self.data_table.insertColumn(self.data_table_num-2)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-2,QtWidgets.QTableWidgetItem('Date('+self.country_input+')'))
            self.data_table.insertColumn(self.data_table_num-1)
            self.data_table.setHorizontalHeaderItem(self.data_table_num-1,QtWidgets.QTableWidgetItem('Cumulative('+self.country_input+')'))
            self.data_table.setCurrentCell(0,self.data_table_num-2)
            for i in range(len(self.cumulative)):
                
                rowPosition = self.data_table.rowCount()
                self.data_table.insertRow(rowPosition)
                self.data_table.setItem(i,self.data_table_num-2,QtWidgets.QTableWidgetItem(str(self.dates[i])))
                self.data_table.setItem(i,self.data_table_num-1,QtWidgets.QTableWidgetItem(str(self.cumulative[i])))

            for i in range(len(self.cumulative)):
                ui.progressBar.setValue(np.linspace(0,100,len(self.cumulative))[i])
                self.graphicsView.clear()
                self.x.append(self.x_cumulative[i])
                self.y.append(self.cumulative[i])
                self.graphicsView.plot(self.x,self.y,pen=pg.mkPen(color=(0,0,255),width=2),name='Cumulative in '+self.country_input,symbol='o',
                symbolSize=7,symbolBrush=(0,255,255))
                pg.QtGui.QApplication.processEvents()

        if self.plot_type.currentIndex() == 3:
            
            self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting comparison. No animation.')
            self.graphicsView.clear()
            self.graphicsView.addLegend()
            self.x_cases_weekly = np.arange(0,len(self.cases_weekly))
            self.graphicsView.showGrid(x=True,y=True)
            self.graphicsView.plot(self.x_cases_weekly,abs(self.cases_weekly),pen=(255,0,0),name='cases_weekly',symbol='o',
            symbolSize=7,symbolBrush=(255,0,0))
            self.graphicsView.plot(self.x_cases_weekly,abs(self.deaths_weekly),pen=(200,200,200),name='deaths_weekly',symbol='o',
            symbolSize=7,symbolBrush=(200,200,200))
            self.graphicsView.plot(self.x_cases_weekly,abs(self.cumulative),pen=(0,0,255),name='Cumulative',symbol='o',
            symbolSize=7,symbolBrush=(0,0,255))
            ui.progressBar.setValue(100)
            #self.graphicsView.setLogMode(x=False,y=True)
        
        if self.plot_type.currentIndex() == 4:
            self.x_cases_weekly = np.arange(0,len(self.cases_weekly))
            self.graphicsView.plot(self.x_cases_weekly,self.cases_weekly)
        
    def get_covid(self):
        if self.animated_checkbox.checkState()==False:
            self.covid_plot()
        else:
            self.covid_plot_anim()

    def reset_covid(self):
        self.text_holder.setText('')
        self.graphicsView.clear()
        self.graphicsView_2.clear()
        self.data_table.clear()
        self.data_table_num = 0
        self.num_iter = 0
        self.animated_checkbox.setCheckState(False)
        self.country_name.setText('None Selected')
        self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Covid Tracker reset!')

    def start_record(self):
        self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+': \n>>>>>><<<<<<\nVoice mode activated\n>>>>>><<<<<<\nListening for 5 seconds....')
        self.text_holder.repaint()
        self.record_covid()
        self.text_holder.append('Voice mode deactivated.')

    def record_covid(self):
        
        df = df_covid_2019
        
        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

        sd.wait()  # Wait until recording is finished
        y = (np.iinfo(np.int32).max * (myrecording/np.abs(myrecording).max())).astype(np.int32)

        wavfile.write('output.wav', fs, y)
        r = sr.Recognizer()
        
        # Reading Audio file as source
        # listening the audio file and store in audio_text variable

        with sr.AudioFile('output.wav') as source:
            
            audio_text = r.listen(source)
            
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
                
                # using google speech recognition
                text = r.recognize_google(audio_text)
                self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+": I guess you said '"+text+"'")
             
            except:
                self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+': Sorry, the speech transcription service did not respond, Try again in a few minutes or type the country name.')

            try:

                if text == None:
                    self.text_holder.append('Nothin recorded')
                if text.lower() == 'infections':
                    self.plot_type.setCurrentIndex(0)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Selecting plot type > Infections')
                elif text.lower() == 'deaths_weekly' or text.lower() == 'death':
                    self.plot_type.setCurrentIndex(1)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Selecting plot type > deaths_weekly')
                elif text.lower() == 'cumulative':
                    self.plot_type.setCurrentIndex(2)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Selecting plot type > Cumulative')
                elif text.lower() == 'comparison' or text.lower()=='comparisons':
                    self.plot_type.setCurrentIndex(3)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Selecting plot type > Comparison')
                elif text.lower() == 'chart':
                    self.plot_type.setCurrentIndex(4)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Selecting plot type > Chart')
                elif text.lower() == 'reset':
                    self.reset_button.click()
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Reset Covid Tracker')
                elif text.lower() == 'dark':
                    self.dark_light.setCurrentIndex(0)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Setting Dark Mode')
                elif text.lower() == 'light':
                    self.dark_light.setCurrentIndex(1)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Setting Light Mode')
                elif text.lower()=='animated':
                    self.animated_checkbox.setCheckState(True) 
                else:
                    self.country_name.setText(text)
                    self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : From voice commands : Country selected > ' +text)
                    country_name = text.replace(' ','_')
                    if country_name in set(self.df['countriesAndTerritories']):
                        self.track_button.click()
            except UnboundLocalError:
                self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+': Nothing was recorded')

    def mode_change(self):
        if self.dark_light.currentIndex() == 0:
            
            app.setStyle('Fusion')
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
            palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
            palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
            palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
            palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
                 
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 67, 202 ,200).lighter())
            palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            app.setPalette(palette)

        if self.dark_light.currentIndex() == 1:
            app.setStyle('Fusion')
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255,255,255))
            palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255,255,255))
            palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(246,246,246))
            palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.black)
            palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
                 
            palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 67, 202 ,200).lighter())
            palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            app.setPalette(palette)
    # def check_box_state_change(self):
    #     self.text_holder.append('Animation toggled')
    #     if self.animated_checkbox.checkState()== True:
    #         self.remove_item()
    #     if self.animated_checkbox.checkState()==False and self.plot_type.itemText(3)!='Comparison':
    #         self.add_item()
    # def remove_item(self):
    #     self.plot_type.removeItem(3)
    #     self.plot_type.repaint()
    # def add_item(self):
    #     self.plot_type.insertItem(3,'Comparison')
        # self.plot_type.repaint()

    def start_covid(self):
        

        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            data = json.loads(url.read().decode())
            self.country_name.setText(str(data['country_name']))
        self.get_covid()
        self.text_holder.setText(datetime.datetime.now().strftime("%I:%M:%S")+' : Country Located : '+self.country_name.text())
        self.text_holder.append(datetime.datetime.now().strftime("%I:%M:%S")+' : Plotting infections')
        self.country_name.setText('None Selected')
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CovidTracker = QtWidgets.QMainWindow()
    ui = Ui_CovidTracker()
    ui.setupUi(CovidTracker)
    if 7 < datetime.datetime.now().hour <19 :
        ui.dark_light.setCurrentIndex(1)
        ui.mode_change()
    else:
        ui.dark_light.setCurrentIndex(0)
        ui.mode_change()
    CovidTracker.show()
    sys.exit(app.exec_())
