#!/usr/bin/env python
"""
This is a utility program to compare similarity between images
"""

import csv
import sys
from async_processor import AsyncProcessor
import os
import logging
import time
from metrics import record_error
logging.basicConfig(format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s',
                    level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger(__name__)


def usage(program_name):
    """
    Print usage of the program
    """

    sys.stderr.write("""Usage - python %s [<csv_path>]
""" % program_name)
    sys.exit(1)


if __name__ == '__main__':
    """
    This is the entry point to the program
    It expects the following:
        - csv_path as an argument (could be a relative path from current directory or an absolute path)
        - The first row of the CSV should be header row with 2 columns 'image1' and 'image2'
    
    The CSV reader iterates over lines and maps information in each row to a dictionary with 
    keys as 'image1' and 'image2' and values are path to the image files (relative or absolute paths)
    """

    csv_path = sys.argv[1] if len(sys.argv) > 1 else usage(sys.argv[0])

    # check if csv file exists, else print error and exit
    if not os.path.exists(csv_path):
        logger.error(f'File not found {csv_path}')
        sys.exit(1)

    # If unable to create output file, exit
    time_in_millis = int(round(time.time() * 1000))
    output_file_name = "results/output-%d.csv" % time_in_millis
    with open(output_file_name, mode='a') as output_file:
        try:
            header_columns = "image1,image2,similar,elapsed"
            output_file.write(header_columns + "\n")
            output_file.flush()
        except BaseException as e:
            logger.error(e, exc_info=True)
            record_error("error_output_init")
            sys.exit(1)

    async_worker = AsyncProcessor(output_file_name)
    with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # No retries for now. Try once and continue
                try:
                    if row["image1"] is None or row["image2"] is None:
                        record_error("error_image_none")
                        continue

                    async_worker.queue_image_comparison(row["image1"], row["image2"])
                except BaseException as e:
                    logger.error(e, exc_info=True)
                    record_error("error_starting_comparison")

    async_worker.shutdown()
    async_worker.join()
    logger.info("Shutdown complete")

    

