# I. Overview
This suite supports evaluation of the output of diarization systems relative to a gold standard subject to the following assumptions:

- both reference and system diarizations are saved as [RTTM](https://catalog.ldc.upenn.edu/docs/LDC2004T12/RTTM-format-v13.pdf) files
- within an RTTM file, for any two recordings the sets of speakers are disjoint


# II. Dependencies
The following are required to run this software:

- Python >= 2.7.1 (https://www.python.org/)
- NumPy >= 1.6.1 (https://github.com/numpy/numpy)
- SciPy >= 0.10.0 (https://github.com/scipy/scipy)
- tabulate >= 0.5.0 (https://pypi.python.org/pypi/tabulate)


# III. Metrics
## Diarization error rate
Following tradition in this area, we report diarization error rate (DER), which
 is the sum of

- speaker error  --  percentage of scored time for which the wrong speaker id
  is assigned within a speech region
- false alarm speech  --   percentage of scored time for which a nonspeech
  region is incorrectly marked as containing speech
- missed speech  --  percentage of scored time for which a speech region is
  incorrectly marked as not containing speech

As with word error rate, a score of zero indicates perfect performance and
higher scores (which may exceed 100) indicate poorer performance.

Typically, DER is computed using various exclusions, which have the effect of
juicing the scores. For instance, systems are not scored within 250 ms of
each reference segment boundary, with the effect that segments under 500 ms in
duration aren't scored at all. Nor does scoring consider regions of overlapping
speech in the reference diarization.

## Clustering metrics
An alternate approach to system evaluation is convert both the reference and
system outputs to frame-level labels, then evaluate using one of many
well-known approaches for evaluating clustering performance. Each recording
is converted to a sequence of 10 ms frames, each of which is assigned a single
label correponding to one of the following cases:

- the frame contains no speech
- the frame contains speech from a single speaker (one label per speaker
  indentified)
- the frame contains overlapping speech (one label for each element in the
  powerset of speakers)

These frame-level labelings are then scored with the following metrics:

### Goodman-Kruskal tau
Goodman-Kruskal tau is an asymmetric association measure dating back to work by Leo Goodman and William Kruskal in the 1950s (Goodman and Kruskal, 1954). For a reference labeling ``ref`` and a system labeling ``ref``, ``GKT(ref, sys)`` corresponds to the fraction of variability in ``ref`` that can be explained by ``sys``. Consequently, ``GKT(ref, sys)`` is 1 when ``ref`` is perfectly predictive of ``sys`` and 0 when it is not predictive at all. Correspondingly, ``GKT(sys, ref)`` is 1 when ``sys`` is perfectly predictive of ``ref`` and 0 when lacking any predictive power.

### B-cubed precision, recall, and F1
The B-cubed precision for a single frame assigned speaker ``S`` in the reference diarization and ``C`` in the system diarization is the proportion of frames assigned ``C`` that are also assigned ``S``. Similarly, the B-cubed recall for a frame is the proportion of all frames assigned ``S`` that are also assigned ``C``. The overall precision and recall, then, are just the mean of the frame-level precision and recall measures and the overall F-1 their harmonic mean. For additional details see Bagga and Baldwin (1998).

### Information theoretic measures
We report three information theoretic measures:

- conditional entropy of the reference labeling given the system labeling (bits)
- mutual information between the reference and system labelings (bits)
- normalized mutual information between the reference and system labelings (bits)


# IV. Scoring a single file
To evaluate system output stored in an [RTTM](https://catalog.ldc.upenn.edu/docs/LDC2004T12/RTTM-format-v13.pdf) file ``sys.rttm`` against a corresponding gold standard RTTM ``ref.rttm``:

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

 For additional details consult the docstring of ``score.py``.


# V. Scoring a batch of files
To evaluate system output stored in RTTM files in the directory ``sys_dir`` against reference RTTM files stored in the directory ``ref_dir`` and write the output to a file ``scores.df``:

    python score_batch.py scores.df ref_dir sys_dir

This will scan both ``ref_dir`` and ``sys_dir`` for files with the ``.rttm`` extension, score each file found in both directories, and write the scores to a tab-delimited file suitable for reading into R as a dataframe containing the following columns:

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

 Alternately, the file ids could have been specified explicitly via a script file of ids (one per line) using the ``-S`` flag:

    python score_batch.py -S all.scp scores.df ref_dir sys_dir

 For additional details consult the docstring of ``score.py``.


# VI. Printing confusion matrix for a single file

To print the confusion matrix between the frame-level labeling corresponding to
a system RTTM file ``sys.rttm`` and a corresponding gold standard RTTM ``ref.rttm``:

    python confusion_matrix.py ref.rttm sys.rttm

By default this will output raw frequencies so that the ``i,j``-th cell contains the
total number of times that the ``i``-th reference class was assigned to the ``j``-th
system class. Alternately, the ``--norm`` flag may be invoked so that each row is normalized
to sum to 1:

    python confusion_matrix.py --norm ref.rttm sys.rttm


# VII. References
- Bagga, A. and Baldwin, B. (1998). "Algorithms for scoring coreference
  chains." Proceedings of LREC 1998.
- Goodman, L.A. and Kruskal, W.H. (1954). "Measures of association for
  cross classifications." Journal of the American Statistical Association.
- Pearson, R. (2016). GoodmanKruskal: Association Analysis for Categorical
  Variables. https://CRAN.R-project.org/package=GoodmanKruskal.
