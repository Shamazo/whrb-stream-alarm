# Deadair alarm for WHRB
This script was written by Hamish Nicholson (/koala) in June 2019 and updated in August 2020.
If it detects silence in any two consecutive 30 second blocks of the stream
then it sends out a slack to the #emergencies whrb channel


##						WARNING!!!!
This DOES NOT detect every possible failure path at WHRB. For example
if we have issues with the transmitter, such as the microwave transmiter
on smith going down this will not detect it. This only detects dead air as
a result of issues in the studio. It is also entirely possible that the 
stream could be broadcasting deadair and the FM broadcast is fine. 
This is to be used as one of many debugging/warning tools.

## Installation 
This script requires pydub which also relies on ffmpeg.
See the local installation instructions here https://github.com/jiaaro/pydub. On Heroku we use a buildpack to install FFMPEG, see .buildpacks.

## Where does this run?
Previously we ran this on a raspberry pi in studio AC. However, we found the pi was unreliable due to connectivity issues (things have a habit of getting accidentally unplugged in AC) and ensuring the script as always running. This now runs in the cloud on Heroku. It is running on my personal account using the free tier. This Git repo is connected to Heroku, so we can easily deploy changes to the code. The configuration file for Heroku is Procfile. 

Any interested WHRBies should slack/email me if they want to know more about how this works.
  


