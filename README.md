# Deadair alarm for WHRB
This script was written by Hamish Nicholson (/koala) in June 2019
If it detects silence in any two consecutive 30 second blocks of the stream
then it sends out an email to the important @whrb emails
Additionally the recovery email for the gmail used here is tech@whrb.org

##						WARNING!!!!
This DOES NOT detect every possible failure path at WHRB. For example
if we have issues with the transmitter, such as the microwave transmiter
on smith going down this will not detect it. This only detects dead air as
a result of issues in the studio. It is also entirely possible that the 
stream could be broadcasting deadair and the FM broadcast is fine. 
This is to be used as one of many debugging/warning tools.

## Installation 
This script requires pydub which also relies on ffmpeg.
See the installation instructions here https://github.com/jiaaro/pydub
