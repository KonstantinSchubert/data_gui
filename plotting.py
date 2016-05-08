"""Methods and functions needed to make the plot
"""

def cut_outliers(series):
    """ Removes outliers from given series

    We define an upper outlier as a data point which is more than 
    n times as far away from the 95 percent quantile than the 90 percent quantile, where n is 
    a tuning parameter. Lower outliers are defined analogously.

    TODO: test and debug!
    """

    quantile5 = np.percentile(series.values, 5)
    quantile10 = np.percentile(series.values, 10)
    quantile90 = np.percentile(series.values, 90)
    quantile95 = np.percentile(series.values, 95)

    def is_outlier(point):
    	if (quantile5 - point) > (n * quantile10 - quantile5):
    		return true
    	if (point - quantile95) > (n * quantile95 - quantile90):
    		return true
    	return false
   	return series[~series.applymap(is_outlier)]
