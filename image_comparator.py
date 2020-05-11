#!/usr/bin/env python
import logging
import csv
import sys
from async_processor import AsyncProcessor
import os
import logging
logging.basicConfig(format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s',
                    level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger(__name__)


def usage(program_name):
    sys.stderr.write("""Usage - %s [<csv_path>]
""" % program_name)
    sys.exit(1)


if __name__ == '__main__':

    csv_path = sys.argv[1] if len(sys.argv) > 1 else usage(sys.argv[0])

    # check if csv file exists, else print error and exit
    if not os.path.exists(csv_path):
        logger.error(f'File not found {csv_path}')
        sys.exit(1)

    async_worker = AsyncProcessor()
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logger.debug(f'Column names are {", ".join(row)}')
                line_count += 1
            logger.debug(f'{row["image1"]} --- {row["image2"]}')
            async_worker.queue_image_comparison(row["image1"], row["image2"])
            line_count += 1

        logger.info(f'Processed {line_count} lines.')
        async_worker.shutdown()
        async_worker.join()
        logger.info("Shutdown complete")

    

