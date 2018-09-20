from __future__ import division
import hashlib
import numpy as np
import matplotlib.mlab as mlab
from termcolor import colored
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)
from operator import itemgetter

IDX_FREQ_I = 0
IDX_TIME_J = 1
DEFAULT_FS = 44100
DEFAULT_WINDOW_SIZE = 4096
DEFAULT_OVERLAP_RATIO = 0.5
DEFAULT_FAN_VALUE = 15
DEFAULT_AMP_MIN = 10
PEAK_NEIGHBORHOOD_SIZE = 20
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200
PEAK_SORT = True
FINGERPRINT_REDUCTION = 20

def fingerprint(channel_samples, Fs=DEFAULT_FS,
                wsize=DEFAULT_WINDOW_SIZE,
                wratio=DEFAULT_OVERLAP_RATIO,
                fan_value=DEFAULT_FAN_VALUE,
                amp_min=DEFAULT_AMP_MIN):

    arr2D = mlab.specgram(
        channel_samples,
        NFFT=wsize,
        Fs=Fs,
        window=mlab.window_hanning,
        noverlap=int(wsize * wratio))[0]

    arr2D = 10 * np.log10(replaceZeroes(arr2D))
    arr2D[arr2D == -np.inf] = 0 

    local_maxima = get_2D_peaks(arr2D, amp_min=amp_min)

    return generate_hashes(local_maxima, fan_value=fan_value)

def get_2D_peaks(arr2D, amp_min=DEFAULT_AMP_MIN):
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    detected_peaks = local_max ^ eroded_background
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)
    amps = amps.flatten()
    
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min] 

    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]
    
    return zip(frequency_idx, time_idx)

def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):
    if PEAK_SORT:
      peaks.sort(key=itemgetter(1))

    for i in range(len(peaks)):
      for j in range(1, fan_value):
        if (i + j) < len(peaks):
          freq1 = peaks[i][IDX_FREQ_I]
          freq2 = peaks[i + j][IDX_FREQ_I]
          
          t1 = peaks[i][IDX_TIME_J]
          t2 = peaks[i + j][IDX_TIME_J]
          t_delta = t2 - t1
          
          if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
            h = hashlib.sha1("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta)))
            yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)

def replaceZeroes(data):
  min_nonzero = np.min(data[np.nonzero(data)])
  data[data == 0] = min_nonzero
  return data