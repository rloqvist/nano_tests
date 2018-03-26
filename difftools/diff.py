import inspect
from difflib import SequenceMatcher
import os
import pickle
import hashlib

filepath = "/".join(os.path.abspath(__file__).split("/")[:-1])
filename = filepath + "/diff.pickle"

class DiffHandler:
    def __init__(self):
        # make sure our caching file exists
        open(filename, "a").close()
        try:
            with open(filename, 'rb') as handle:
                pickle.load(handle)
        except:
            self.clear()

    def clear(self):
        with open(filename, 'wb') as handle:
            pickle.dump(dict(), handle)

    def _put(self, key, value):
        cache = dict()
        with open(filename, 'rb') as handle:
            cache = pickle.load(handle)
        cache[key] = value
        with open(filename, 'wb') as handle:
            pickle.dump(cache, handle)

    def _get(self, key):
        cache = dict()
        with open(filename, 'rb') as handle:
            cache = pickle.load(handle)
        return cache.get(key)

    def _compare_ratio(self, s1, s2):
        return SequenceMatcher(None, s1, s2).ratio()

    def _get_hash(self, func):
        total = "".join(inspect.getsourcelines(func)[0])
        digest = hashlib.sha256(total.encode('utf-8')).hexdigest()
        return int(digest, 16) % 10**8

    def compare(self, test, driver, threshold):
        # convert the function to a hash and use that hash to look for a cached
        # version of the page
        source = driver.page_source
        key = self._get_hash(test)
        cached = self._get(key)
        if not cached:
            self._put(key, source)
            return 1
        current_ratio = self._compare_ratio(cached, source)
        #if current_ratio > threshold:
        self._put(key, source)
        return current_ratio


if __name__ == "__main__":
    d = DiffHandler()
    print(d._get_hash(foo_func))
