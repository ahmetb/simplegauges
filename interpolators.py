# coding: utf-8


def linear(data):
    """Completes data records with missing data (0 or None) using linear
    interpolation. Works only if first and last data points have valid data"""

    data = list(data)
    last_data_pt = 0
    i = 0
    interpolate = False
    for i in range(len(data)):
        dt = data[i]
        if not dt['data']:  # 0 or None
            interpolate = True
        else:
            if interpolate:
                lo_val = data[last_data_pt]['data']
                hi_val = dt['data']
                points = i - last_data_pt - 1
                incr = (1.0 * (hi_val - lo_val)) / (points + 1)

                for j in range(1, points + 1):
                    data[last_data_pt + j]['data'] = lo_val + incr * j
            last_data_pt = i
            interpolate = False
    return data
