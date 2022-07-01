from wind2power import wind2power
import xarray as xr
import matplotlib.pylab as plt
import numpy as np
import dask.array as da

## Parameters
# station = 25 ## Burgos
station = 12 ## Cabauw
date_ini = '2020-01-01'
date_end = '2022-01-01'
level = 133
type = 'high-wind'

for res in ["2.8km", "4km", "9km"]:
    ## Each of the 3IFS runs (2.8km.4km,9km) is stored in one zarr
    ds = xr.open_zarr(f'/work/bm1235/a270046/cycle2-sync/ddh_output/{res}') ## xarray Dataset
    # ds_icon = xr.open_zarr('/work/bm1235/k203123/experiments/ngc2009/outdata/ngc2009_mtgrm.zarr')
    model = f"IFS{res}"
    print(model)
    ## Here all the 30 station names and locations:
    city = list(zip(ds.station_name.values,ds.station.values,ds.lat.values,ds.lon.values))[station]

    ## it is best to select the station of interest first, and other limits in dimensions
    u_station = ds.u.sel(time = slice(date_ini,date_end), station = station, level = level)
    v_station = ds.v.sel(time = slice(date_ini,date_end), station = station, level = level)
    wind_station = np.sqrt(u_station**2 + v_station**2)

    from validation_plots import plot_metrics
    if res == "2.8km":
        wind_station = wind_station[::4]
    elif res == "4km":
        wind_station = wind_station[::3]
    else:
        wind_station = wind_station[:]
    plot_metrics(wind_station, f"lvl{level}", model)

ds_icon = xr.open_zarr('/work/bm1235/k203123/experiments/ngc2009/outdata/ngc2009_mtgrm.zarr')
res="5km"
model = f"ICON{res}"
print(model)
## Here all the 30 station names and locations:

u_station = ds_icon.u.isel(station=station, level=-2)
v_station = ds_icon.u.isel(station=station, level=-2)
## it is best to select the station of interest first, and other limits in dimensions
wind_station = np.sqrt(u_station**2 + v_station**2)

from validation_plots import plot_metrics
if res == "5km":
    wind_station = wind_station[::4]
else:
    wind_station = wind_station[:]
plot_metrics(wind_station, f"lvl{level}", model)


## Wind to Power
#power = xr.apply_ufunc(wind2power, wind_station, input_core_dims = [0])
#power_func = da.gufunc(wind2power, signature='(i)->()', output_dtypes=float, axis=0)
#power = power_func(da.asarray([wind_station])).compute()
#power = [wind2power(wind = point, type = type) for point in wind_station]
# power = wind2power(wind = wind_station, type = type)

# ## Select and plot sw rad at surface for first 10 days of august
# plt.figure(figsize=(15,10))
# plt.plot(wind_station.time, wind_station)
# plt.title('Wind speed - City: ' + str(city[0]) + ' (' + str(city[1]) + 'ºN' + '; ' + str(city[2]) + 'ºE)')
# plt.savefig('./wind.png')

# ## Select and plot sw rad at surface for first 10 days of august
# plt.figure(figsize = (15,10))
# plt.plot(wind_station.time, power)
# plt.title('Wind power - City: ' + str(city[0]) + ' (' + str(city[1]) + 'ºN' + '; ' + str(city[2]) + 'ºE)')
# plt.savefig('./power.png')
