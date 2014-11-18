# -*- coding: utf-8 -*-
"""
CSS bindings to ObsPy event module.

:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import os

import numpy as np

from obspy import UTCDateTime


def writeCSS(catalog, filename, **kwargs):
    """
    Writes a Catalog to a CSS database.

    .. note::
        Because CSS stores data in multiple files, you cannot write to a
        file-like object. You should specify the basename of the CSS database
        only.

    .. warning::
        This function should NOT be called directly, it registers via the
        the :meth:`~obspy.core.event.Catalog.write` method of an
        ObsPy :class:`~obspy.core.event.Catalog` object, call this instead.

    :type catalog: :class:`~obspy.core.event.Catalog`
    :param catalog: The ObsPy Catalog object to write.
    :type filename: str
    :param filename: Filename to write.
    """

    if not isinstance(filename, (str, native_str)):
        raise ValueError('Writing a Catalog to a file-like object in CSS '
                         'format is unsupported.')

    arrival = []
    assoc = []
    event = []
    netmag = []
    origerr = []
    origin = []
    remark = []
    sregion = []
    stamag = []
    stassoc = []
    lddate = (catalog.creation_info.creation_time if catalog.creation_info else UTCDateTime()).strftime('%Y-%m-%dT%H%M%S')
    for ev in catalog:
        arrival_line = '%-6s %17.5f %8d %8d %8d %8d %-8s %-8s %-1s %6.3f %7.2f %7.2f %7.2f %7.2f %7.2f %7.3f %10.1f %7.2f %7.2f %-1s %-2s %10.2f %-1s %-15s %8d %-17s' % (
            # sta
            # time
            # arid
            # jdate
            # stassid
            # chanid
            # chan
            # iphase
            # stype
            # deltim
            # azimuth
            # delaz
            # slow
            # delslo
            # ema
            # rect
            # amp
            # per
            # logat
            # clip
            # fm
            # snr
            # qual
            # auth
            # commid
            lddate)
        assoc_line = '%8d %8d %-6s %-8s %4.2f %8.3f %7.2f %7.2f %-1s %7.1f %-1s %7.2f %-1s %7.1f %6.3f %-15s %8d %-17s' % (
            # arid
            # orid
            # sta
            # phase
            # belief
            # delta
            # seaz
            # esaz
            # timeres
            # timedef
            # azres
            # azdef
            # slores
            # slodef
            # emares
            # wgt
            # vmodel
            # commid
            lddate)
        event_line = '%8d %-15s %8d %-15s %8d %-17s' % (
            # evid
            # evname
            # prefor
            # auth
            # commid
            lddate)
        netmag_line = '%8d %-8s %8d %8d %-6s %8d %7.2f %7.2f %-15s %8d %-17s' % (
            # magid
            # net
            # orid
            # evid
            # magtype
            # nsta
            # magnitude
            # uncertainty
            # auth
            # commid
            lddate)
        origerr_line = '%8d %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 %9.4f %9.4f %9.4f %6.2f %9.4f %8.2f %5.3f %8d %-17s' % (
            # orid
            # sxx
            # syy
            # szz
            # stt
            # sxy
            # sxz
            # syz
            # stx
            # sty
            # stz
            # sdobs
            # smajax
            # sminax
            # strike
            # sdepth
            # stime
            # conf
            # commid
            lddate)
        remark_line = '%8d %8d %-80s %-17s' % (
            # commid
            # lineno
            # remark
            lddate)
        stamag_line = '%8d %-6s %8d %8d %8d %-8s %-6s %7.2f %7.2f %-15s %8d %-17s' % (
            # magid
            # sta
            # arid
            # orid
            # evid
            # phase
            # magtype
            # magnitude
            # uncertainty
            # auth
            # commid
            lddate)
        stassoc_line = '%8d %-6s %-7s %-32s %7.2f %7.2f %9.4f %9.4f %9.4f %17.5f %7.2f %7.2f %7.2f %-15s %8d %-17s' % (
            # stassid
            # sta
            # etype
            # location
            # dist
            # azimuth
            # lat
            # lon
            # depth
            # time
            # imb
            # ims
            # iml
            # auth
            # commid
            lddate)
        for orig in ev:
            origin_line = '%9.4f %9.4f %9.4f %17.5f %8d %8d %8d %4d %4d %4d %8d %8d %-7s %9.4f %-1s %7.2f %8d %7.2f %8d %7.2f %8d %-15s %-15s %8d %-17s' % (
                orig.latitude,
                orig.longitude,
                orig.depth / 1000.0,
                orig.time,
                # orid
                # evid
                # jdate
                # nass
                # ndef
                # ndp
                # grn
                # srn
                # etype
                # depdp
                # dtype
                # mb
                # mbid
                # ms
                # msid
                # ml
                # mlid
                # algorithm
                # auth
                # commid
                lddate)


# algorithm
# amp
# arid
# auth
# azdef
# azimuth
# azres
# belief
# chan
# chanid
# clip
# commid
# conf
# delaz
# delslo
# delta
# deltim
# depdp
# depth
# dist
# dtype
# ema
# emares
# esaz
# etype
# evid
# evname
# fm
# grn
# imb
# iml
# ims
# iphase
# jdate
# lat
# lineno
# location
# logat
# lon
# magid
# magnitude
# magtype
# mb
# mbid
# ml
# mlid
# ms
# msid
# nass
# ndef
# ndp
# net
# nsta
# orid
# per
# phase
# prefor
# qual
# rect
# remark
# sdepth
# sdobs
# seaz
# slodef
# slores
# slow
# smajax
# sminax
# snr
# srn
# sta
# stassid
# stime
# strike
# stt
# stx
# sty
# stype
# stz
# sxx
# sxy
# sxz
# syy
# syz
# szz
# time
# timedef
# timeres
# uncertainty
# vmodel
# wgt
    for data, name in [(arrival, 'arrival'), (assoc, 'assoc'),
                       (event, 'event'), (gregion, 'gregion'),
                       (origerr, 'origerr'), (origin, 'origin'),
                       (netmag, 'netmag'), (remark, 'remark'),
                       (sregion, 'sregion'), (stamag, 'stamag'),
                       (stassoc, 'stassoc')]:
        if data:
            with open(filename + '.' + name, 'wt') as fh:
                fh.write('\n'.join(data))
                fh.write('\n')
