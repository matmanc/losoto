#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This operation for LoSoTo implement a smoothing function
# WEIGHH: flag ready

import logging
from losoto.operations_lib import *

logging.debug('Loading SMOOTH module.')

def run( step, parset, H ):

#    import scipy.ndimage.filters
    import numpy as np
    from losoto.h5parm import solFetcher, solWriter
    from scipy.ndimage import generic_filter

    soltabs = getParSoltabs( step, parset, H )

    axesToSmooth = parset.getStringVector('.'.join(["LoSoTo.Steps", step, "Axes"]), [] )
    size = parset.getIntVector('.'.join(["LoSoTo.Steps", step, "Size"]), [] )
    mode = parset.getString('.'.join(["LoSoTo.Steps", step, "Mode"]), "runningmedian" )
    degree = parset.getInt('.'.join(["LoSoTo.Steps", step, "Degree"]), 1 )

    if mode == "runningmedian" and len(axesToSmooth) != len(size):
        logging.error("Axes and Size lenghts must be equal for runningmedian.")
        return 1

    if mode == "runningpoly" and (len(axesToSmooth) != 1 or len(size) != 1):
        logging.error("Axes and size lenghts must be 1 for runningpoly.")
        return 1

    for i, s in enumerate(size):
        if s % 2 == 0:
            logging.warning('Size should be odd, adding 1.')
            size[i] += 1

    for soltab in openSoltabs( H, soltabs ):

        logging.info("Smoothing soltab: "+soltab._v_name)

        sf = solFetcher(soltab)
        sw = solWriter(soltab, useCache = True) # remember to flush!

        # axis selection
        userSel = {}
        for axis in sf.getAxesNames():
            userSel[axis] = getParAxis( step, parset, H, axis )
        sf.setSelection(**userSel)

        for i, axis in enumerate(axesToSmooth[:]):
            if axis not in sf.getAxesNames():
                del axesToSmooth[i]
                del size[i]
                logging.warning('Axis \"'+axis+'\" not found. Ignoring.')

        for vals, weights, coord, selection in sf.getValuesIter(returnAxes=axesToSmooth, weight=True):

            if mode == 'runningmedian':
                np.putmask(vals, weights==0, np.nan)
                valsnew = generic_filter(vals, np.nanmedian, size=size, mode='reflect')

            elif mode == 'runningpoly':
                def polyfit(data):
                    x = np.arange(len(data))[ data != 0]
                    y = data[ data != 0 ]
                    p = np.polynomial.polynomial.polyfit(x, y, deg=degree)
                    #import matplotlib as mpl
                    #mpl.use("Agg")
                    #import matplotlib.pyplot as plt
                    #plt.plot(x, y, 'ro')
                    #plt.plot(x, np.polyval( p[::-1], x ), 'k-')
                    #plt.savefig('test.png')
                    #sys.exit()
                    return np.polyval( p[::-1], (size[0]-1)/2 ) # polyval has opposite convention for polynomial order

                # flags and at edges pass 0 and then remove them
                vals_bkp = vals[ weights == 0 ]
                vals[ weights == 0 ] = 0
                valsnew = generic_filter(vals, polyfit, size=size[0], mode='constant', cval=0)
                valsnew[ weights == 0 ] = vals_bkp
                #print coord['ant'], vals, valsnew

            elif mode == 'median':
                valsnew = np.median( vals[(weights!=0)] )

            elif mode == 'mean':
                valsnew = np.mean( vals[(weights!=0)] )

            else:
                logging.error('Mode must be: runningmedian, runningpoly, median or mean')
                return 1

            sw.selection = selection
            sw.setValues(valsnew)

        sw.flush()
        sw.addHistory('SMOOTH (over %s with mode = %s)' % (axesToSmooth, mode))
        del sf
        del sw
    return 0


