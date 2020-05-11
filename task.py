import time
from algorithms import get_algorithm
import config
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
        # Using -1 to represent this task has not been processed
        self.similarity = -1
        self.time_taken = -1

    def __call__(self):
        start_time = time.time()
        self.similarity = self.get_similarity()
        self.time_taken = time.time() - start_time
        return self.image_1 + "," + self.image_2 + "," + str(self.similarity) + "," + str(round(self.time_taken, 3))

    def __str__(self):
        return 'ImageComparisonTask - "%s" - "%s"' % (self.image_1, self.image_2)

    def is_image(self, filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
               f.endswith(".jpeg") or f.endswith(".bmp") or \
               f.endswith(".gif") or '.jpg' in f or f.endswith(".svg")

    def get_similarity(self):

        if not self.is_image(self.image_1) or not self.is_image(self.image_2):
            return -1

        algorithm = get_algorithm(config.DEFAULT_IMAGE_COMPARISON_ALGORITHM)

        try:
            return algorithm.get_similarity(self.image_1, self.image_2)
        except Exception as e:
            print('Problem:', e)
            return -2



