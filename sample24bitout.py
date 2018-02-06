#
#  stero 16bit WAV file convert  2 times sampling frequency 24bit
#--------------------------------------------------------------
#  Using 
#    Python 2.7.12   32 bit on win 32
#    numpy(1.9.2)
#    scipy(0.16.1)
#  ------------------------------------------------------------

import numpy as np
from scipy.fftpack import fft, ifft
from scipy.io.wavfile import read, write
import sys

#--------------------------------------------------------------
# Using wavio,  Please see wavio.py about copyright of
#                  <https://github.com/WarrenWeckesser/wavio>
import wavio

#--------------------------------------------------------------
# Specify input/output wav file name !
# input wav file name
wavfile="./1000HZ-0dB.WAV"



# output file name
wavfile2="./out1.wav"

# Specify output width Byte, sampwidth
# 16bit 
#sampwidtho=2
# 24bit
sampwidtho=3




#---------------------------------------------------------------


# FFT point and every shift
N = 4096
SHIFT= N/2  # shift must be N/2
N2=N*2      # output point is 2 times than input

w = wavio.read(wavfile)
wdata=w.data
fs=w.rate
sampwidth=w.sampwidth
stmono= wdata.shape[1]
size0= wdata.shape[0]


# show WAV information
print "sampling rate ", fs
print "points ", size0
print "width Byte", sampwidth

if (sampwidth == 2):
	if (sampwidtho == 3):   # case :input 16bit, output 24bit
		bai0=256.0
	else:                   # case :input 16bit, output 16bit
		bai0=1.0
else:
	print "Sorry, only 16bit wav file is available"
	sys.exit()		

if (stmono == 2):
    wleft = wdata[:, 0]
    wright = wdata[:, 1]
else:
	print "Sorry, only stereo wav file is available"
	sys.exit()

# count shift number
num0= int((size0 - N)/ SHIFT) + 1
print "number ", num0


###############################################################
#
#  SHIFT DATA OVERLAP METHOD:
#
#
#     BBBMMMCCCCCCMMMBBB
#              BBBMMMCCCCCCMMMBBB
#     B: zero, ignore, Suteru
#     M: linearly MIX
#     C: sonomama tukau
#
###############################################################
# MIX value
M=3  # bunkatu suu of half duration
NL0=int(N2/(M*2))    # duration CCC and BBB,  ex It's 682 when N=4096
NL= N2/2 - (NL0 *2)  # duration MMM           ex It's 684 when N=4096
print "NL0, NL ", NL0, NL
k0=np.linspace(0,1,NL)
k1=np.linspace(1,0,NL)


# output data
wavo=np.zeros( (size0*2,2) )


for loop in range(num0):
	print "loop ", loop
	
	sp0= SHIFT * loop      # input point
	sp2= SHIFT * 2 * loop  # output point is 2 times than input
	
	#######################################
	# 1st channl process
	ch0=0
	# read N points via every SHIFT
	w1= wleft[sp0: sp0 + N]
	fw1= w1.astype(np.float64)
	
	# Fourier transform via FFT
	yf = fft(fw1)
	# 1/N ga kakarukara node *2baisuru,  center Value ha ryouhou ni huru
	yf2=np.concatenate([yf[0:1] , yf[1:N/2], yf[N/2:N/2+1]*0.5, np.zeros(N-1), yf[N/2:N/2+1]*0.5, yf[N/2+1:N] ]) 
	iyf2= ifft(yf2 * 2)
	
	
	# 1st loop
	if loop == 0:
		# clip between int32 value
		riyf2=np.clip(iyf2.real,-32768.0, 32767)
		#wavo[0:N2/2+NL0,ch0]=riyf2[0:N2/2+NL0].astype(np.int16)
		wavo[0:N2/2+NL0,ch0]=riyf2[0:N2/2+NL0]
	else:
		# mix, duration of mmm
		dmix=(iyf2[N2/2-NL0-NL:N2/2-NL0] * k0)  + dch0[:]  # for ch0
		rdmix=np.clip(dmix.real,-32768.0, 32767)  # clip between int16 value
		#wavo[sp2+N2/2-NL0-NL:sp2+N2/2-NL0,ch0]=rdmix[:].astype(np.int16)
		wavo[sp2+N2/2-NL0-NL:sp2+N2/2-NL0,ch0]=rdmix[:]
		
		# duration of ccc
		riyf2=np.clip(iyf2.real,-32768.0, 32767)  # clip between int16 value
		wavo[sp2+N2/2-NL0:sp2+N2/2+NL0,ch0]=riyf2[N2/2-NL0:N2/2+NL0]		

	# copy to backup
	dch0=iyf2[N2/2+NL0:N2/2+NL0+NL] * k1
	# 1st channl process end
	#######################################


	#######################################
	# 2nd channl process
	ch0=1
	# read N points via every SHIFT
	w1= wright[sp0: sp0 + N]
	fw1= w1.astype(np.float64)
	
	# Fourier transform via FFT
	yf = fft(fw1)
	# 1/N ga kakarukara node *2baisuru,  center Value ha ryouhou ni huru
	yf2=np.concatenate([yf[0:1] , yf[1:N/2], yf[N/2:N/2+1]*0.5, np.zeros(N-1), yf[N/2:N/2+1]*0.5, yf[N/2+1:N] ] )
	iyf2= ifft(yf2 * 2)
	
	
	# 1st loop
	if loop == 0:
		# clip between int32 value
		riyf2=np.clip(iyf2.real,-32768.0, 32767)
		wavo[0:N2/2+NL0,ch0]=riyf2[0:N2/2+NL0]
	else:
		# mix, duration of mmm
		dmix=(iyf2[N2/2-NL0-NL:N2/2-NL0] * k0)  + dch1[:]  # for ch1
		rdmix=np.clip(dmix.real,-32768.0, 32767)  # clip between int16 value
		wavo[sp2+N2/2-NL0-NL:sp2+N2/2-NL0,ch0]=rdmix[:]
		
		# duration of ccc
		riyf2=np.clip(iyf2.real,-32768.0, 32767)  # clip between int16 value
		wavo[sp2+N2/2-NL0:sp2+N2/2+NL0,ch0]=riyf2[N2/2-NL0:N2/2+NL0]		

	# copy to backup
	dch1=iyf2[N2/2+NL0:N2/2+NL0+NL] * k1
	# 2nd channl process end
	#######################################

# write output
#  In wavio.write, scaling is not done, only clipping is available.
wavio.write(wavfile2, wavo * bai0, fs * 2, scale="none", sampwidth=sampwidtho)








