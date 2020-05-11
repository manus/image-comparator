"""
The code here abstracts an asynchronous task.
It defines a base class 'Task' which can be extended
"""

import time
from algorithms import get_algorithm
import config
from metrics import record_error
import logging
logger = logging.getLogger(__name__)


class Task(object):

    def __init__(self):
        self.create_time = time.time()

    def __call__(self):
        pass

    def __str__(self):
        pass


class ImageComparisonTask(Task):

    def __init__(self, image_1, image_2):
        super(ImageComparisonTask, self).__init__()
        self.image_1 = image_1
        self.image_2 = image_2
        # Using -2 to represent this task has not been processed
        self.similarity = -2
        self.time_taken = -2

    def __call__(self):
        start_time = time.time()
        self.similarity = self.get_similarity()
        self.time_taken = time.time() - start_time
        return f'{self.image_1},{self.image_2},{self.similarity},{round(self.time_taken, 3)}'

    def __str__(self):
        return 'ImageComparisonTask - "%s" - "%s"' % (self.image_1, self.image_2)

    def is_image(self, filename):
        """
        For now, just checking file extension, not the actual format
        """

        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
               f.endswith(".jpeg") or f.endswith(".bmp") or \
               f.endswith(".gif") or '.jpg' in f or f.endswith(".svg")

    def get_similarity(self):
        if not self.is_image(self.image_1) or not self.is_image(self.image_2):
            raise Exception('Invalid image file')

        """
        For exact match, a brute force algorithm would be to match images pixel by pixel
        But the phash algorithm is able to identify exact matches quite efficiently.
        So relying on phash for exact matches. It returns 1.0 for exact matches.
        The target is to return 0 for exact matches. So if result is 1.0, changing it to 0
        This will create confusion if phash actually returns 0 similarity for 2 images.
        So changing 0 similarity to -1 (although this would be vary rare that 2 images have 0 similarity) 
        """
        algorithm = get_algorithm(config.DEFAULT_IMAGE_COMPARISON_ALGORITHM)
        similarity = algorithm.get_similarity(self.image_1, self.image_2)
        if similarity == 0:
            return -1
        elif similarity == 1:
            return 0
        else:
            return similarity




