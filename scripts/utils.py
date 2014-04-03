#!/usr/bin/env python

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB']}

def convertSize(size, suffix, kilobyte_1024_bytes=True):
    '''Convert a file size to human-readable form.

    Keyword arguments:
    size                                     --      file size in bytes
    suffix                                  --      suffix to use for calculation, i.e: KB, GiB
    kilobyte_1024_bytes         --      if True (default), use multiples of 1024
                                                          if False, use multiples of 1000

    Returns: string

    '''

    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if kilobyte_1024_bytes else 1000
    exponent = SUFFIXES[multiple].index(suffix)
    
    size /= (multiple ** exponent)
    
    return '{0:.1f} {1}'.format(size, suffix)
