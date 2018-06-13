###############################################################################
#
# Miscellaneous functions to support libmsot
#
###############################################################################

from datetime import datetime, timedelta
from itertools import zip_longest


def convert_time(timestamp):
    ''' Windows NT time is specified as the number of 100 nanosecond intervals since
        01/01/1601 00:00:00 UTC. It is stored as a 64 bit value. Python time libraries use
        the format of seconds since 01/01/1970. '''

    epoch_as_filetime = 116444736000000000
    hundreds_of_ns = 10000000

    # Convert to little endian before converting to int. Timestamp is a string containing a hex value.
    # Split into a list (1 byte per element), reverse the list, and convert back to string.
    timestamp_le = []
    for offset in range(0, 16, 2):
        timestamp_le.append(timestamp[offset:offset + 2])
    timestamp_le = timestamp_le[::-1]
    timestamp_le = ''.join(timestamp_le)

    # Convert timestamp_le to int
    timestamp_int = int(timestamp_le, 16)

    return (datetime.utcfromtimestamp((timestamp_int - epoch_as_filetime) / hundreds_of_ns))


def chunker(data, query_size, fillvalue='0'):
    ''' Take a bytes object, return an iterable that will iterate in chunks of query_size. '''

    args = [iter(data)] * query_size
    return zip_longest(*args, fillvalue=fillvalue)


def string_cleaner(data):
    ''' The tbl file format has blocks allocated for string data. If the data doesn't fill the full block, it will be
        padded with 00s. These 00s must be removed. Strip functions won't work because 00 is not a whitespace character. '''

    # Create a list to hold the data without the 00s.
    data_clean = []

    for chunk in chunker(data, 2):
        if chunk != (0, 0):
            data_clean.append(chr(chunk[0]))

    # Convert the list back to a string
    clean_data_str = ''.join(data_clean)  # Convert

    # Return the string
    return (clean_data_str)

