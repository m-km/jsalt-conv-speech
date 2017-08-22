#!/usr/bin/env python
"""Score diarization system output.

To evaluate system output stored in an RTTM file ``sys.rttm`` against a
corresponding gold standard RTTM ``ref.rttm``:

    python score.py ref.rttm sys.rttm

which will calculate and report the following metrics:

- diarization error rate (DER)
- B-cubed precision
- B-cubed recall
- B-cubed F1
- Goodman-Kruskal tau in the direction of the reference diarization to the
  system diarization (GKT(ref, sys))
- Goodman-Kruskal tau in the direction of the system diarization to the
  reference diarization (GKT(sys, ref))
- conditional entropy of the reference diarization given the system
  diarization in bits (H(ref|sys))
- mutual information in bits (MI)
- normalized mutual information (NMI)

Diarization error rate (DER) is scored using the NIST ``md-eval.pl`` tool
using a default collar size of 250 ms and ignoring regions that contain
overlapping speech in the reference RTTM. If desired, this behavior can be
altered using the ``--collar`` and ``--score_overlaps`` flags. For instance

    python --collar 0.100 --score_overlaps score.py ref.rttm sys.rttm

would compute DER using a 100 ms collar and with overlapped speech included.

All other metrics are computed off of frame-level labelings created from the
turns in the RTTM files **WITHOUT** any use of collars. The default frame
step is 10 ms, which may be altered via the ``--step`` flag. 
"""
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys

from scorelib import __version__ as VERSION
from scorelib.logging import getLogger
from scorelib.score import score

logger = getLogger()


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
        '--collar', nargs=None, default=0.250, type=float, metavar='FLOAT',
        help='collar size in seconds for DER computaton '
             '(Default: %(default)s)')
    parser.add_argument(
        '--score_overlaps', action='store_false', default=True,
        dest='ignore_overlaps',
        help='score overlaps when computing DER')
    parser.add_argument(
        '--step', nargs=None, default=0.010, type=float, metavar='FLOAT',
        help='step size in seconds (Default: %(default)s)')
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s ' + VERSION)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    metrics = score(args.ref_rttm, args.sys_rttm, args.collar,
                    args.ignore_overlaps, args.step)
    logger.info('DER: %.2f' % metrics[0])
    logger.info('B-cubed precision: %.2f' % metrics[1])
    logger.info('B-cubed recall: %.2f' % metrics[2])
    logger.info('B-cubed F1: %.2f' % metrics[3])
    logger.info('GKT(ref, sys): %.2f' % metrics[4])
    logger.info('GKT(sys, ref): %.2f' % metrics[5])
    logger.info('H(ref|sys): %.2f' % metrics[6])
    logger.info('MI: %.2f' % metrics[7])
    logger.info('NMI: %.2f' % metrics[8])
