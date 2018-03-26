from default import DefaultCase
import time
import sys

class FooTest(DefaultCase):

    def _test_always_fail(self):
        return False

def main(**kwargs):

    test = FooTest(**kwargs)
    test.setUp()
    result = test.run()
    test.tearDown()
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    kwargs = get_init_arguments()
    main(**kwargs)
