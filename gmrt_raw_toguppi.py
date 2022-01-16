import numpy as np
from pathlib import Path
from baseband import guppi
import sys
from os import path
#from astropy.time import Time
#import astropy.units as u

def gmrt_guppi(rawfile, npol=2, header=None, chunk=None, samples_per_frame=4096, nchan=1):
    """
    To read gmrt raw voltages file of GWB to convert to guppi raw

    :USAGE:
    --------
    $ python3 gmrt_raw_toguppi [path/to/rawfile] [chunk]
    
    $ python3 gmrt_raw_toguppi path/to/rawfile 4096
    $ file created: path/to/guppifile
    
    [chunk] is optional

    NOTE
    ----- 
    imaginary data is not being read as documentation(https://baseband.readthedocs.io/en/stable/api/baseband.guppi.open.html#baseband.guppi.open):
    For GUPPI, complex data is only allowed when nchan > 1.
    """
    if path.isfile(rawfile):
        rawname=Path(rawfile).stem
        if header is None:
            header = {#'CHAN_BW':-100,
        'TBIN':1, #provide sample rate in astropy.units * Hz
        'TELESCOP':'GMRT',
        'NPOL':npol,
        'NCHAN':nchan,
        'OBSERVER':'Avinash Kumar',
            'STT_IMJD':58132,
            'STT_SMJD':51093,
        'NBITS':8}
        print(f'selected parameters: rawfile={rawfile}, npol={npol}, header={header}, chunk={chunk}, samples_per_frame={samples_per_frame}, nchan={nchan}')
        if chunk is None:
            npcm_data=np.memmap(rawfile, dtype='<i1', mode='r' )#,shape=(4096,))
        else:
            npcm_data=np.memmap(rawfile, dtype='<i1', mode='r', shape=(chunk,))
        npcm_data.flush()
        real_d =npcm_data[::2] # odd indexed
        #im_d = npcm_data[1::2] # even indexed

        #pol1, pol2 = npcm_data[::2], npcm_data[1::2] # if no imaginary is in the bytes
        pol1, pol2 = real_d[::2], real_d[1::2]
        
        
        # pol1_real, pol2_real = real_d[::2], real_d[1::2]
        # pol1_im,pol2_im =im_d[1::2],im_d[::2] # if you need imaginary and real
        # pol1=pol1_real#+pol1_im*1j
        # pol2=pol2_real#+pol2_im*1j
        
        
        resd=np.array([pol1,pol2], dtype='int8').transpose()
        guppifile=rawname+'_guppi.0000.raw'

        fgh = guppi.open(guppifile, 'ws',#frames_per_file=2,
                    samples_per_frame=samples_per_frame, nchan=nchan, npol=npol,
                    **header)
        fgh.write(resd)
        fgh.close()
        return f'file created: {guppifile}'
    else:
        return f'file does not exist : {rawfile}'

def cli():
    rawfile=None
    chunk=None
    help = f'[filename] [chunk]'
    
    if len(sys.argv)>1 and len(sys.argv)<4:
        if len(sys.argv) ==2:
            try:
                rawfile=str(sys.argv[1])
            except:
                print(f'give filename!')
        elif len(sys.argv) == 3:
            try:
                rawfile=str(sys.argv[1])
                chunk = int(sys.argv[2])
            except:
                print(f'wrong arguements!')
        else:
            print(help)
        print(gmrt_guppi(rawfile=rawfile,chunk=chunk ))
    else:
        print(help)
if __name__=='__main__':
    cli()
