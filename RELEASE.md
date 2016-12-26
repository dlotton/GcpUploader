Garmin Uploader Release Notes
==============================

Maintained by [Bastien Abadie](https://github.com/La0)

Version 1.0.0
-------------

Major refactoring from [GCPUploader](https://github.com/dlotton/GcpUploader) source code:

 * Supports new Garmin authentication (SSO)
 * Split code in small classes
 * Support Python 2.7 & Python 3.5
 * Add unit tests, run by Travis CI


Garmin Connect Python Uploader Release Notes
============================================

Maintained by [Dave Lotton](https://github.com/dlotton)

Release 2015.02.28:
  Comments:
  Error when using credentials from a config file caused by incorrect 
  variable name in gupload.py.  This was caused in the major rearrangement
  and feature adds to code in gupload.py in the last release.

  Changes:
  1) fixed variable name in gupload.py
  
Release 2015.02.21:
  Comments:
  Garmin Connect has made some changes whic has broken login again.  Some 
  features have been added to allow setting of activity type, and multiple 
  file upload,
  
  Changes:
  1) fix broken login (change URLs from http: to https:)
  2) add feature to set activity type 
  3) add feature to upload multiple files
  4) add feature to upload miltiple files specified in csv file
 
  
Release 2014.03.01:
  Comments:
  Garmin Connect completley chaged their login authentication scheme rendering
  Gcp completely inoperable.  Code from another open source project was 
  leveraged to get authorization working again.  

  Changes:
  1) Python package 'requests' is now required.
  2) Minor change to gupload.py to pass logging level to UploadGarmin.py
  3) Major overhaul of UploadGarmin.py leveraging heavily from Tapiriik project
     (https://github.com/cpfair/tapiriik) for the new authentication scheme.
  4) License for new UploadGarmin.py was changed to Apache 2.0 to match the
     source from which work was heavily leveraged.
  4) MultipartPostHandler.py no longer required. Remove from project.

Release 2014.02.16:
  Comments:
  Something changed with the Garmin Connect web site causing uploads to fail.
  They are now particular about the order of parts in the Multi-part post.
  Specifically, they want the filename as the first part of the multi-part
  post.
  
  Changes:
  1) UploadGarmin.py now give better information if an upload fails
  2) MultipartPostHandler.py now outputs the filename part first.

Release 2012.05.05:
  Comments:
  Fixed issue where script failed if user's Garmin Connect display name was 
  not the same as their login name.  Garmin Connect returns the user's 
  display name as the 'username' instead of the login name.  Most people using
  the script apparently never change their display name, which defaults to the
  user's login name.
  
  Changes:
  1) UploadGarmin.py now just verifies that the username JSON response to the 
     login transaction is not empty instead of comparing it to the login name.
     It was first verified that the user cannot change their display name to 
     an empty string in Garmin Connect, which would indicate a failed login 
     with the new scheme.

Release 2012.11.11:
  Comments:
  There have been no changes to the functionality of GcpUploader. It was
  merely converted to a python package that can be installed using pip
  package manager.  Pip is the replacement for Python easy_install.  The
  new package 'GcpUploader' is hosted at http://pypi.python.org/pypi. See 
  README.txt for installation details.

  Changes:
  1) Converted project to a pip installable project (no functional changes)
  2) Changed versioning schema for compatability with pypi version system.  
     Versioning schema is now year.month.day[.subrelease].

Release 20120516:
  Comments:
  Fixed a problem where binary FIT files did not upload successfully to Garmin 
  Connect in Windows.  

  Changes:
  1)  In UploadGarmin.py when uploading .FIT files, open files in 'rb' (read 
      binary) mode.  In Python under Windows there is an important distinction
      between opening files in binary and txt modes.  

Release 20120129:
  Comments:
  No real change of features.  Mostly code cleanup.  

  Changes:
  1)  Obscure password when printing verbose output. This will reduce the 
      chance of users unintentionally disclosing their password.
  2)  When no credentials are given on the command line and no config file is
      present, print the locations that were searched for the config file.
  3)  Added text to help explaining the meaning of various STATUS outputs.
  4)  Removed redundant os.path.expanduser() statement in line 112. 


Release 20120121:
  Initial Release
