"""Functions for scoring paired system/reference RTTM files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict

import numpy as np

from . import metrics

__all__ = ['rttm_to_turns', 'rttms_to_frames', 'score', 'turns_to_frames',
           'Turn']


class Turn(object):
    """Speaker turn.

    Parameters
    ----------
    speaker_id : str
        Speaker id.

    onset : float
        Turn onset in seconds.

    offset : float
        Turn offset in seconds.
    """
    def __init__(self, speaker_id, onset, offset):
        self.__dict__.update(locals())
        del self.self

    def __repr__(self):
        return ('Speaker: %s, Onset: %.2f, Offset: %.2f' %
                (self.speaker_id, self.onset, self.offset))


def rttm_to_turns(rttm_fn, enc='utf-8'):
    """Read turns from RTTM file.

    Parameters
    ----------
    rttm_fn : str
        Path to RTTM file.

    enc : str, optional
        Encoding.
        (Default: 'utf-8')

    Returns
    -------
    rec_id_to_turns : dict
        Mapping from recording ids to speaker turns.
    """
    with open(rttm_fn, 'rb') as f:
        rec_id_to_turns = defaultdict(list)
        for line in f:
            fields = line.strip().decode(enc).split()
            rec_id = fields[1]
            onset = float(fields[3])
            dur = float(fields[4])
            offset = onset + dur
            speaker_id = fields[7]
            rec_id_to_turns[rec_id].append(Turn(speaker_id, onset, offset))
    return dict(rec_id_to_turns)


def turns_to_frames(turns, dur=None, step=0.010, as_string=False):
    """Return frame-level labels corresponding to diarization.

    Parameters
    ----------
    turns : list of Turn
        Speaker turns.

    dur : float, optional
        Recording duration in seconds. If None, determined from ``turns``.
        (Default: None)

    step : float, optional
        Frame step size  in seconds.
        (Default: 0.01)

    as_string : bool, optional
        If True, returned frame labels will be strings that are the class
        names. Else, they will be integers.

    Returns
    -------
    labels : ndarray, (n_frames,)
        Frame-level labels.
    """
    onsets = [turn.onset for turn in turns]
    offsets = [turn.offset for turn in turns]
    speaker_ids = [turn.speaker_id for turn in turns]
    if dur is None:
        dur = max(offsets)

    # Create matrix whose i,j-th entry is True IFF the j-th speaker was
    # present at frame i.
    speaker_classes, speaker_class_inds = np.unique(
        speaker_ids, return_inverse=True)
    speaker_classes = np.concatenate([speaker_classes, ['non-speech']])
    n_frames = int(dur/step)
    X = np.zeros((n_frames, speaker_classes.size), dtype='bool')
    times = step*np.arange(n_frames)
    bis = np.searchsorted(times, onsets)
    eis = np.searchsorted(times, offsets)
    for bi, ei, speaker_class_ind in zip(bis, eis, speaker_class_inds):
        X[bi:ei, speaker_class_ind] = True
    is_nil = ~(X.any(axis=1))
    X[is_nil, -1] = True

    # Now, convert to frame-level labelings.
    pows = 2**np.arange(X.shape[1])
    labels = np.sum(pows*X, axis=1)
    if as_string:
        def to_binary(n):
            return [bool(int(x))
                    for x in np.binary_repr(n, speaker_classes.size)][::-1]
        label_classes = np.array(['_'.join(speaker_classes[to_binary(n)])
                                   for n in range(2**speaker_classes.size)])
        try:
            # Save some memory in the (majority of) cases where speaker ids are
            # ASCII.
            label_classes = label_classes.astype('string')
        except UnicodeEncodeError:
            pass
        labels = label_classes[labels]

    return labels


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
    ref_rec_id_to_turns = rttm_to_turns(ref_rttm_fn)
    sys_rec_id_to_turns = rttm_to_turns(sys_rttm_fn)
    ref_labels = []
    sys_labels = []
    max_ref_label = max_sys_label = 0
    rec_ids = sorted(set(ref_rec_id_to_turns.keys()) &
                     set(sys_rec_id_to_turns.keys()))
    for rec_id in rec_ids:
        # Determine recording duration.
        ref_turns = ref_rec_id_to_turns[rec_id]
        sys_turns = sys_rec_id_to_turns[rec_id]
        ref_dur = max(turn.offset for turn in ref_turns)
        sys_dur = max(turn.offset for turn in sys_turns)
        dur = min(ref_dur, sys_dur)

        # Determine labels, ensuring that frames from different recordings
        # have distinct labels.
        ref_labels_ = turns_to_frames(ref_turns, dur, step) + max_ref_label
        ref_labels.append(ref_labels_)
        max_ref_label = ref_labels_.max()
        sys_labels_ = turns_to_frames(sys_turns, dur, step) + max_sys_label
        sys_labels.append(sys_labels_)
        max_sys_label = sys_labels_.max()
    ref_labels = np.concatenate(ref_labels)
    sys_labels = np.concatenate(sys_labels)

    return ref_labels, sys_labels


def score(ref_rttm_fn, sys_rttm_fn, collar=0.250, ignore_overlaps=True,
          step=0.010, nats=False):
    """Score diarization.

    Parameters
    ----------
    ref_rttm_fn : str
        Path to reference RTTM file.

    sys_rttm_fn : str
        Path to system RTTM file.

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

    nats : bool, optional
        If True, use nats as unit for information theoretic metrics.
        Otherwise, use bits.
        (Default: False)

    Returns
    -------
    der : float
        Overall percent diarization error.

    bcubed_precision : float
        B-cubed precision.

    bcubed_recall : float
        B-cubed recall.

    bcubed_f1 : float
        B-cubed F1.

    tau_ref_sys : float
        Value between 0 and 1 that is high when the reference diarization is
        predictive of the system diarization and low when the reference
        diarization provides essentially no information about the system
        diarization.

    tau_sys_ref : float
        Value between 0 and 1 that is high when the system diarization is
        predictive of the reference diarization and low when the system
        diarization provides essentially no information about the reference
        diarization.

    ce : float
        Conditional entropy of the reference diarization given the system
        diarization.

    mi : float
        Mutual information.

    nmi : float
        Normalized mutual information.
    """
    der = metrics.der(ref_rttm_fn, sys_rttm_fn)
    ref_labels, sys_labels = rttms_to_frames(ref_rttm_fn, sys_rttm_fn, step)
    cm, _, _ = metrics.contingency_matrix(ref_labels, sys_labels)
    bcubed_precision, bcubed_recall, bcubed_f1 = metrics.bcubed(
        None, None, cm)
    tau_ref_sys, tau_sys_ref = metrics.goodman_kruskal_tau(
        None, None, cm)
    ce = metrics.conditional_entropy(None, None, cm, nats) # H(ref | sys)
    mi, nmi = metrics.mutual_information(None, None, cm, nats)
    return (der, bcubed_precision, bcubed_recall, bcubed_f1,
            tau_ref_sys, tau_sys_ref, ce, mi, nmi)
