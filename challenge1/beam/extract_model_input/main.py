
import sys
import logging
import extract_model_input

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    extract_model_input.run(sys.argv)
