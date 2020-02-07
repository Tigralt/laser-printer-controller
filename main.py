#!/usr/bin/env python3
from laser_engraver import LaserEngraver
from matrix import load_vectors
from argparse import ArgumentParser
from progressbar import ProgressBar
import numpy as np
    
if __name__ == "__main__":
    # Parsing CLI args
    parser = ArgumentParser(description="Laser engraver control software")
    parser.add_argument("-c", "--calibrate", help="Start with a manual calibration of the position of the laser", action="store_true")
    parser.add_argument("-s", "--scale",     help="The SCALE of the laser movement", type=float, default=1)
    parser.add_argument("-f", "--fast",      help="Activate fast printing", action="store_true")
    parser.add_argument("-p", "--path",      help="The PATH to the file to read and engrave")
    parser.add_argument("-l", "--loop",      help="Set a number of time to loop through the engraving", type=int, default=1)
    parser.add_argument("-d", "--debug",     help="Start engraving in debug mode which print all commands into the specified DEBUG file instead")
    args = parser.parse_args()

    if not (args.calibrate or args.path):
        parser.print_help()
        exit()

    # Init laser engraver
    laser = LaserEngraver(debug=bool(args.debug))

    # Calibrate laser position
    if args.calibrate:
        laser.calibrate()

    # Set laser movement scale
    if args.scale:
        laser.set_scale(args.scale)

    # Load file and engrave it
    if args.path:
        matrix = np.loadtxt(args.path, dtype=int)
        vectors = load_vectors(matrix)

        # Engrave with laser
        laser.unlock()
        laser.set_position_mode("ABSOLUTE")
        laser.set_unit_mode("MILLIMETERS")

        with ProgressBar(max_value=args.loop * len(vectors)) as bar:
            loading = 0
            for _ in range(0, args.loop):
                for vector in vectors:
                    laser.move(vector["x"], vector["y"], args.fast)
                    laser.set_laser(True)
                    laser.move(vector["x"] + vector["length"], vector["y"], args.fast)
                    laser.set_laser(False)

                    loading += 1
                    bar.update(loading)
                laser.move(0, 0) # Reset position

        if args.debug:
            laser.save_debug_logs(args.debug)