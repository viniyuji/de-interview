
import sys
import logging
import load_dw

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    load_dw.run(sys.argv)
