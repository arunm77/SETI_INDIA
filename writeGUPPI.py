from baseband import guppi
import astropy.units as u
from baseband.data import SAMPLE_PUPPI
from astropy.time import Time
import numpy as np

# Polarization 1

fv1 = guppi.open('/home/arunm77/iFFT/VLBI_SPECTRAL_VLT_25MHZ_17Mar2021/B0740-28_B4_25MHz_P1_small.rawvlt','rb')
dv1 = fv1.read()
fv1.close()
num_array1 = [np.int8(numeric_string) for numeric_string in dv1]

### WARNING - LENGTH IS PRESET ### 
cmplx_len = 40000

if len(num_array1)%2 != 0:
    print('Array length fault for complex values')
cmplx_len1 = int(len(num_array1)/2)
cmplx_len1 = cmplx_len
nchan = 2048
npol = 2

rem = int(cmplx_len1%nchan)
if rem!= 0:
    append_len = nchan - rem
    eff_len = cmplx_len1 + append_len
else:
    eff_len = cmplx_len1

cmplx_array1 = np.zeros(eff_len,dtype=np.complex64)
for i in range(eff_len): # This is taking time (8+ min)
    cmplx_array1[i] = np.complex(num_array1[2*i],num_array1[2*i+1]) 

nblocks1 = int(eff_len/(npol*nchan))


# Polarization 2

fv2 = guppi.open('/home/arunm77/iFFT/VLBI_SPECTRAL_VLT_25MHZ_17Mar2021/B0740-28_B4_25MHz_P2_small.rawvlt','rb')
dv2 = fv2.read()
fv2.close()
num_array2 = [np.int8(numeric_string) for numeric_string in dv2]

if len(num_array2)%2 != 0:
    print('Array length fault for complex values')
cmplx_len2 = int(len(num_array2)/2)
cmplx_len2 = cmplx_len
nchan = 2048
npol = 2

rem = int(cmplx_len2%nchan)
if rem!= 0:
    append_len = nchan - rem
    eff_len = cmplx_len2 + append_len
else:
    eff_len = cmplx_len2

cmplx_array2 = np.zeros(eff_len,dtype=np.complex64)
for i in range(eff_len): # This is taking time (8+ min)
    cmplx_array2[i] = np.complex(num_array2[2*i],num_array2[2*i+1]) 

nblocks2 = int(eff_len/(npol*nchan))

# Interspersing the two polarizations
cmplx_array = np.zeros(2*eff_len,dtype=np.complex64)
nblocks = int(eff_len/nchan)
for i in range(nblocks):
    for j in range(nchan):
        cmplx_array[2*i*nchan+j] = cmplx_array1[i*nchan+j]
        cmplx_array[(2*i+1)*nchan+j] = cmplx_array2[i*nchan+j]


data_array = np.asarray(cmplx_array.reshape((nblocks, npol, nchan)))


# Writing GUPPI raw

ftestw = guppi.open('/home/arunm77/GUPPIRAW/Guppi_test.0002.raw', 'ws', 
                sample_rate=250*u.Hz,
                samples_per_frame=960, pktsize=1024,
                time=Time(58132.59135416667, format='mjd'),
                npol=2, nchan=2048)
ftestw.write(data_array)
ftestw.close()
ftestr = guppi.open('/home/arunm77/GUPPIRAW/Guppi_test.0002.raw', 'rs')
dtest = ftestr.read()
print(dtest.shape)