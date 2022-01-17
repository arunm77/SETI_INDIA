import numpy as np
from astropy import units as u
import setigen as stg
from baseband import guppi

sample_rate = 1024e3 #taken as 2*BW
num_taps = 1
num_branches = 2048
chan_bw = sample_rate / num_branches

antenna = stg.voltage.Antenna(sample_rate=sample_rate, 
                              fch1=0,
                              ascending=True,
                              num_pols=1)

rvb = stg.voltage.RawVoltageBackend(antenna,
                                    num_chans=1,
                                    block_size=64,
                                    blocks_per_file=64,
                                    num_subblocks=64)

rvb.record(output_file_stem='/home/arunm77/GUPPIRAW/small2_GUPPI',
           num_blocks=1, 
           length_mode='num_blocks',
           header_dict={'OBSERVER': 'SETI_INDIA',
                        'TELESCOP': 'GMRT',
                        'DIRECTIO' : 0
                        },
           verbose=False)

# start_chan = 0
# input_file_stem = '/home/arunm77/GUPPIRAW/small_G2'
# raw_params = stg.voltage.get_raw_params(input_file_stem=input_file_stem,
#                                         start_chan=start_chan)

# TO PRINT FILE CONTENTS
fid = guppi.open('/home/arunm77/GUPPIRAW/small2_GUPPI.0000.raw','rb')
d = fid.read()
fid.close()
num_array2 = [np.int8(numeric_string) for numeric_string in d]
print(d)
print(d.rfind(b'END'))  # .rfind for last occurrence of 'END'. Chance to confuse with 'BACKEND'