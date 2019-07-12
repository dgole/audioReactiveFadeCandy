# audioReactiveFadeCandy
This repo started by cloning https://github.com/scanlime/fadecandy.  
All underlying code (opc, fastopc, etc) is not mine.  
My additions are the ar, ledWall, bassGuitar, and musicTheory, and basement directories.  

# How this should be organized:
The ar (audio-reactive) directory contains tools and libraries to be used in the implementation of patterns.  
Each project or configuration of lights gets its own directory.  
Each directory should have:  
1. The .json file to configure the server.  
2. Some sort of patterns.py file that contains the patterns as functions.  
3. Some gui or script that implements the patterns.  
