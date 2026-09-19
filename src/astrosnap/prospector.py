"""
File: prospector.py

Prospector helper tools for preparation of Prospector fit running and later analysis.

Programmer: Neil Ghugare

Revision History:
09/19/2026 - Created initial version.

Notes:
"""

import glob
import os
import warnings

from typing import *
from tqdm import tqdm 


def create_slurm_array_text(fp: str, zred: float, snap_num: int, output: Optional[str] = 'galaxy_list.txt') -> None:
    """
    Creates a .txt file that can be used for a SLURM job array.

    Arguments (Required)
    1. fp: The file path/directory where the .rtout.sed files are located
    2. zred: The redshift of the files.
    3. snap_num: The snapshot number of the simulation suite.

    Arguments (Optional)
    1. output: The output .txt file name.

    Returns

    None.
    """

    # Use glob to read in all the available .rtout.sed files in the directory.
    files = glob.glob(os.path.join(fp, '*.rtout.sed'))

    # Open up the output file.
    with open(output, 'w') as f:
        # Write a header for the .txt file table.
        f.write('# galaxyid zred directory snap_num\n')

        # Iterate the files.
        # TQDM allows for a nice loading bar output. 
        for fp in tqdm(files):
            # Fetch the base .rtout.sed file name without the path.
            fn = os.path.basename(fp)

            # Attempt to dynamically extract the galaxy id.
            # ! This expects that the galaxy snapshot output is in the following format: 
            # ! snap[no.]_galaxy[no.].rtout.sed, where [no.] represents the number of the snapshot and galaxy, respectively.
            # TODO: Make this work for more formats.
            try:
                galaxy_id = fn[fn.index('galaxy')+6:fn.index('rtout')-1]
                galaxy_id = int(galaxy_id)
            except Exception:
                # If we encounter an error, skip. 
                warnings.warn(f'Galaxy ID for file {fn} could not be resolved. Skipping...')
                continue

            # Write the data to the output file.
            f.write(f'{galaxy_id} {zred} {fp} {snap_num}\n')

    # Close the file. 
    f.close()

    return