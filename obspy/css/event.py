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
from future.utils import native_str

from obspy import UTCDateTime


def _add_remarks(node, commid, remark, lddate):
    if node.comments:
        this_commid = commid = commid + 1
        for lineno, comment in enumerate(node.comments):
            remark_line = '%8d %8d %-80.80s %-17.17s' % (
                this_commid,
                lineno + 1,
                comment.text.replace('\n', ' '),
                lddate)
            remark.append(remark_line)
    else:
        this_commid = -1

    return this_commid, commid


def _evname(ev):
    name = '-'
    for desc in ev.event_descriptions:
        if desc.type and desc.type == 'earthquake name':
            name = desc.text or '-'
    return name


def _auth(node):
    name = '-'
    try:
        info = node.creation_info
        name = info.author or info.agency or '-'
    except AttributeError:
        name = '-'
    return name


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

    arid = {}
    commid = 0
    evid = {}
    magid = {}
    orid = {}
    stassid = {}
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
    lddate = (catalog.creation_info.creation_time if catalog.creation_info
              else UTCDateTime()).strftime('%Y-%m-%dT%H%M%S')
    for ev in catalog:
        this_evid = evid.setdefault(ev.resource_id, len(evid) + 1)
        this_commid, commid = _add_remarks(ev, commid, remark, lddate)
        prefor = orid.setdefault(ev.preferred_origin().resource_id,
                                 len(orid) + 1)
        event_line = '%8d %-15.15s %8d %-15.15s %8d %-17.17s' % (
            this_evid,
            _evname(ev),
            prefor,
            _auth(ev),
            this_commid,
            lddate)
        event.append(event_line)

        for orig in ev:
            this_orid = orid.setdefault(orig.resource_id, len(orid) + 1)
            this_commid, commid = _add_remarks(orig, commid, remark, lddate)
            origin_line = ('%9.4f %9.4f %9.4f %17.5f %8d %8d %8d %4d %4d %4d '
                           '%8d %8d %-7.7s %9.4f %-1.1s %7.2f %8d %7.2f %8d '
                           '%7.2f %8d %-15.15s %-15.15s %8d %-17.17s') % (
                orig.latitude,
                orig.longitude,
                orig.depth / 1000.0,
                orig.time,
                this_orid,
                this_evid,
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
                _auth(orig),
                this_commid,
                lddate)
            origin.append(origin_line)

            # this_commid, commid = _add_remarks(?, commid, remark, lddate)
            this_commid = -1
            origerr_line = ('%8d %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 %15.4 '
                            '%15.4 %15.4 %15.4 %9.4f %9.4f %9.4f %6.2f %9.4f '
                            '%8.2f %5.3f %8d %-17.17s') % (
                this_orid,
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
                this_commid,
                lddate)
            origerr.append(origerr_line)

            for arr in orig.arrivals:
                this_arid = arid.setdefault(arr.resource_id, len(arid) + 1)
                this_commid, commid = _add_remarks(arr, commid, remark, lddate)
                arrival_line = ('%-6.6s %17.5f %8d %8d %8d %8d %-8.8s %-8.8s '
                                '%-1.1s %6.3f %7.2f %7.2f %7.2f %7.2f %7.2f '
                                '%7.3f %10.1f %7.2f %7.2f %-1.1s %-2.2s '
                                '%10.2f %-1.1s %-15.15s %8d %-17.17s') % (
                    # sta
                    # time
                    this_arid,
                    # jdate
                    # stassid
                    # chanid
                    # chan
                    # iphase
                    # stype
                    # deltim
                    arr.azimuth if arr.azimuth is not None else -1,
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
                    _auth(arr),
                    this_commid,
                    lddate)
                arrival.append(arrival_line)

                # this_commid, commid = _add_remarks(?, commid, remark, lddate)
                this_commid = -1
                assoc_line = ('%8d %8d %-6.6s %-8.8s %4.2f %8.3f %7.2f %7.2f '
                              '%-1.1s %7.1f %-1.1s %7.2f %-1.1s %7.1f %6.3f '
                              '%-15.15s %8d %-17.17s') % (
                    this_arid,
                    this_orid,
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
                    this_commid,
                    lddate)
                assoc.append(assoc_line)

                # this_commid, commid = _add_remarks(?, commid, remark, lddate)
                this_commid = -1
                stassoc_line = ('%8d %-6.6s %-7.7s %-32.32s %7.2f %7.2f %9.4f '
                                '%9.4f %9.4f %17.5f %7.2f %7.2f %7.2f '
                                '%-15.15s %8d %-17.17s') % (
                    # stassid
                    # sta
                    # etype
                    # location
                    # dist
                    arr.azimuth if arr.azimuth is not None else -1,
                    # lat
                    # lon
                    # depth
                    # time
                    # imb
                    # ims
                    # iml
                    # auth
                    this_commid,
                    lddate)

                if False:
                    this_magid = magid.setdefault(mag.resource_id,
                                                  len(magid) + 1)
                    # this_commid, commid = _add_remarks(?, commid, remark,
                    #                                    lddate)
                    this_commid = -1
                    stamag_line = ('%8d %-6.6s %8d %8d %8d %-8.8s %-6.6s '
                                   '%7.2f %7.2f %-15.15s %8d %-17.17s') % (
                        this_magid,
                        # sta
                        this_arid,
                        this_orid,
                        this_evid,
                        # phase
                        # magtype
                        # magnitude
                        # uncertainty
                        # auth
                        this_commid,
                        lddate)

                    # this_commid, commid = _add_remarks(?, commid, remark,
                    #                                    lddate)
                    this_commid = -1
                    netmag_line = ('%8d %-8.8s %8d %8d %-6.6s %8d %7.2f %7.2f '
                                   '%-15.15s %8d %-17.17s') % (
                        this_magid,
                        # net
                        this_orid,
                        this_evid,
                        # magtype
                        # nsta
                        # magnitude
                        # uncertainty
                        # auth
                        this_commid,
                        lddate)
                    netmag.append(netmag_line)

# algorithm
# amp
# auth
# azdef
# azres
# belief
# chan
# chanid
# clip
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
