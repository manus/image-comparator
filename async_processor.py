"""
The code here defines capabilities needed for sending tasks to a queue to be processed asynchronously.
"""

import multiprocessing
from consumer import Consumer
from task import ImageComparisonTask
import time
from metrics import time_method
import logging
logger = logging.getLogger(__name__)


class AsyncProcessor(object):

    def __init__(self, output_file_name):
        self.tasks_queue = multiprocessing.JoinableQueue()
        self.write_output_lock = multiprocessing.Lock()
        self.num_consumers = multiprocessing.cpu_count() * 2

        self.consumers = [Consumer(self.tasks_queue, output_file_name, self.write_output_lock)
                          for i in range(self.num_consumers)]
        logger.info('Starting %d consumers' % self.num_consumers)
        for w in self.consumers:
            w.start()

    def join(self):
        # Wait for all of the tasks to finish
        self.tasks_queue.join()

    @time_method
    def queue_image_comparison(self, image_1, image_2):
        task = ImageComparisonTask(image_1, image_2)
        logger.info('Queuing task : %s' % task)
        self.tasks_queue.put(task)

    def shutdown(self):
        logger.info("Sending shut down signal to consumers")
        # Add a poison pill for each consumer
        for i in range(self.num_consumers):
            self.tasks_queue.put(None)
