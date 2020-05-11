from PIL import Image
import six
import imagehash
import config


class Algorithm(object):

    def get_similarity(self, image_1, image_2):
        return -1


class ImageHashAlgorithm(Algorithm):

    def __init__(self, hash_method):
        self.hash_method = hash_method
        self.hash_func = self.get_hash_func(self.hash_method)

    def get_hash_func(self, hash_method):
        hash_func = None
        if hash_method == 'ahash':
            hash_func = imagehash.average_hash
        elif hash_method == 'phash':
            hash_func = imagehash.phash
        elif hash_method == 'dhash':
            hash_func = imagehash.dhash
        elif hash_method == 'whash-haar':
            hash_func = imagehash.whash
        elif hash_method == 'whash-db4':
            hash_func = lambda img: imagehash.whash(img, mode='db4')
        return hash_func

    def get_similarity(self, image_1, image_2):
        hash_1 = self.hash_func(Image.open(image_1))
        hash_2 = self.hash_func(Image.open(image_2))
        return hash_1 - hash_2


algorithm_dict = {}
algorithm_dict[config.DEFAULT_IMAGE_COMPARISON_ALGORITHM] = ImageHashAlgorithm(config.DEFAULT_IMAGE_COMPARISON_ALGORITHM)


def get_algorithm(algorithm_name):
    return algorithm_dict[algorithm_name]

