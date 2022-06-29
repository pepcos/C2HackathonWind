import numpy as np

def wind2power(wind, type):
    
    ## wind in m/s
    ## type must be 'high-wind' or 'low-wind'
    
    if type == 'high-wind':
        xp = [3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,25,25.5]
        fp = [0.002,0.015,0.036,0.060,0.090,0.124,0.164,0.212,0.269,0.333,0.406,0.489,0.581,0.681,0.781,0.873,0.943,0.982,0.996,0.999,1.000,1.000,0.000]
    elif type == 'low-wind':
        xp = [3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,21.5,22]
        fp = [0.023,0.050,0.083,0.123,0.174,0.236,0.310,0.396,0.498,0.612,0.738,0.870,0.994,1.094,1.163,1.197,1.213,1.217,1.217,0.000]
    else:
        raise ValueError('type must be "high-wind" or "low-wind"')
    
    power = np.interp(x = wind, xp = xp, fp = fp, left = 0, right = 0)
    
    return power
