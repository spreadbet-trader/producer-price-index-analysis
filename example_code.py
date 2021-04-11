"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

import requests
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from dateutil import parser
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
from numpy import NaN, Inf
from datetime import datetime
from fake_useragent import UserAgent
import pprint
import sys

"""######################################
######################################
######################################
"""

mpl.rc('axes', labelsize=6, titlesize=6)
plt.rcParams.update({'font.size': 6})
pp = pprint.PrettyPrinter(indent=4)
ua = UserAgent()
headers = {'User-Agent': ua.random, }

"""######################################
######################################
######################################
"""


def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    v = np.asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return maxtab, mintab


dataset_urls = [
    "https://www.quandl.com/api/v3/datasets/FRED/PCU33123312.json",
    "https://www.quandl.com/api/v3/datasets/FRED/PPIACO.json",
    "https://www.quandl.com/api/v3/datasets/FRED/PCU331110331110P.json",
    "https://www.quandl.com/api/v3/datasets/FRED/PCU331110331110D.json"]


for each_dataset in dataset_urls:
    _YearValue = []
    _DataPointValue = []

    r = requests.get(
        each_dataset,
        headers=headers)
    parsed = json.loads(r.text)
    line_label = str(parsed["dataset"]["name"])

    for each in parsed["dataset"]["data"]:
        if each[0] is not None and each[1] is not None:
            date_time = parser.parse(str(each[0]))
            _YearValue.append(date_time)
            _DataPointValue = list(_DataPointValue)
            _DataPointValue.append(float(each[1]))

    _YearValue.reverse()
    _DataPointValue.reverse()

    _DataPointValue = np.asarray(_DataPointValue)

    print("###########PEAKS---->" + str(line_label) + "###########")
    print("###########PEAKS---->" + str(line_label) + "###########")
    print("###########PEAKS---->" + str(line_label) + "###########")

    peaks, _ = peakdet(_DataPointValue, 3)
    # peaks, _ = find_peaks(_DataPointValue, height=0) #alternative
    for each in peaks:
        plt.scatter(_YearValue[each[0]], each[1], marker='o')
        print(_YearValue[each[0]].strftime('%Y-%m-%d'))
        plt.text(_YearValue[each[0]], each[1], s=str(
            _YearValue[each[0]].strftime('%Y-%m-%d')), rotation=45)

    plt.plot(_YearValue, _DataPointValue, label=line_label)
    """##########
    #smoothing
    ##########"""
    # plt.plot(_YearValue, savgol_filter(_DataPointValue, 11, 4, mode='mirror'))
    # plt.plot(_YearValue, savgol_filter(_DataPointValue, 11 , 4, mode='nearest'))
    # plt.plot(_YearValue, savgol_filter(_DataPointValue, 11 , 4, mode='constant'))
    # plt.plot(_YearValue, savgol_filter(_DataPointValue, 11 , 4, mode='wrap'))

plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.autoscale(enable=True, axis='both')
plt.tight_layout()
plt.grid()
plt.text(
    1,
    1,
    "Graph Created from https://github.com/spreadbet-trader/producer-price-index-analysis",
    fontsize=12)
plt.title(
    "Producer Price Index Graph",
    fontsize=12)
# output_name = "graph_" + str(dt_string) + ".png"
# plt.savefig(output_name, dpi=600, format="png")
plt.show()
