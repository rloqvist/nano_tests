from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from time import time, sleep
from uuid import uuid4
import os, sys
from utils import *
import inspect
from difftools.diff import DiffHandler

class DefaultCase:

    def __init__(self, useDisplay=False, size=None, clearCache=False):
        if clearCache:
            DiffHandler().clear()
        self.useDisplay = useDisplay
        if size:
            self.size = size
        else:
            self.size = 800, 600

    def setUp(self):
        if not self.useDisplay:
            print_info("Starting virtual display with size {0}x{1}".format(*self.size))
            self.display = Display(visible=0, size=self.size)
            self.display.start()
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()
        if not self.useDisplay:
            self.display.stop()

    def waitFor(self, identifier, find_by=By.CLASS_NAME, timeout=10, withLogging=True):
        """
        Utility method
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((find_by, identifier)))
            return True
        except:
            return False

    def compare(self, threshold=0.8):
        """
        Utility method

        Set the threshold ratio for which the cached
        version of the page should be updated with the current one
        """
        func_str = inspect.stack()[1][3]
        func = getattr(self, func_str)
        d = DiffHandler()
        result = d.compare(func, self.driver, threshold)
        print_info("Comparison ratio:", result)
        return result >= threshold

    def getTestNames(self):

        ### Get all the names
        testNames = [
                        func_str for func_str in dir(self)
                            if callable(getattr(self, func_str))
                                and func_str.startswith("test_")
                    ]

        ### Try to order them by docstring integer
        tests = [getattr(self, func_str) for func_str in testNames]
        def getOrder(test):
            try:
                return int(test.__doc__)
            except:
                return 0
        sorted_test_names = [test.__name__ for test in sorted(tests, key=getOrder)]


        return sorted_test_names

    def run(self):
        names = self.getTestNames()
        successful = True
        for test_name in names:
            test_func = getattr(self, test_name)
            ret = False
            try:
                ret = test_func() # do the actual test
            except Exception as ex:
                print(ex)
            finally:
                if not ret:
                    print("Test failed: {0}".format(test_name))
                    successful = False
        return successful

if __name__ == '__main__':
    test = DefaultCase()
    test.setUp()
    test.run()
    test.tearDown()
