import os.path
import glob
import csv
import time
from collections import namedtuple
from garmin_uploader import logger, VALID_GARMIN_FILE_EXTENSIONS
from garmin_uploader.user import User

Activity = namedtuple('Activity', ['filename', 'name', 'type'])


class Workflow():
    """
    Upload workflow:
     * List activities according to CLI args
     * Load user credentials
     * Authenticate user
     * Upload activities
    """

    def __init__(self, paths, username=None, password=None, activity_type=None, activity_name=None, verbose=3):
        self.last_request = None
        logger.setLevel(level=verbose * 10)

        self.activity_type = activity_type
        self.activity_name = activity_name

        # Load activities
        self.activities = self.load_activities(paths)

        # Load user
        self.user = User(username, password)


    def load_activities(self, paths):
      """
      Load all activities files
      """
      # Sort out file name args given on command line.  Figure out if they are fitness
      # file names, directory names containing fitness files, or names of csv file
      # lists.  Also, expand file name wildcards, if necessary.  Check to see if
      # files exist and if the file extension is valid.  Build lists of fitnes
      # filenames, directories # which will be further searched for files, and
      # list files.

      def is_csv(filename):
          '''
          check to see if file exists and that the file
          extension is .csv
          '''
          extension = os.path.splitext(filename)[1].lower()
          return extension == '.csv' and os.path.isfile(filename)

      def is_activity(filename):
          '''
          check to see if file exists and that the extension is a
          valid activity file accepted by GC.
          '''
          if not os.path.isfile(filename):
              logger.warning("File '{}' does not exist. Skipping...".format(filename))
              return False

          # Get file extension from name
          extension = os.path.splitext(filename)[1].lower()
          logger.debug("File '{}' has extension '{}'".format(filename, extension))

          # Valid file extensions are .tcx, .fit, and .gpx
          if extension in VALID_GARMIN_FILE_EXTENSIONS:
              logger.debug("File '{}' extension '{}' is valid.".format(filename, extension))
              return True
          else:
              logger.warning("File '{}' extension '{}' is not valid. Skipping file...".format(filename, extension))
              return False

      filenames, listfiles = [], []
      for path in paths:
        path = os.path.realpath(path)
        if is_activity(path):
          # Use file directly
          filenames.append(path)

        elif is_csv(path):
            # Use file directly
            logger.info("List file '{}' will be processed...".format(path))
            filenames.append(path)

        elif os.path.isdir(path):
            # Use files in directory
            # - Does not recursively drill into directories.
            # - Does not search for csv files in directories.
            filenames += [f for f in glob.glob(os.path.join(path, '*')) if is_activity(f)]

      # Activity name given on command line only applies if a single filename
      # is given.  Otherwise, ignore.
      if len(filenames) != 1 and self.activity_name:
          logger.warning('-a option valid only when one fitness file given.  Ignoring -a option.')
          self.activity_name = None

      activities = []

      # Build activity tuples - a Activity has a filename, name, and file type
      for filename in filenames:
          activities.append(Activity(filename=filename, name=self.activity_name, type=self.activity_type))

      # Pull in file info from csv files and apend tuples to list
      for listfile in listfiles:
          with open(listfile, 'rb') as csvfile:
              reader = csv.DictReader(csvfile)
              for row in reader:
                  if self.checkFile(row['filename']):
                    activities.append(Activity(filename=row['filename'], name=row['name'], type=row['type']))


      if len(activities) == 0:
          logger.critical('No valid Files.')
          raise(IOError('No valid files.'))

      return activities


    def run(self):
        """
        Authenticated part of the workflow
        Simply login & upload every activity
        """
        self.user.authenticate()

        for activity in self.activities:
            self.rate_limit()
            self.user.upload(activity)

    def rate_limit(self):
        min_period = 1 # I appear to been banned from Garmin Connect while determining this.
        if not self.last_request:
            self.last_request = 0.0

        wait_time = max(0, min_period - (time.time() - self.last_request))
        time.sleep(wait_time)

        self.last_request = time.time()
        logger.info("Rate limited for %f" % wait_time)

