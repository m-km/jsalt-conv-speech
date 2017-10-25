#!/usr/bin/env python
"""Score diarization system output for a batch of files and write to a
dataframe.

To evaluate system output stored in RTTM files in the directory ``sys_dir``
against reference RTTM files stored in the directory ``ref_dir`` and write
the output to a file ``scores.df``:

    python score_batch.py scores.df ref_dir sys_dir

This will scan both ``ref_dir`` and ``sys_dir`` for files with the ``.rttm``
extension, score each file found in both directories, and write the scores to
a tab-delimited file suitable for reading into R as a dataframe. Alternately,
the file ids could have been specified explicitly via a script file of ids
(one per line) using the ``-S`` flag:

    python score_batch.py -S all.scp scores.df ref_dir sys_dir

Minimally, the output dataframe has the following columns:

- FID  --  the file id
- DER  --  diarization error rate
- B3Precision  --  B-cubed precision
- B3Recall  --  B-cubed recall
- B3F1  --  B-cubed F1
- GKTRefSys  --  Goodman-Kruskal tau in the direction of the reference
  diarization to the system diarization
- GKTSysRef  --  Goodman-Kruskal tau in the direction of the system diarization
  to the reference diarization
- HRefSys  --  conditional entropy of the reference diarization given the
  system diarization (bits)
- MI  --  mutual information (bits)
- NMI  --  normalized mutual information (bits)

Optionally, it may contain additional columns specified via the
``--additional_columns`` flag, which takes a string containing semicolon
delimited column name/value pairs, each pair having the form:

    CNAME=VAL

For instance, the string

    Corpus=AMI;NClusters=4

would result in two additional columns, "Corpus" and "NClusters", being output
with the values "AMI" and 4 respectively in each row.

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
import glob
import os
import sys

from multiprocessing import Pool

from scorelib import __version__ as VERSION
from scorelib.logging import getLogger
from scorelib.score import score

logger = getLogger()


def _score_recordings(args):
    fid, ref_rttm_dir, sys_rttm_dir, collar, ignore_overlaps, step = args
    ref_rttm_fn = os.path.join(ref_rttm_dir, fid +'.rttm')
    sys_rttm_fn = os.path.join(sys_rttm_dir, fid + '.rttm')
    fail = False
    if not (os.path.exists(ref_rttm_fn)):
        logger.warn('Missing reference RTTM: %s. Skipping.' % sys_rttm_fn)
        fail = True
    if not (os.path.exists(ref_rttm_fn)):
        logger.warn('Missing system RTTM: %s. Skipping.' % sys_rttm_fn)
        fail = True
    if fail:
        return
    row = [fid]
    row.extend(score(ref_rttm_fn, sys_rttm_fn))
    return row


def score_recordings(fids, ref_rttm_dir, sys_rttm_dir, collar, ignore_overlaps,
                    step, n_jobs=1):
    """Score batch of recordings.

    Parameters
    ----------
    fid : list of str
        File ids.

    ref_rttm_dir : str
        Path to directory containing reference RTTM files.

    sys_rttm_dur : str
        Path to directory containing system RTTM files.

    collar : float, optional
        Size of forgiveness collar in seconds. Diarization output will not be
        evaluated within +/- ``collar`` seconds of reference speaker
        boundaries. Only relevant for computing DER.
        (Default: 0.250)

    ignore_overlaps : bool, optional
        If True, ignore regions in the reference diarization in which more
        than one speaker is speaking. Only relevant for computing DER.
        (Default: True)

    step : float, optional
        Frame step size  in seconds. Not relevant for computation of DER.
        (Default: 0.01)

    n_jobs : int, optional
        Number of threads to use.
        (Default: 1)
    """
    def args_gen():
        for fid in fids:
            yield (fid, ref_rttm_dir, sys_rttm_dir, collar, ignore_overlaps,
                   step)
    if n_jobs == 1:
        rows = [_score_recordings(args) for args in args_gen()]
    else:
        pool = Pool(n_jobs)
        rows = pool.map(_score_recordings, args_gen())
    rows = [row for row in rows if row]
    return rows


def write_dataframe(fn, rows, additional_columns=None, enc='utf-8'):
    """Write scores to dataframe.

    Parameters
    ----------
    fn : str
        Output dataframe.

    rows : list of tuple
        Rows of dataframe.

    additonal_columns : list of tuple, optional
        List of column name/value pairs specifying additional columns to be
        written.
        (Default: None)

    enc : str, optional
        Character encoding.
        (Default: 'utf-8')
    """
    with open(fn, 'wb') as f:
        def write_line(vals):
            vals = map(str, vals)
            line = '\t'.join(vals)
            f.write(line.encode(enc))
            f.write('\n')

        # Write header.
        col_names = ['DER', # Diarization error rate.
                     'B3Precision', # B-cubed precision.
                     'B3Recall', # B-cubed recall.
                     'B3F1', # B-cubed F1.
                     'TauRefSys', # Goodman-Kruskal tau ref --> sys.
                     'TauSysRef', # Goodman-Kruskal tau sys --> ref.
                     'CE', # H(ref | sys).
                     'MI', # Mutual information between ref and sys.
                     'NMI', # Normalized mutual information between ref/sys.
                    ]
        if additional_columns:
            col_names.extend(col_name for col_name, val in additional_columns)
        write_line(col_names)

        # Write rows.
        for row in rows:
            if additional_columns:
                row.extend(val for col_name, val in additional_columns)
            write_line(row)


def parse_additional_columns(spec_str):
    """Parse additional columns specification.

    The column specification should be a semicolon delimited list of column
    name/value pairs, each pair having the form

        CNAME=VAL

    For instance, the string

        Corpus=AMI;NClusters=4

    would be parsed as specifying two columns, "Corpus" and "NClusters",
    taking on the values "AMI" and 4 respectively.

    Parameters
    ----------
    spec_str : str
        Additional columns specificiation.

    Returns
    -------
    additional_columns : list of tuple
        List of column name/value pairs.
    """
    if spec_str == '':
        return []
    else:
        return [pair.split('=') for pair in spec_str.split(';')]


def _get_fids(ref_rttm_dir, sys_rttm_dir):
    ref_bns = [os.path.basename(fn)
               for fn in glob.glob(os.path.join(ref_rttm_dir, '*.rttm'))]
    sys_bns = [os.path.basename(fn)
               for fn in glob.glob(os.path.join(sys_rttm_dir, '*.rttm'))]
    bns = set(ref_bns) & set(sys_bns)
    return sorted([bn.replace('.rttm', '') for bn in bns])


if __name__ == '__main__':
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description='Score RTTMs.', add_help=True,
        usage='%(prog)s [options] scoresf ref_rttm_dir sys_rttm_dir')
    parser.add_argument(
        'scoresf', nargs=None, help='output dataframe')
    parser.add_argument(
        'ref_rttm_dir', nargs=None, help='reference RTTM directory')
    parser.add_argument(
        'sys_rttm_dir', nargs=None, help='system RTTM directory')
    parser.add_argument(
        '-S', nargs=None, default=None, metavar='FILE', dest='scpf',
        help='set script file (Default: None)')
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
        '--additional_columns', nargs=None, default='',
        help='additional columns')
    parser.add_argument(
        '-j', nargs=None, default=1, type=int, metavar='N', dest='n_jobs',
        help='set number of threads to use (Default: 1)')
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s ' + VERSION)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if args.scpf is not None:
        with open(args.scpf, 'rb') as f:
            fids = [line.strip() for line in f]
    else:
        fids = _get_fids(args.ref_rttm_dir, args.sys_rttm_dir)
    rows = score_recordings(
        fids, args.ref_rttm_dir, args.sys_rttm_dir, args.collar,
        args.ignore_overlaps, args.step, args.n_jobs)
    additional_columns = parse_additional_columns(args.additional_columns)
    write_dataframe(args.scoresf, rows, additional_columns)
