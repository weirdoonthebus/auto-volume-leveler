import wave
import struct
import numpy as np
import os
import sys
import glob
from pydub import AudioSegment


#globals
songs = []

if __name__ == '__main__':

	# provide folder name as argument
	folder = sys.argv[1]

	if not folder:
		print("Please provide a folder to use")
	else:
		print("Searching for .wavs in: " + folder)

	# extract files array from folder
	current_dir = os.getcwd()
	target_dir = current_dir + "/" + folder + "/*.wav"

	files = glob.glob(target_dir)
	total = len(files)

	print("Found " + str(total) + " .wav files.")


	# for returning htz values later
	def get_levels(file):
        	file_name = file.replace(current_dir + "/" + folder + "/", "")
	        print("Processing: " + file_name)

		frate = 11025.0

		wav_file = wave.open(file, 'r')
		data_size = wav_file.getnframes()
		data = wav_file.readframes(data_size)
		vol  = struct.unpack("%ih" % (data_size* wav_file.getnchannels()), data)
		wav_file.close()

		# calculate frequency
		data = struct.unpack('{n}h'.format(n=data_size), data)
		data = np.array(data)
		w = np.fft.fft(data)
		freqs = np.fft.fftfreq(len(w))
		print("Min Freq: " + str(freqs.min()), "Max Freq: " + str(freqs.max()))

		# Find the peak in the coefficients
		idx = np.argmax(np.abs(w))
		freq = freqs[idx]
		freq_in_hertz = abs(freq * frate)
		print("Median Freq in Hertz: " + str(freq_in_hertz))

		# Calculate volume
		vol = [float(val) / pow(2, 15) for val in vol]
		print("Min Vol: " + str(min(vol)), "Max Vol: " + str(max(vol)))

		median_vol = np.mean(vol)
		print("Median Volume: " + str(median_vol))

		# Add to master array
		song = [file, freq_in_hertz, median_vol]
		songs.append(song)


	# adjust volume off competed calculations
	def adjust_levels(file):
		file_name = file.replace(current_dir + "/" + folder + "/", "")
		song = AudioSegment.from_wav(file)


		###

		song.export(current_dir + "/" + folder + "_processed/" + file_name)




	# loop and get htz for each file
        i = 0
        while i < total:
                get_levels(files[i])
                i += 1
		if (i == total):
			print(songs)

	# then loop the hrtz values and adjust each
	j = 0
	while i >= total and j < total:
#		adjust_levels(songs[j])
		j += 1
