usage: main.py [-h] [-c] [-s SCALE] [-f] [-p PATH] [-l LOOP] [-d DEBUG]

Laser engraver control software

optional arguments:
  -h, --help            show this help message and exit
  -c, --calibrate       Start with a manual calibration of the position of the
                        laser
  -s SCALE, --scale SCALE
                        The SCALE of the laser movement
  -f, --fast            Activate fast printing
  -p PATH, --path PATH  The PATH to the file to read and engrave
  -l LOOP, --loop LOOP  Set a number of time to loop through the engraving
  -d DEBUG, --debug DEBUG
                        Start engraving in debug mode which print all commands
                        into the specified DEBUG file instead