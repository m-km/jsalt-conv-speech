"""Functions for scoring frame-level diarization output."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
import subprocess

import numpy as np
from scipy.sparse import coo_matrix

__all__ = ['bcubed', 'conditional_entropy', 'contingency_matrix', 'der',
           'goodman_kruskal_tau', 'mutual_information']


EPS = np.finfo(float).eps


def contingency_matrix(ref_labels, sys_labels):
    """Return contingency matrix between ``ref_labels`` and ``sys_labels``."""
    ref_classes, ref_class_inds = np.unique(ref_labels, return_inverse=True)
    sys_classes, sys_class_inds = np.unique(sys_labels, return_inverse=True)
    n_frames = ref_labels.size
    # Following works because coo_matrix sums duplicate entries. Is roughly
    # twice as fast as np.histogram2d.
    cmatrix = coo_matrix(
        (np.ones(n_frames), (ref_class_inds, sys_class_inds)),
        shape=(ref_classes.size, sys_classes.size),
        dtype=np.int)
    cmatrix = cmatrix.toarray()
    return cmatrix, ref_classes, sys_classes


def bcubed(ref_labels, sys_labels, cm=None):
    """Return B-cubed precision, recall, and F1.

    The B-cubed precision of an item is the proportion of items with its
    system label that share its reference label (Bagga and Baldwin, 1998).
    Similarly, the B-cubed recall of an item is the proportion pf items
    with its reference label that share its system label. The overall B-cubed
    precision and recall, then, are the means of the precision and recall for
    each item.

    Parameters
    ----------
    ref_labels : ndarray, (n_frames,)
        Reference labels.

    sys_labels : ndarray, (n_frames,)
        System labels.

    cm : ndarray, (n_ref_classes, n_sys_classes)
        Contingency matrix between reference and system labelings. If None,
        will be computed automatically from ``ref_labels`` and ``sys_labels``.
        Otherwise, the given value will be used and ``ref_labels`` and
        ``sys_labels`` ignored.
        (Default: None)

    Returns
    -------
    precision : float
        B-cubed precision.

    recall : float
        B-cubed recall.

    f1 : float
        B-cubed F1.

    References
    ----------
    Bagga, A. andBaldwin, B. (1998). "Algorithmsfor scoring coreference
    chains." Proceedings of LREC 1998.
    """
    if cm is None:
        cm, _, _ = contingency_matrix(ref_labels, sys_labels)
    cm = cm.astype('float64')
    cm_norm = cm / cm.sum()
    precision = np.sum(cm_norm * (cm / cm.sum(axis=0)))
    recall = np.sum(cm_norm * (cm / np.expand_dims(cm.sum(axis=1), 1)))
    f1 = 2*(precision*recall)/(precision + recall)
    return precision, recall, f1


def goodman_kruskal_tau(ref_labels, sys_labels, cm=None):
    """Return Goodman-Kruskal tau between ``ref_labels`` and ``sys_labels``.

    Parameters
    ----------
    ref_labels : ndarray, (n_frames,)
        Reference labels.

    sys_labels : ndarray, (n_frames,)
        System labels.

    cm : ndarray, (n_ref_classes, n_sys_classes)
        Contingency matrix between reference and system labelings. If None,
        will be computed automatically from ``ref_labels`` and ``sys_labels``.
        Otherwise, the given value will be used and ``ref_labels`` and
        ``sys_labels`` ignored.
        (Default: None)

    Returns
    -------
    tau_ref_sys : float
        Value between 0 and 1 that is high when ``ref_labels`` is predictive
        of ``sys_labels`` and low when ``ref_labels`` provides essentially no
        information about ``sys_labels``.

    tau_sys_ref : float
        Value between 0 and 1 that is high when ``sys_labels`` is predictive
        of ``ref_labels`` and low when ``sys_labels`` provides essentially no
        information about ``ref_labels``.

    References
    ----------
    - Goodman, L.A. and Kruskal, W.H. (1954). "Measures of association for
      cross classifications." Journal of the American Statistical Association.
    - Pearson, R. (2016). GoodmanKruskal: Association Analysis for Categorical
      Variables. https://CRAN.R-project.org/package=GoodmanKruskal.
    """
    if cm is None:
        cm, _, _ = contingency_matrix(ref_labels, sys_labels)
    cm = cm.astype('float64')
    cm = cm / cm.sum()
    ref_marginals = cm.sum(axis=1)
    sys_marginals = cm.sum(axis=0)

    # Tau(ref, sys).
    vy = 1 - np.sum(sys_marginals**2) + EPS
    xy_term = np.sum(cm**2, axis=1)
    vy_bar_x = 1 - np.sum(xy_term / ref_marginals)
    tau_ref_sys = (vy - vy_bar_x) / vy

    # Tau(sys, ref).
    vx = 1 - np.sum(ref_marginals**2) + EPS
    yx_term = np.sum(cm**2, axis=0)
    vx_bar_y = 1 - np.sum(yx_term / sys_marginals)
    tau_sys_ref = (vx - vx_bar_y) / vx

    return tau_ref_sys, tau_sys_ref


def conditional_entropy(ref_labels, sys_labels, cm=None, nats=False):
    """Return conditional entropy of ``ref_labels`` given ``sys_labels``.

    Parameters
    ----------
    ref_labels : ndarray, (n_frames,)
        Reference labels.

    sys_labels : ndarray, (n_frames,)
        System labels.

    cm : ndarray, (n_ref_classes, n_sys_classes)
        Contingency matrix between reference and system labelings. If None,
        will be computed automatically from ``ref_labels`` and ``sys_labels``.
        Otherwise, the given value will be used and ``ref_labels`` and
        ``sys_labels`` ignored.
        (Default: None)

    nats : bool, optional
        If True, return nats. Otherwise, return bits.
        (Default: False)
    """
    log = np.log if nats else np.log2
    if cm is None:
        cm, _, _ = contingency_matrix(ref_labels, sys_labels)
    sys_marginals = cm.sum(axis=0)
    N = cm.sum()
    n_sys = sys_marginals.sum()
    ref_inds, sys_inds = np.nonzero(cm)
    vals = cm[ref_inds, sys_inds] # Non-zero values of contingency matrix.
    sys_marginals = sys_marginals[sys_inds]
    sigma = vals/N * (
        log(sys_marginals) - log(vals) + log(N) - log(n_sys))
    return sigma.sum()


def mutual_information(ref_labels, sys_labels, cm=None, nats=False):
    """Return mutual information between ``ref_labels`` and ``sys_labels``.

    Parameters
    ----------
    ref_labels : ndarray, (n_frames,)
        Reference labels.

    sys_labels : ndarray, (n_frames,)
        System labels.

    cm : ndarray, (n_ref_classes, n_sys_classes)
        Contingency matrix between reference and system labelings. If None,
        will be computed automatically from ``ref_labels`` and ``sys_labels``.
        Otherwise, the given value will be used and ``ref_labels`` and
        ``sys_labels`` ignored.
        (Default: None)

    nats : bool, optional
        If True, return nats. Otherwise, return bits.
        (Default: False)

    Returns
    -------
    mi : float
        Mutual information.

    nmi : float
        Normalized mutual information.
    """
    log = np.log if nats else np.log2
    if cm is None:
        cm, _, _ = contingency_matrix(ref_labels, sys_labels)

    # Mutual information.
    N = cm.sum()
    ref_marginals = cm.sum(axis=1)
    sys_marginals = cm.sum(axis=0)
    ref_inds, sys_inds = np.nonzero(cm)
    vals = cm[ref_inds, sys_inds] # Non-zero values of contingency matrix.
    outer = ref_marginals[ref_inds]*sys_marginals[sys_inds]
    sigma = (vals/N) * (
        log(vals) - log(outer) + log(N))
    mi = sigma.sum()

    # Normalized mutual information.
    def h(p):
        p = p[p>0]
        return -np.sum(p*log(p))
    ref_marginals = ref_marginals / N
    sys_marginals = sys_marginals / N
    nmi = mi / np.sqrt(h(ref_marginals) * h(sys_marginals)  + EPS)

    return mi, nmi


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
MDEVAL_BIN = os.path.join(SCRIPT_DIR, 'md-eval-22.pl')
DER_REO = re.compile(r'(?<=OVERALL SPEAKER DIARIZATION ERROR = )[\d.]+')

def der(ref_rttm_fn, sys_rttm_fn, collar=0.250, ignore_overlaps=True):
    """Return overall diarization error rate as computed using NIST tool.

    **NOTE** that unlike other functions in ``scorelib.metrics``, ``der``
    does not take as input frame-level labelings, but instead paths to
    reference and system RTTM files, which are then given as arguments to the
    NIST ``md-eval.pl`` scoring tool to compute diarization error rate (DER).
    Currently, v22 of the scoring tool is used.

    Parameters
    ----------
    ref_rttm_fn : str
        Path to reference RTTM file.

    sys_rttm_fn : str
        Path to system RTTM file.

    collar : float, optional
        Size of forgiveness collar in seconds. Diarization output will not be
        evaluated within +/- ``collar`` seconds of reference speaker
        boundaries.
        (Default: 0.250)

    ignore_overlaps : bool, optional
        If True, ignore regions in the reference diarization in which more
        than one speaker is speaking.
        (Default: True)

    Returns
    -------
    der : float
        Overall percent diarization error.
    """
    cmd = [MDEVAL_BIN,
           '-r', ref_rttm_fn,
           '-s', sys_rttm_fn,
           '-c', str(collar),
           ]
    if ignore_overlaps:
        cmd.append('-1')
    with open(os.devnull, 'wb') as f:
        txt = subprocess.check_output(cmd, stderr=f)
    der = float(DER_REO.search(txt).group())
    return der
