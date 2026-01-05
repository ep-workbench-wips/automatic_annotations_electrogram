import scipy
import numpy as np

def nleo(signal):
	"""
	Compute the non-linear energy of a signal
	"""

	out = [0]
	for i in range(1, len(signal)-1):
		out.append(signal[i]**2 - (signal[i-1]*signal[i+1]))
	out.append(0)

	return out

def annotate_bounds(egm, fs, e_percentile=85, v_percentile=10):
	"""
	egm = signal to annotate
	fs = sampling frequency (usually 1000 for CARTO, 2000 for EnSite)
	e_percentile = minimum energy percentile required for signal to be "on"
	v_percentile = minimum voltage percentile required for signal to be "on"
	"""
	egm_nleo = nleo(egm)
	lpf = scipy.signal.butter(N=2, Wn=65, btype='lowpass', fs=fs, output='sos')
	egm_nleo_lpf = np.absolute(scipy.signal.sosfiltfilt(lpf, egm_nleo))
	egm = np.absolute(egm)

	e_threshold = np.percentile(egm_nleo_lpf, e_percentile)
	v_threshold = np.percentile(egm, v_percentile)

	onset = -10000
	for t, v in enumerate(egm_nleo_lpf):
		if v > e_threshold and egm[t] > v_threshold:
			onset = t + 1
			break

	offset = -10000
	for t, v in enumerate(egm_nleo_lpf[::-1]):
		if v > e_threshold and egm[::-1][t] > v_threshold:
			offset = len(egm) - t - 1
			break
	return onset, offset

case = cases[case_1]
num_pts = len(case.electric.bipolar_egm._egm)
for i in range(0, num_pts):
	egm = case.electric.bipolar_egm._egm[i]
	print
	fs = len(egm)/2.5
	woi_start = int(case.electric.annotations.window_of_interest[i][0])
	woi_end = int(case.electric.annotations.window_of_interest[i][1])
	ref = int(case.electric.annotations.reference_activation_time[i])
	egm = egm[ref+woi_start:ref+woi_end]

	e_percentile=80
	v_percentile=10
	onset, offset = annotate_bounds(egm, fs, e_percentile, v_percentile)
	case.electric.annotations._local_activation_time_indices[i] = float(offset + ref + woi_start)

out_cases['onsets_annotated'] = case