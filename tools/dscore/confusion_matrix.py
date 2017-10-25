#!/usr/bin/env python
"""Print confusion matrix between reference and system diarization at frame
level.

To print the confusion matrix between the frame-level labeling corresponding to
a system RTTM file ``sys.rttm`` and a corresponding gold standard RTTM
``ref.rttm``:

    python confusion_matrix.py ref.rttm sys.rttm

By default this will output raw frequencies so that the ``i,j``-th cell
contains the total number of times that the ``i``-th reference class was
assigned to the ``j``-th system class. Alternately, the ``--norm`` flag may be
invoked so that each row is normalized to sum to 1:

    python confusion_matrix.py --norm ref.rttm sys.rttm
"""
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys

import numpy as np
from tabulate import tabulate

from scorelib import __version__ as VERSION
from scorelib.logging import getLogger
from scorelib.metrics import contingency_matrix
from scorelib.score import rttm_to_turns, turns_to_frames

logger = getLogger()


# TODO: See if this can be subsumed under scorelib.scores.rttms_to_frames
#       without code becoming unreadable.
def rttms_to_frames(ref_rttm_fn, sys_rttm_fn, step=0.010):
    """Return frame-level labels corresponding to reference and system RTTMs.

    Parameters
    ----------
    ref_rttm_fn : str
        Path to reference RTTM file.

    sys_rttm_fn : str
        Path to system RTTM file.

    step : float, optional
        Frame step size  in seconds.
        (Default: 0.01)

    Returns
    -------
    ref_labels : ndarray, (n_frames,)
        Frame-level labels corresponding to reference RTTM.

    sys_labels : ndarray, (n_frames,)
        Frame-level labels corresponding to system RTTM.
    """
    # Load turns from RTTMs.
    ref_rec_id_to_turns = rttm_to_turns(ref_rttm_fn)
    sys_rec_id_to_turns = rttm_to_turns(sys_rttm_fn)
    ref_labels = []
    sys_labels = []
    max_ref_label = max_sys_label = 0
    rec_ids = sorted(set(ref_rec_id_to_turns.keys()) &
                     set(sys_rec_id_to_turns.keys()))
    if len(rec_ids) != 1:
        raise ValueError('RTTM contains more than one file.')

    # Determine correct duration.
    ref_turns = list(ref_rec_id_to_turns.values())[0]
    sys_turns = list(sys_rec_id_to_turns.values())[0]
    ref_dur = max(turn.offset for turn in ref_turns)
    sys_dur = max(turn.offset for turn in sys_turns)
    dur = min(ref_dur, sys_dur)

    # Convert to frame-level labelings.
    ref_labels = turns_to_frames(ref_turns, dur, step, as_string=True)
    sys_labels = turns_to_frames(sys_turns, dur, step, as_string=True)

    return ref_labels, sys_labels


def print_cm(cm, ref_classes, sys_classes, norm=True):
    """Print confusion_matrix.

    Parameters
    ----------
    cm : ndarray, (n_ref_classes, n_sys_classes)
        Contingency table between reference and system labelings.

    ref_classes : ndarray, (n_ref_classes,)
        Reference classes.

    sys_classes : ndarray, (n_sys_classes,)
        System classes.

    norm : bool, optional
        If True, normalize rows of confusion matrix to sum to 1.
        (Default: False)
    """
    cm, ref_classes, sys_clases = contingency_matrix(ref_labels, sys_labels)
    if norm:
        marginals = cm.sum(axis=1, dtype='float64')
        cm = cm / np.expand_dims(marginals, axis=1)
    cm = cm.tolist()
    for ii, label in enumerate(ref_classes):
        cm[ii].insert(0, label)
    logger.info(tabulate(cm, headers=[''] + list(sys_classes)))


if __name__ == '__main__':
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description='Score RTTM.', add_help=True,
        usage='%(prog)s [options] ref_rttm sys_rttm')
    parser.add_argument(
        'ref_rttm', nargs=None, help='reference RTTM')
    parser.add_argument(
        'sys_rttm', nargs=None, help='system RTTM')
    parser.add_argument(
        '--step', nargs=None, default=0.010, type=float, metavar='FLOAT',
        help='step size in seconds (Default: %(default)s)')
    parser.add_argument(
        '--norm', action='store_true', default=False,
        help='normalize rows')
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s ' + VERSION)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    ref_labels, sys_labels = rttms_to_frames(
        args.ref_rttm, args.sys_rttm, args.step)
    cm, ref_classes, sys_classes = contingency_matrix(ref_labels, sys_labels)
    print_cm(cm, ref_classes, sys_classes, args.norm)
