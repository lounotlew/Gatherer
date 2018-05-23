###########################################################################################
# Gatherer.                                                                               #
# Written by Lewis Kim.                                                                   #
# A simple way to collect time-series data based on any category.                         #
# Easily visualize the pandas dataframe within the applet, and                            #
# visualize the trend of the data vs. time.                                               #
# Also includes ARIMA Forecasting (based on ARIMA(1, 0, 1), but the meaningfulness of.    #
# the predictions depends on what the data represents, and it is highly recommended       #
# that you use forecasting with daily data, and not monthly or annual data.               #
###########################################################################################

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import pandas as pd
from pandas import Series
from pandastable import Table, TableModel

import numpy as np
import math
import os
from datetime import datetime

from statsmodels.tsa.stattools import acf, pacf
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA


# Main GUI class for Gatherer.
class Gatherer:

	def __init__(self, master):
		self.master = master
		self.currentData = pd.DataFrame([] ,columns = ["Entry", "Date"])   # Data Frame. Current dataset. Initialized as an empty data frame, with defined columns.
		self.currentDataName = ""         # String. Name of the current dataset.
		self.filepath = ""                # String. Filepath of the current dataset.
		self.numEntries = 0               # Integer. Number of entries (rows) in current dataset.
		self.createdNew = False           # Boolean. True if user created a new dataset.
		self.loaded = False               # Boolean. True if user loaded an existing dataset.

		# Frames for widgets below.		
		frame1 = Frame(master)
		frame2 = Frame(master)
		frame3 = Frame(master)
		frame4 = Frame(master)
		frame1.pack(side = TOP)
		frame2.pack()
		frame3.pack()
		frame4.pack()

		# Button for creating a new dataset.
		self.createDataset = Button(frame1, text = "Create New Dataset", command = self.create_new)
		self.createDataset.grid(row = 0)

		# Button for loading in an existing dataset, found as a pickle (.gz) in /data.
		self.loadDataset = Button(frame1, text = "Load an Existing Dataset", command = self.load_file)
		self.loadDataset.grid(row = 1)

		# Label for the name of the current dataset; the name of a dataset is the file name (NAME.gz).
		self.datalabel = Label(frame1, text = "Your Current Dataset: " + self.currentDataName)
		self.datalabel.grid(row = 2)

		# Label for the number of entries in the current dataset. Number of entries = len(self.currentData).
		self.entrylabel = Label(frame1, text = "Current Number of Entries: " + str(self.numEntries))
		self.entrylabel.grid(row = 3)

		# Label for data entry.
		self.label1 = Label(frame2, text = "Entry (Must be Numeric):")
		self.label1.grid(row = 0, column = 0)

		# Label for date entry.
		self.label1 = Label(frame2, text = "Date (MM-DD-YYYY):")
		self.label1.grid(row = 1, column = 0)

		# Entry field for datum.
		self.valEntry = Entry(frame2)
		self.valEntry.grid(row = 0, column = 1)

		# Entry field for the date associated with the datum.
		self.dateEntry = Entry(frame2)
		self.dateEntry.grid(row = 1, column = 1)

		# Button for adding the information in valEntry and dateEntry to self.currentData.
		# If either valEntry or dateEntry is empty, or has invalid inputs (see associated functions), it throws an error.
		self.addButton = Button(frame2, text = "Add to Current Dataset", command = self.addToCurrentDF)
		self.addButton.grid(row = 2, column  = 0)

		# Button for removing the last entry 
		# If self.currentData is empty, it throws an error.
		self.removeButton = Button(frame2, text = "Remove Last Entry", command = self.removeLastEntry)
		self.removeButton.grid(row = 2, column = 1)

		# Button for displaying the current data frame (self.currentData) in a new window using pandastable.
		self.showDFButton = Button(frame3, text = "Display Data Frame", command = self.showDF)
		self.showDFButton.grid(row = 3, column = 0)

		# Button for visualizing the trend in self.currentData (with date as the x-axis) using matplotlib.
		self.visButton = Button(frame3, text = "Visualize Trend", command = self.visualizeTrend)
		self.visButton.grid(row = 3, column = 1)

		# Button for predicting the next value in self.currentData using Teras (see Predictor.py for more details).
		# Not Yet Implemented.
		self.predictButton = Button(frame3, text = "ARIMA Forecasts (7 Days)", command = self.ARIMAModel)
		self.predictButton.grid(row = 3, column = 2)

		# Button for exporting self.currentData into a .csv file in /export.
		self.exportButton = Button(frame4, text = "Export Dataset to .csv", command = self.exportToCSV)
		self.exportButton.grid(row = 4, column = 0)

		# Button for quitting Gatherer.
		self.quitButton = Button(frame4, text = "Quit Gatherer", command = master.destroy)
		self.quitButton.grid(row = 4, column = 1)

	"""Create a new dataset. self.currentData gets pointed to an empty dataframe (with defined column names),
		and self.filepath gets updated to /data/FILENAME.gz, where FILENAME is the new dataset name given by
		the user."""
	def create_new(self):
		filename = simpledialog.askstring("Create a New Dataset", "New Dataset Name:")
		self.currentData = pd.DataFrame([], columns = ["Entry", "Date"])
		self.numEntries = len(self.currentData)
		self.currentDataName = filename

		self.createdNew = True
		self.loaded = False

		self.filepath = "data/" + filename + ".gz"

		text1 = "Your Current Dataset: " + self.currentDataName
		text2 = "Current Number of Entries: " + str(self.numEntries)

		self.datalabel['text'] = text1
		self.entrylabel['text'] = text2

	"""Load an existing dataset in /data. self.currentData gets pointed to a data frame associated with the selected
		pickle file (.gz), and filepath points to that same pickle file."""
	def load_file(self):
		self.filepath = askopenfilename()
		self.currentData = pd.read_pickle(self.filepath)

		self.loaded = True
		self.createdNew = False

		# Extract the file name from self.filepath (name of the .gz file), and update the current number of entries.
		self.currentDataName = os.path.splitext(str(self.filepath))[0].split('/')[-1]
		self.numEntries = len(self.currentData)
		
		text1 = "Your Current Dataset: " + self.currentDataName
		text2 = "Current Number of Entries: " + str(self.numEntries)

		self.datalabel['text'] = text1
		self.entrylabel['text'] = text2

	"""Update the information in self.dataLabel and self.entryLabel."""
	def updateInfo(self):
		self.numEntries = len(self.currentData)
		text1 = "Your Current Dataset: " + self.currentDataName
		text2 = "Current Number of Entries: " + str(self.numEntries)

		self.datalabel['text'] = text1
		self.entrylabel['text'] = text2

	"""Returns the value in valEntry as a floating number. Throws an error if the input is not numeric."""
	def getEntry(self):
		try:
			return float(self.valEntry.get())
		except:
			showinfo("Error", "Need a numeric entry.")
			return

	"""Returns the value in dateEntry as a time object. Returns an error if the input does not follow the given
		date format, or if the input is invalid (e.g. "hello")."""
	def getDate(self):
		try:
			return datetime.strptime(self.dateEntry.get(), '%m-%d-%Y')
		except:
			showinfo("Error", "Please input a valid date.")
			return

	"""Add the values in valEntry and dateEntry to the current data frame, and writes the data frame
	   into a new .csv."""
	def addToCurrentDF(self):
		if self.getEntry() == None or self.getDate == None:
			return

		elif self.createdNew == False and self.loaded == False:
			showinfo("Error", "You need to create or load a datset first.")
			return

		else:
			try:
				tempDF = pd.DataFrame({'Entry': [self.getEntry()], 'Date': [self.getDate()]})
				self.currentData = self.currentData.append(tempDF)
				self.currentData = self.currentData.reset_index(drop = True)

				self.updateInfo()
				self.currentData.to_pickle(self.filepath)
			except:
				showinfo("Error", "Error")
				return

	"""Remove the last row (last entry) from self.currentData."""
	def removeLastEntry(self):
		if len(self.currentData) == 0:
			showinfo("Error", "Your dataset is empty!")

		else:
			self.currentData = self.currentData[:-1]
			self.currentData = self.currentData.reset_index(drop = True)

			self.updateInfo()
			self.currentData.to_pickle(self.filepath)

	"""Display self.currentData in a new window using pandastable."""
	def showDF(self):
		if len(self.currentData) == 0:
			showinfo("Error", "Your current dataset is empty.")

		else:
			top1 = Toplevel()

			self.table = pt = Table(top1, dataframe = self.currentData)
			pt.show()
			return

	"""Display a graph of Date vs. Entry for self.currentData in a new window using matplotlib."""
	def visualizeTrend(self):
		top2 = Toplevel()

		figure = Figure(figsize = (5, 5), dpi = 100)
		a = figure.add_subplot(111)
		a.plot(self.currentData['Date'], self.currentData['Entry'])

		canvas = FigureCanvasTkAgg(figure, top2)
		canvas.show()
		canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

	"""ARIMA Forecasting based on ARIMA(1, 0, 1). Provides multi-step out-of-sample forecasts, up to 7 days."""
	def ARIMAModel(self):
		if len(self.currentData) == 0:
			showinfo("Error", "Your Dataset is Empty!")
			return

		df = self.currentData.set_index('Date')
		entries = df['Entry']

		def difference(dataset, interval = 1):
			diff = list()
			for i in range(interval, len(dataset)):
				value = dataset[i] - dataset[i - interval]
				diff.append(value)

			return np.array(diff)

		def inverse_difference(history, yhat, interval = 1):
			return yhat + history[-interval]

		differenced = difference(entries, 1)

		model = ARIMA(differenced, order = (1, 0, 1))
		model_fit = model.fit(disp = 0)

		forecast = model_fit.forecast(steps = 7)[0]
		history = [e for e in entries]

		day = 1
		forecast_list = []
		for yhat in forecast:
			inverted = inverse_difference(history, yhat, 1)
			forecast_list.append('Day %d: %f' % (day, inverted))
			history.append(inverted)
			day += 1

		top1 = Toplevel()

		descriptionLabel = Label(top1, text = "ARIMA Forecast Predictions for the Next 7 Days:")
		day1label = Label(top1, text = forecast_list[0])
		day2label = Label(top1, text = forecast_list[1])
		day3label = Label(top1, text = forecast_list[2])
		day4label = Label(top1, text = forecast_list[3])
		day5label = Label(top1, text = forecast_list[4])
		day6label = Label(top1, text = forecast_list[5])
		day7label = Label(top1, text = forecast_list[6])

		descriptionLabel.grid(row = 0)
		day1label.grid(row = 1)
		day2label.grid(row = 2)
		day3label.grid(row = 3)
		day4label.grid(row = 4)
		day5label.grid(row = 5)
		day6label.grid(row = 6)
		day7label.grid(row = 7)

	"""Export self.currentData to a .csv file in /export."""
	def exportToCSV(self):
		if len(self.currentData) == 0:
			showinfo("Error", "Your current dataset is empty!")
			return

		try:
			filename = simpledialog.askstring("Export Dataset", "File Name (without .csv):")
			export_path = "export/" + filename + ".csv"

			self.currentData.to_csv(path_or_buf = export_path, date_format = '%m-%d-%Y')
		except:
			showinfo("error", "error")


root = Tk()
gatherer = Gatherer(root)

while True:
	try:
		root.mainloop()
		break
	except UnicodeDecodeError: # Added to avoid the program crashing when scrolling in 'showDF()'.
		pass
