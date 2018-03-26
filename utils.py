import sys
import datetime

def get_init_arguments():
    args = {
        "useDisplay": False,
        "size": None,
        "clearCache": False,
    }
    if "-d" in sys.argv:
        args["useDisplay"] = True
    elif "-s" in sys.argv:
        # seems to be called with the size option
        # now figure out what size to use
        fail_string = "Size option given, but no size was specified (in the format <width>x<height>)"
        size_index = sys.argv.index("-s") + 1
        if len(sys.argv) == size_index:
            print_warning(fail_string)
            sys.exit(1)
        try:
            size_option = sys.argv[size_index]
            size_list = size_option.split("x")
            args["size"] = int(size_list[0]), int(size_list[-1])
        except:
            print_warning(fail_string)
            sys.exit(1)
    if datetime.datetime.now().weekday() == 6 or "-c" in sys.argv:
        args["clearCache"] = True
    return args

def print_test(*args, **kwargs):
    print("[TEST]:", *args, **kwargs)

def print_info(*args, **kwargs):
    print("[INFO]:", *args, **kwargs)

def print_error(*args, **kwargs):
    print("[ERROR]:", *args, **kwargs)

def print_warning(*args, **kwargs):
    print("[WARNING]:", *args, **kwargs)
