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

# Week1 goals:
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
    * Rebuild the model in JHU __[Matthew]__
    * Make a short presentation on Monday afternoon. __[Mathew]__.
    * SDM first and then on to the IHM setup __[Matthew]__
    * Transfer Kaldi setup from JHU to Bridges __[Neville]__
6. Social Analysis  __[Zhou]__
    * AMI using gold transcriptions.
7. Homebank __[Rajat]__ 
    * Look at the annotation. Speech activity detection confusion matrix may be ?
    * 159 manually handpicked and annotated. 
    * Diarization __[Mark/Elika]__ 

# Week2 goals:
1. Make Brno and JHU systems somewhat comparable __[Matthew]__
    * Attributing SAD errors __[Jan]__
    * Using SAD (Energy, Phonetic or ASR based) to reevaluate JHU DER __[Matthew]__
    * Investigate if SAD markers can be provided to the Brno system __[Jan]__

2. Evaluate JHU system for mismatched condition. Using MDM8 models on SDM1 __[Matthew]__

3. Speech enhancement __[Jun]__
    * Generate cleaned up audio files from denoising and dereverberation
    * Train and test using JHU setup with help from Matthew

4. Speaker Diarization __[Ken]__
    * Use Jun Du group's beamforming output to see if it can be used for diarization
    * More analysis on site/room characteristics with social analysis from Zhou

5. Social Analysis __[Zhou]__
    * Analyze dialog acts

5. Multi-channel processing __[Sriram]__
    * Generate synthetic 3-channel TIMIT data with different SNR __[Sriram]__
    * Train and test 2D and 3D CNN models using Keras/Kaldi (https://github.com/dspavankumar/keras-kaldi) __[Neville]__
    * 3D CNN model support and developing any new module needed __[Mahesh]__

6. HomeBank analysis __[Rajat]__
    * Document data being analyzed (copy of the VanDam corpus currently at /home/rkulshre/Vandam )
    * Diarization error rate baseline


Week3 goals:
1. Diarization - 
       * Brno system  without assumptions about the number of speakers [Jan].
       * Analyze why the error is so high from DiarTk/Brno/JHU. [Mark] 
       * Home Bank Diarization using DiarTk. [Rajat]. 
       * Using the GMM-SAD on Brno System [Jan].
       * Mismatch in i-vector training SDM1, IHM [Matthew].
       * i-vectors dumped [Matthew].
       * Brno system on bridges. [Jan].
       * Learning regression for system combination [Ken]

2. Documentation for corpora
      * AMI Corpus Documentation [Neville].
      * HomeBank Documention [Rajat].
      
3. SAD setup which can work on AMI (Not sure at the moment ?).

4. Speech Enhancement
     * Uniformly improving over all meetings (MDM). [Yu Ding].
     * SDM diarization results using DiarTk. 
     * SAD - GMM setup in Bridges [Matthew/Neville].
     * CGMM beamformer testing [Lei].

5. Social Analysis [Zhou]
    * Backchannel detection using text.
    * Frequency of backchannel.
    
6. ASR and multi-channel
    * TIMIT with 3-D models [Sriram].
    * Basic DNN/CNN on AMI [Sriram].
    * Complicated Keras models which work on multiple GPUs [Neville]. 
    
7. HomeBank [Rajath]
   * Classification of speakers. 
   
8. ADOS dataset [Mark, Neville].
   

   
Week4 goals:

Week5 goals:

Week6 goals:

