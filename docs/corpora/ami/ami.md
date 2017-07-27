The [AMI Meeting Corpus](http://groups.inf.ed.ac.uk/ami/corpus/) consists of 100 hours of meetings recorded at the University of Edinburgh in Scotland, Idiap in Switzerland, and the TNO Human Factors Research Institute in the Netherlands.


Recordings
----------
Recordings were made at 48 kHz from a combination of head mounted, lapel, and distant microphone arrays, then downsampled to 16 kHz for delivery. Unfortunately, while the delivery format is 16 kHz, 16 bit WAV files, the gain was set ridiculously at recording time, so the effective bit depth is much smaller.

On Bridges these recordings are located at 

    /pylon2/ci560op/nryant/data/AMI/amicorpus/*/audio/*.wav
    
with individual WAV files named using the following convention:

    <meeting id>.<channel>.wav

For a full listing of all WAV files along with their duration, sampling rate, and number of channels please consult [wav_files.tbl](./wav_files.tbl). This is a tab-delimited file with five columns:

- basename minus extension
- sample rate (Hz)
- number of channels (not always 1!)
- duration (seconds)
- absolute path on Bridges

### Edinburgh recording setup

- circular microphone array at center of table
  - 8 Sennheiser MK2E-P-C omni-directional microphones
  - 10 cm radius
- circular microphone array atend of table on side bordering screen
  - 8 Sennheiser MK2E-P-C omni-directional microphones
  - 10 cm radius
- head-mounted microphones
  - one per participant, so number varies meeting to meeting (typically 4)
  - Sennheiser ME 3-N
- lapel microphones
  - one per participant, so number varies meeting to meeting (typically 4)
  - Sennheiser MKE 2-EW

  
### Idiap recording setup
- circular microphone array at center of table
  - 8 microphones
- circular microphone array mounted on ceiling
  - 4 microphones
- binaural manikin at end of table
  - 2 channels
- 4 head-mounted microphones
  - one per participant


### TNO reording setup
- circular microphone array at center of table
  - 8 microphones
- linear microphone array mounted above screen
  - 10 microphones
- 4 head-mounted microphones
  - one per participant


Transcripts
-----------
- performed off of the head-mounted microphones
- initial segmentation done using energy-based speech activity detector
- full transcription manual: <http://groups.inf.ed.ac.uk/ami/corpus/Guidelines/speech-transcription-manual.v1.2.pdf>
 



Meeting ids
-----------
[[Taken from <http://groups.inf.ed.ac.uk/ami/corpus/meetingids.shtml>]]

AMI meeting IDs have the form

    [IETB][SNB][1-5][0-9]{4}[a-z]
    
which encodes, among other information, the meeting site, the scenario type of the meeting, and the order of the meeting within a multi-meeting series. More specifically, the parts that comprise a meeting ID have the following meaning:

- First character  --  Location, which is one of (I)diap, (E)dinburgh, or (T)NO.
- Second character  --  Meeting scenario, which is one
  - S  --  scenario-based using remote control design
  - N  --  naturally occurring
  - B  --  other scenario-based elicitation
- Four digit number  --  The meeting number, which is site-specific
  - 1000 series  --  Idiap
  - 2000 series  --  Edinburgh
  - 3000 series  --  TNO
- Final character  --  Indicates order of sub-meeting within a single meeting. If a meeting was not broken into submeetings, this character is optional.


Participant ids
---------------
[[Taken from <http://groups.inf.ed.ac.uk/ami/corpus/participantids.shtml>]]

AMI participant IDs have the form

    [MF][IET][EDO][0-9]{3}(PM | ID | ME | UID)?
    
which encodes the participant gender, native language, and the site at which they were recorded. More specifically, the parts that comprise a participant ID have the following meeting:

- First character  --  Gender, one of (M)ale or (F)emale
- Second character  --  Location, which is one of (I)diap, (E)dinburgh, or (T)NO.
- Third character  --  Native language, one of (E)nglish, (D)utch, or (O)ther
- Three digit number  --  Chosen to make a unique identifier
- (OPTIONAL) Final character sequence  --  For participants recoreded at TNO, the participant ID may optionally end in a two or three character sequence indicating their role in the meeting:
	- PM  --  project manager
	- ID  --  industrial designer
	- ME  --  marketing expert
	- UID  --  user interface designer
	 
**NOTE** that participant role is **ONLY**, and optionally, recorded for participants recorded at TNO. To determine the roles of other participants, you will need to consult

    corpusResources/meetings.xml
    
    
Meetings
--------
AMI is comprised of both naturalistic meeting data (non-scenario meetings) and elicited data (scenario meetings) in which participants play the roles of employees in a electronics company that are tasked with developing a new product.

### Scenario meetings

The bulk of AMI, 65 hours, consists of scenario meetings in which participants play the roles of employees in an electronics company tasked with designing a new television remote control. Participants were randomly assigned one of four roles to form a product group, which then meetings four times, each meeting dedicated to one of four distinguished design process phases:

- *Project kick-off*  --  consists of building a project team and getting acquainted with each other and the task.
- *Functional design*  -- the team sets the user requirements, the technical functionality, and the working design.
- *Conceptual design*  -- the team determines the conceptual specification for the components, properties, and materials to be used in the apparatus,
as well as the user interface.
- *Detailed design*  --  finalization of the look-and-feel and user interface and evaluation of the result

The relevant roles are:

- *Project manager (PM)*  --  coordinates the project
- *Marketing expert (ME)*  --  determines user requirements, watches market trends, and evaluates the prototype
- *User interface designer (UI)*  --  determines features and designs user interface
- *Industrial designer (ID)*  --  responsible for implementation

**NOTE** that none of the participants were professionally trained for design work or had prior experience in the roles to which they were assigned.

### Non-scenario meetings
The remaining 35 hours of AMI is composed of naturalistic meetings, though it is not clear to what extent the topics of these meetings were determined by participants. For a full list of the non-scenario meetings and a description of each, see: <http://groups.inf.ed.ac.uk/ami/corpus/nonscenariomeetings.shtml>.

Train/Dev/Test split
--------------------
| Division  | Meetings  | Duration (hours) | IDS   |
| --------  | --------  | ---------------- | ----  |
| Train     | 135       | 80.2             | [train.ids](./train.ids) |
| Dev       | 18        | 9.67             | [dev.ids](./dev.ids) |
| Test      | 16        | 9.06             | [test.ids](./test.ids) |
