# SETI_INDIA

Usage:
-----

```bash
$ python3 gmrt_raw_toguppi [path/to/rawfile] [chunk]
$ python3 gmrt_raw_toguppi path/to/rawfile 4096
$ file created: path/to/guppifile
```
[chunk] - is optional; \
if you want to read just first few bytes of files instead of the whole file.


NOTE
----- 
Imaginary data is not being read as documentation(https://baseband.readthedocs.io/en/stable/api/baseband.guppi.open.html#baseband.guppi.open):
For GUPPI, complex data is only allowed when nchan > 1.