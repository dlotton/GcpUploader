Garmin Uploader
===============

Garmin Uploader (aka gupload), uploads files 
(.tcx, .gpx, and .fit files ) created by Garmin fitness 
devices to the http://connect.garmin.com web site.

:star: Yes, it works with the latest (September 2016) Garmin connect authentication update.

This is an up to date version of [GCPUploader](https://github.com/dlotton/GcpUploader) by Dave Lotton. Thanks Dave for creating this tool :+1:

Requirements
------------

Tested on Python 2.7 and Python 3.5

[![Build Status](https://travis-ci.org/La0/garmin-uploader.svg?branch=master)](https://travis-ci.org/La0/garmin-uploader)

Install
-------

You can install garmin-uploader as any othe package availale on PyPi with pip:


On Linux
```
sudo pip install garmin-uploader
```

On Windows
```
pip install garmin-uploader
```

Required Python Modules: (automatically installed by pip)

 * requests
 * six


Garmin Connect Account
-----------------------
You must already have a Garmin Connect account set up.  If you
don't have one, go to https://connect.garmin.com and create your
user account.  The login credentials (username or email and password) for this account are 
required for uploading data to Garmin Connect.


Config File:
-----------
You may create a config file containing your Garmin Connect
username and password to eliminate the need to type it in 
on the command line.  

 :warning: WARNING!!! The username and password
are stored in clear text, WHICH IS NOT SECURE.  If you have 
concerns about storing your garmin connect username and 
password in an unsecure file, do not use this option.

Create a text file named .guploadrc (gupload.ini for Windows
users) containing the following:

```
[Credentials]
username=<username>
password=<password>
```

Replace <username> and <password> with your Garmin Connect
login credentials.  gupload looks for this file either in
your home directory (usually something like '/home/<username>' 
in Linux, or C:\Documents and Settings\<username>' in Windows)
, or in the current working directory (the directory you are 
in when you execute gupload).  See help below for priority 
information. 


Help
----

```
usage: cli.py [-h] [-a ACTIVITY_NAME] [-t ACTIVITY_TYPE] [-u USERNAME]
              [-p PASSWORD] [-v {1,2,3,4,5}]
                            paths [paths ...]

A script to upload .TCX, .GPX, and .FITfiles to the Garmin Connect web site.

positional arguments:
  paths                 Path and name of file(s) to upload, list file name, or
                        directoryname containing fitness files.

optional arguments:
  -h, --help            show this help message and exit
  -a ACTIVITY_NAME, --name ACTIVITY_NAME
                        Sets the activity name for the upload file. This
                        option isignored if multiple upload files are given.
  -t ACTIVITY_TYPE, --type ACTIVITY_TYPE
                        Sets activity type for ALL files in filename list,
                        except filesdescribed inside a csv list file.
  -u USERNAME, --username USERNAME
                        Garmin Connect user login
  -p PASSWORD, --password PASSWORD
                        Garmin Connect user password
  -v {1,2,3,4,5}, --verbose {1,2,3,4,5}
                        Verbose - select level of verbosity. 1=DEBUG(most
                        verbose), 2=INFO, 3=WARNING, 4=ERROR, 5=
                        CRITICAL(least verbose). [default=2]
```

Examples
--------
Upload file and set activity name:
```
gupload -u myusername -p mypassword -a 'Run at park - 12/23' myfile.tcx
```

Upload multiple files:
```
gupload -u myusername -p mypassword myfile1.tcx myfile2.tcx myfile3.fit
```

Upload multiple files and set activity type for all to running:
```
gupload -u myusername -p mypassword -t "running" myfile1.tcx myfile2.tcx
```

Upload files using config file for credentials and csv list file:
```
gupload file_list.csv
```

Upload file using config file for credentials, name file, verbose output:
```
gupload -v 1 -a 'Run at park - 12/23' myfile.tcx
```
