import scipy
import numpy as np

def annotate_lat(signal):
	return np.argmin(np.gradient(signal))

case = cases[case_1]
num_pts = len(case.electric.bipolar_egm._egm)
for i in range(0, num_pts):
	egm = case.electric.unipolar_egm._egm[i]
	uni1, _ = map(list, zip(*egm))
	egm = uni1

	fs = len(egm)/2.5
	woi_start = int(case.electric.annotations.window_of_interest[i][0])
	woi_end = int(case.electric.annotations.window_of_interest[i][1])
	ref = int(case.electric.annotations.reference_activation_time[i])

	egm = egm[ref+woi_start:ref+woi_end]

	lat = annotate_lat(egm)
	case.electric.annotations._local_activation_time_indices[i] = float(lat + ref + woi_start)

out_cases['uni_-dvdt_annotated'] = case
