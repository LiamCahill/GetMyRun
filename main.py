import logging

import gs_reader
import todays_run


def set_logging():
    logging.basicConfig(
        filename="output.log",
        level=logging.DEBUG,
        format='%(levelname)s %(asctime)s %(message)s'
    )


def main():
    set_logging()
    gsa = gs_reader
    gsa.start_gs_reader()

    tr = todays_run
    tr.get_todays_run_info()


if __name__ == "__main__":
    main()
