# Gatherer - A Simple Way to Gather and Analyze Time Series Data
> Applet written by Lewis Kim

### Description

Gatherer is a small-scale ``python`` applet using ``tkinter`` as its GUI framework that collects user-inputed time-series data, and stores it locally as a .gz (pickle) file, with an option to export the dataset to .csv. The data internally stored as a ``pandas`` data frame. Gatherer uses ``pandastable`` (see references) to display the data frame in a new window. Gatherer also uses ``matplotlib`` to display a simple trend graph of Entry vs. Date, which is useful for analyzing the time series' behavior and seasonality. This plot can be used in conjunction with the ARIMA forecasting feature, which uses an ``ARIMA(1, 0, 1)`` model from ``statsmodels`` to produce 7 (days) multi-step out-of-sample forecasts. This forecast feature was built with daily data in mind (based on https://machinelearningmastery.com/make-sample-forecasts-arima-python/), and may not produce meaningful predictions with monthly or annual data (although the ``p, d, q`` parameters can easily be changed). Statistical significances of the 7-day forecasts have not been thoroughly tested, and the model may need adjustments.

For a GUI sample and applet walkthrough, click this [link](gui_sample/README.md).

### Installation

Gatherer was written in Python 3.6, and may not work with Python 2.

Required packages:
- ``tkinter`` (included with Python 3)
- ``matplotlib`` (pip install: ``pip3 install matplotlib``)
- ``pandas`` (pip install: ``pip3 install pandas``)
- ``pandastable`` (pip install: ``pip3 install pandastable``)
- ``scipy``/``numpy`` (pip install: ``pip3 install scipy numpy``)
- ``statsmodels`` (pip install: ``pip3 install statsmodels``)

To run this application (after installing all required packages), type the following command in terminal/bash in the directory inside the Gatherer folder:

```
python3 gatherer.py
```

### References

References to the libraries and packages used in Gatherer:

1) ``tkinter``: https://wiki.python.org/moin/TkInter
2) ``matplotlib``: https://matplotlib.org/gallery/index.html
3) ``pandas``: https://pandas.pydata.org/pandas-docs/stable/
4) ``pandastable``: https://github.com/dmnfarrell/pandastable
5) ``scipy``/``numpy``: https://www.scipy.org/
6) ``statsmodels`` (specifically time series ARIMA): http://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARIMA.html
