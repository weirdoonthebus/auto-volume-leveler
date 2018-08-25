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
	        print("Processing: " + str(file_name))
		mode = "r"
		sizes = {1: "B", 2: "h", 4: "i"}
		wav_file = wave.open(file, mode)

		channels = wav_file.getnchannels()
		print("channels: " + str(channels))
		samples = wav_file.getsampwidth()
		print("samples: " + str(samples))
		frames = wav_file.getnframes()
		fmt_size = sizes[samples]
		print("size: " + str(fmt_size))
		fp = channels * samples
		print("fp: " + str(fp))
		fmt = "<" + fmt_size * fp
		print("fmt: " + str(fmt))
		while wav_file.tell() < wav_file.getnframes():
			try:
				channels = wav_file.getnchannels()
			        print("channels: " + str(channels))
		                samples = wav_file.getsampwidth()
		                print("samples: " + str(samples))
		                frames = wav_file.getnframes()
		                fmt_size = sizes[samples]
		                print("size: " + str(fmt_size))
		                fp = channels * samples
		                print("fp: " + str(fp))
		                fmt = "<" + fmt_size * fp
		                print("fmt: " + str(fmt))
				decoded = struct.unpack(fmt, wav_file.readframes(channels))
			except struct.error:
	        		# (w.getnframes() - w.tell()) < chunk_size
				tmp_size = wav_file.getnframes() - wav_file.tell()
				tmp_fmt = "<{0}h".format(16)
				decoded = struct.unpack(tmp_fmt, wav_file.readframes(channels))

		print(decoded)


#		while wav_file.tell() < wav_file.getnframes():
#			decoded = struct.unpack(fmt, wav_file.readframes(channels))
#			data.append(decoded)
#
#		print(data)
		

#		frames = wav_file.getnframes()
#		rate = wav_file.getframerate()
##		duration = frames / rate
####		data_size = frames * rate
#		data = wav_file.readframes(frames)

		#vol  = struct.unpack("%ih" % (frames* wav_file.getnchannels()), data)

		wav_file.close()
		# calculate frequency
#		data = struct.unpack("<h".format(n=rate), data)
#		data = np.array(data)
#		w = np.fft.fft(data)
#		freqs = np.fft.fftfreq(len(w))
#		print("Min Freq: " + str(freqs.min()), "Max Freq: " + str(freqs.max()))
#
#		# Find the peak in the coefficients
#		idx = np.argmax(np.abs(w))
#		freq = freqs[idx]
#		freq_in_hertz = abs(freq * frate)
#		print("Median Freq in Hertz: " + str(freq_in_hertz))
#
#		# Calculate volume
#		vol = [float(val) / pow(2, 15) for val in vol]
#		print("Min Vol: " + str(min(vol)), "Max Vol: " + str(max(vol)))
#
##		median_vol = np.mean(vol)
#		print("Median Volume: " + str(median_vol))
#
#		# Add to master array
#		song = [file, freq_in_hertz, median_vol]
#		songs.append(song)


	# adjust volume off competed calculations
	def adjust_levels(file):
		file_name = file.replace(current_dir + "/" + folder + "/", "")
		song = AudioSegment.from_wav(file)


		###

		song.export(current_dir + "/" + folder + "_processed/" + file_name)




	# loop and get htz for each file
        i = 0
        while i < total:
		if (i == 0):
                	get_levels(files[i])
                i += 1
		if (i == total):
			print(songs)




	# then loop the hrtz values and adjust each
	j = 0
	while i >= total and j < total:
#		adjust_levels(songs[j])
		j += 1
