import seaborn as sns
import pandas as pd
import xarray as xr
import datetime
import numpy as np
import os
import dateutil.parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

path = os.getcwd()

def plot_metrics(df, height, typ):
    daily_mean=df.groupby("time.date").mean(dim='time')
    daily_std=df.groupby("time.date").std(dim='time')
    #daily_std=df.resample(time="1D").std(dim='time')
    daily_std["date"]=pd.to_datetime(daily_std.date)
    daily_mean["date"]=pd.to_datetime(daily_mean.date)
    #daily_std.sel(daily_std.groupby("date.month")==1)
    for m_name, metric in zip(["mean", "variability"],[daily_mean, daily_std]):
    #for m_name, metric in zip(["variability"],[daily_std]):
        month_idxs = metric.groupby('date.month').groups
        list_of_metrics = [metric.isel(date=idxs) for idxs in month_idxs.values()]
        # list_of_metrics = [metric.isel(date=idxs)[variable] for idxs in month_idxs.values()]
        plt.figure(figsize=(8,6))
        sns.boxplot(data=list_of_metrics)
        plt.title(f"{typ} monthly aggregated daily windspeed {m_name} at {height}m (Cabauw)")
        if "mean" in m_name:
            plt.ylim([0,20])
        else:
            plt.ylim([0,6])
        plt.ylabel("wind [m/s]")
        plt.xlabel("month index")
        plt.savefig(os.path.join(path, f"{typ}_mon_aggr_day_wind_{m_name}_{height}.png"))