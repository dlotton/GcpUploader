This project is no longer maintained, you can use this upto date fork instead https://github.com/La0/garmin-uploader


---------------------------------------------

LICENSE:

File: gupload.py 
License: GNU General Public License (GPL)

File: UploadGarmin.py
License: Apache 2.0


DISCLAIMER:

# THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM 
# 'AS IS' WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR 
# IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE 
# ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM 
# IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME 
# THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
# USE AT YOUR OWN RISK.


DESCRIPTION:

Garmin Connect Python Uploader, gupload.py, uploads files 
(.tcx, .gpx, and .fit files ) created by Garmin fitness 
devices to the http://connect.garmin.com web site.


REQUIREMENTS:
Tested on Python 2.6.5 under Linux and 2.7.2 under Windows XP.

Pip:  
pip is a tool for installing and managing Python packages, 
such as those found on Python Package Index(pypi).  It is
a replacement/enhancement for easy_install.  

Linux Pip Installation:
If you use and Ubuntu distro search for python-pip in your 
package browser.  Other distros my have a similar package. 
Otherwise, check out the following link.

http://www.pip-installer.org/en/latest/


Windows Pip Installation:
1) Download the last easy installer for Windows that fits your 
   installed python version: (download the .exe at the bottom 
   of http://pypi.python.org/pypi/setuptools ). Install it.
2) Add c:\Python2x\Scripts to the Windows path (replace 
   Python2x with the correct directory)
3) Open a NEW (!) DOS prompt. From there run 'easy_install pip'

http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows

Note that for Windows you MUST add your python 'scripts'
directory to your PATH environment variable.  


Required Python Modules: (automatically installed by pip)
logging
simplejson
requests

Garmin Connect Account:
You must already have a Garmin Connect account set up.  If you
don't have one, go to http://connect.garmin.com and create your
user account.  The login credentials for this account are 
required for uploading data to Garmin Connect.


INSTALL:

The following command should download and install GcpUploader...

Linux: 
sudo pip install GcpUploader


Win: 
pip install GcpUploader



Config File:
You may create a config file containing your Garmin Connect
username and password to eliminate the need to type it in 
on the command line.  WARNING!!! The username and password
are stored in clear text, WHICH IS NOT SECURE.  If you have 
concerns about storing your garmin connect username and 
password in an unsecure file, do not use this option.

Create a text file named .guploadrc (gupload.ini for Windows
users) containing the following:
[Credentials]
username=<username>
password=<password>

Replace <username> and <password> with your Garmin Connect
login credentials.  gupload.py looks for this file either in
your home directory (usually something like '/home/<username>' 
in Linux, or C:\Documents and Settings\<username>' in Windows)
, or in the current working directory (the directory you are 
in when you execute gupload.py).  See help below for priority 
information. 


HELP:

usage: gupload.py [-h] [-a A] [-t T] [-l L L] [-v {1,2,3,4,5}]
                  filename [filename ...]

A script to upload .TCX, .GPX, and .FIT files to the Garmin Connect web site.

positional arguments:
  filename        Path and name of file(s) to upload, list file name, or
                  directory name containing fitness files.

optional arguments:
  -h, --help      show this help message and exit
  -a A            Sets the activity name for the upload file. This option is
                  ignored if multiple upload files are given.
  -t T            Sets activity type for ALL files in filename list, except
                  files described inside a csv list file.
  -l L L          Garmin Connect login credentials '-l username password'
  -v {1,2,3,4,5}  Verbose - select level of verbosity. 1=DEBUG(most verbose),
                  2=INFO, 3=WARNING, 4=ERROR, 5= CRITICAL(least verbose).
                  [default=3]

    Status Output:
        The script will output a status for each upload file; Success, FAIL, or
  EXISTS.  Definitions are as follows: 

        SUCCESS = Garmin Connect indicated that the upload was successful.
        FAIL = Garmin Connect indicated there was a problem with the upload.
        EXISTS = Garmin Connect indicated that the workout already exists in
                 your account.

    Credentials:
        Username and password credentials may be placed in a configuration file 
        located either in the current working directory, or in the user's home
        directory.  WARNING, THIS IS NOT SECURE. USE THIS OPTION AT YOUR OWN
        RISK.  Username and password are stored as clear text in a file
        format that is consistent with Microsoft (r) INI files. 
    
        The configuration file must contain a [Credentials] section containing 
        'username' and 'password' entries.

        The name of the config file for non-windows platforms is '.guploadrc'
        for windows platforms the config file is named 'gupload.ini'.

        Example '.guploadrc' (or 'gupload.ini' for windows):
            [Credentials]
            username=<myusername>
            password=<mypassword>

        Replace <myusername> and <mypassword> above with your own login 
        credentials.

    Priority of credentials:
        Command line credentials take priority over config files, current 
        directory config file takes priority over a config file in the user's
        home directory.

    CSV List Files:
        A CSV (comma separated values) file can be created to associate files 
        with filename and file type information.  Each record (line) in the csv
        file consists of three fields (filename, name, type).  Fields are 
        separated by commas, and text containing spaces or special characters
        is quoted with double quotes (").  Empty fields may be left blank, but
        the field separators must be present.  THE FIRST LINE IN THE CSV FILE 
        DEFINES THE ORDER OF THE FIELDS AND *MUST* CONTAIN THE KEY WORDS
        'filename', 'name', and 'type'.  Most popular spreadsheet 
        programs can save files in CSV format, or files can be easily 
        constructed in your favorite text editor.
        
        Example 'file_list.csv':
            filename, name, type
            file1.tcx, "10K race", running
            file2.fit, "Training Run", running
            file3.fit, , swimming
        
        Example 'file_list2.csv' (note field order changed):
            name, filename, type
            "10K race", file1.tcx, running
            "Training Run", file2.fit, running
            , file3.fit, swimming
            
    Activity Types: 
        The following list of activity types should be valid for setting 
        your activity type on Garmin Connect...
        
        running, street_running, track_running, trail_running, 
        treadmill_running, cycling, cyclocross, downhill_biking, indoor_cycling,
        mountain_biking, recumbent_cycling, road_biking, track_cycling, 
        fitness_equipment, elliptical, , indoor_cardio, indoor_rowing, 
        stair_climbing, strength_training, hiking, swimming, lap_swimming, 
        open_water_swimming, walking, casual_walking, speed_walking, transition,
        swimToBikeTransition, bikeToRunTransition, runToBikeTransition, 
        motorcycling, other, backcountry_skiing_snowboarding, boating, 
        cross_country_skiing, driving_general, flying, golf, horseback_riding,
        inline_skating, mountaineering, paddling, resort_skiing_snowboarding, 
        rowing, sailing, skate_skiing, skating, snowmobiling, snow_shoe, 
        stand_up_paddleboarding, whitewater_rafting_kayaking, wind_kite_surfing.
        

    Examples:
        Upload file and set activty name:
            gupload.py -l myusername mypassword -a 'Run at park - 12/23' myfile.tcx

        Upload multiple files:
            gupload.py -l myusername mypassword myfile1.tcx myfile2.tcx myfile3.fit

        Upload multiple files and set activity type for all to running:
            gupload.py -l myusername mypassword -t "running" myfile1.tcx myfile2.tcx

        Upload files using config file for credentials and csv list file:
            gupload.py file_list.csv

        Upload file using config file for credentials, name file, verbose 
        output:
            gupload.py -v 1 -a 'Run at park - 12/23' myfile.tcx
    
