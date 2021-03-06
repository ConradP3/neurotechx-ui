# import csv
# import pickle
# import os
import numpy as np
from sklearn import preprocessing as sk
import mne

def process(chunk):
	# TODO: perform MNE processing here
	print(type(chunk))
	chunk = np.transpose(chunk)

	info = mne.create_info(7, sfreq=250, ch_types='emg')

	raw = mne.io.RawArray(chunk, info)
	sfreq = 1000
	f_p = 40

	# Applying butterworth filter
	iirs_params = dict(order=4, ftype='butter', output='sos')
	iir_params = mne.filter.construct_iir_filter(iirs_params, f_p, None, sfreq, 'lowpass', return_copy=False,
												 verbose=True)

	filtered_raw = mne.filter.filter_data(chunk, sfreq=sfreq, l_freq=None, h_freq=f_p, picks=None, method='iir',
										  iir_params=iir_params, copy=False, verbose=True)

	filtered_data = mne.io.RawArray(filtered_raw, info)

	# Setting up data for fitting
	#ICA is removed for now, but might be used again in the future
# 	ica_info = mne.create_info(7, sfreq, ch_types='eeg')
# 	ica_data = mne.io.RawArray(filtered_raw, ica_info)

# 	# Fitting and applying ICA
# 	ica = mne.preprocessing.ICA(verbose=True)
# 	ica.fit(inst=ica_data)
# 	ica.apply(ica_data)
# 	filtered_raw_numpy = ica_data[:][0]

	#Normalization
# 	normalized_raw = sk.normalize(filtered_raw_numpy, norm='l2')
# 	preprocessed_raw = ica_data[:][0]
# 	normalized_raw = sk.normalize(preprocessed_raw, norm='l2')
# 	print((normalized_raw))

# 	normalized_data = mne.io.RawArray(normalized_raw, info)
	return filtered_data[:][0]

# def splice(filename, channels=7, hz=250, chunkSecs=2):

# 	chunks, curr, labels = [], [], [] # all chunks, current reading chunk
# 	#with open(filename, 'r') as file:
# 	#f = csv.reader(file)
# 	# for i in range(5): # skip first five lines
# 	# 	next(f)

# 	for l in filename:
# 		if len(curr) == chunkSecs * hz: # if done with one chunk
# 			# if len(chunks) < 35:
# 			# 	labels.append(1)
# 			# else:
# 			# 	labels.append(0)

# 			# decide how to label data.
# 			# if truth == "no" :
# 			# 	labels.append(0)
# 			# elif truth == "yes" :
# 			# 	labels.append(1)

# 			chunks.append(process(curr)) # add to list of all chunks
# 			curr = [] # prepare for next chunk

# 		curr.append([float(sample) for sample in l[1:channels]]) # add channel recording to current chunk

# 	data = np.asarray(chunks) # convert chunks to np array
# 	# with open('%s_labels.csv' % filename.split('.')[0], 'w', newline='') as file:
# 	# 	writer = csv.writer(file)
# 	# 	writer.writerow(labels)

# 	pickle.dump(data, open('%s.pkl' % filename.split('.')[0], 'wb'))
# 	print('Extracted %d chunks from %s' % (data.shape[0], filename))
