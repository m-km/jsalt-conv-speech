# High level goals

0. Document results in progress/report-week-__n__.md
1. Show that diarization metrics do not capture short turns, propose a new metric
2. Show relevance of processing multi-channel audio for speaker diarization
3. Show relevance of processing multi-channel audio for ASR by improving/using:
   * Speech Activity Detection
   * Speaker segmentation
   * Overlap detection
   * Source separation
4. How do we do on diarization in the wild (HomeBank)
5. Social analysis of overlap and speaker changes in conversational speech

## Corpus, Baseline Models and Tools
## Training and development
AMI corpus, using Kaldi models and baseline for AMI.

## Testing

# Subtasks
## Better Diarization Metrics
[Mark, Ken]



## Processing Multi-channel audio for better diarization
1. iVector generalization for multiple channels
2. Overlap detection

## Processing Multi-channel audio for better ASR
1. Source separation

## Diarization in the wild
1. HomeBank Analysis


## Social analysis

Week1 goals:
1. Propose Better Diarization Metrics __[Mark]__ 
    * Tools to build diarization metric (different scripting methods) __[Diana]__.
2. See how the proposed metrics affects DER for AMI __[Sriram]__
    * Do diarization (using DiarTK) for SDM1 and beamformed output (BeamformIt toolkit also available) __[Matthew]__.  
    * A possiblity to run on more than 2 channels __[Ken]__.
    * ivector based diarization __[Jan]__.
    * Analyze the gold standards from AMI (with energy) __[Ken]__.
    * Collar size experiments __[Jan]__
3. Understand iVector formulation for multi-channel. See http://www.ee.columbia.edu/~ronw/pubs/taslp2017-multichannel.pdf for motivation __[Sriram]__
    * Presentation on Monday afternooon 2pm __[Mahesh]__
4. Source Separation using oracle segmentation on SDM, get WER/DER __[Jun]__
    * Speech enhancement, generate audio back and send out __[Lei]__. 
    * Early work on Overlap speech detection and separation.
    * Early work on the use of IHM, Array-mics to dereverb, get WER, DER __[Yu Ding]__.
5. ASR baselines on AMI __[Neville]__
    * Get setup locally on bridges __[Mathew]__
    * Rebuild the model in JHU.
    * Make a short presentation on Monday afternoon. __[Mathew]__.
    * SDM first and then on to the IHM setup __[Matthew]__
    * Transfer Kaldi setup from JHU to Bridges __[Neville]__
6. Social Analysis  __[Zhou]__
    * AMI using gold transcriptions.
7. Homebank __[Rajat]__ 
    * Look at the annotation. Speech activity detection confusion matrix may be ?
    * 159 manually handpicked and annotated. 
    * Diarization __[Mark/Elika]__ 

Week2 goals:

Week3 goals:

Week4 goals:

Week5 goals:

Week6 goals:

