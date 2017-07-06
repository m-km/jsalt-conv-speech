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
1. Propose Better Diarization Metrics [Mark] 
    * Tools to build diarization metric (different scripting methods) [Diana].
2. See how the proposed metrics affects DER for AMI [Sriram]
    * Do diarization (using DiarTK) for SDM1 and beamformed output (BeamformIt toolkit also available) [Matthew].  
    * A possiblity to run on more than 2 channels [Ken].
    * ivector based diarization [Jan].
    * Analyze the gold standards from AMI (with energy) [Ken].
    * Collar size experiments [Jan]
3. Understand iVector formulation for multi-channel. See http://www.ee.columbia.edu/~ronw/pubs/taslp2017-multichannel.pdf for motivation [Sriram]
    * Presentation on Monday afternooon 2pm [Mahesh]
4. Source Separation using oracle segmentation on SDM, get WER/DER [Jun]
    * Speech enhancement, generate audio back and send out [Lei]. 
    * Early work on Overlap speech detection and separation.
    * Early work on the use of IHM, Array-mics to dereverb, get WER, DER [Yu Ding].
5. ASR baselines on AMI [Neville]
    * Get setup locally on bridges [Mathew]
    * Rebuild the model in JHU.
    * Make a short presentation on Monday afternoon. [Mathew].
    * SDM first and then on to the IHM setup [Matthew]
    * Transfer Kaldi setup from JHU to Bridges [Neville]
6. Social Analysis  [Zhou]
    * AMI using gold transcriptions.
7. Homebank [Rajat] 
    * Look at the annotation. Speech activity detection confusion matrix may be ?
    * 159 manually handpicked and annotated. 
    * Diarization [Mark/Elika] 

Week2 goals:

Week3 goals:

Week4 goals:

Week5 goals:

Week6 goals:

