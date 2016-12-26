import os.path
import glob
import csv
import time
import six
from garmin_uploader import (
    logger, VALID_GARMIN_FILE_EXTENSIONS, BINARY_FILE_FORMATS
)
from garmin_uploader.user import User
from garmin_uploader.api import GarminAPI, GarminAPIException


class Activity(object):
    """
    Garmin Connect Activity model
    """
    def __init__(self, path, name=None, type=None):
        self.id = None  # provided on upload
        self.path = path
        self.name = name
        self.type = type

    def __repr__(self):
        if self.id is None:
            out = self.name or self.filename
        else:
            out = '{} : {}'.format(self.id, self.name or self.filename)
        if six.PY3 and isinstance(out, bytes):
            return out.decode('utf8')
        else:
            return out

    @property
    def extension(self):
        extension = os.path.splitext(self.path)[1].lower()

        # Valid File extensions are .tcx, .fit, and .gpx
        if extension not in VALID_GARMIN_FILE_EXTENSIONS:
            raise Exception("Invalid File Extension")

        return extension

    @property
    def filename(self):
        """
        Garmin Connect web site does not comply with RFC 2231.
        urllib3 (used by the requests module) automatically detects non-ascii
        characters in filenames and generates the filename* header parameter
        (with asterisk - signifying that the filename has non-ascii characters)
        instead of the filename (without asterisk) header parameter.  Garmin
        Connect does not accept the asterisked version of filename and there
        is no way to tell urllib3 to not generate it.  The work-around for
        Garmin's noncompliant behavior (sending non-ascii characters with the
        non-asterisked filename parameter) is to always send an ascii encodable
        filename.  This is achieved by parsing out the non-ascii characters.
        """
        filename = os.path.basename(self.path)
        if six.PY3:
            return filename
        try:
            return filename.encode('ascii')
        except UnicodeEncodeError:
            return filename.decode('ascii', 'ignore')

    def open(self):
        """
        Open local activity file as a file descriptor
        """
        mode = self.extension in BINARY_FILE_FORMATS and 'rb' or 'r'
        return open(self.path, mode)

    def upload(self, user):
        """
        Upload an activity once authenticated
        """
        assert isinstance(user, User)
        assert user.session is not None

        api = GarminAPI()
        try:
            self.id, uploaded = api.upload_activity(user.session, self)
        except GarminAPIException as e:
            logger.warning('Upload failure: {}'.format(e))
            return False

        if uploaded:
            logger.info('Uploaded activity {}'.format(self))

            # Set activity name if specified
            if self.name:
                try:
                    api.set_activity_name(user.session, self)
                except GarminAPIException as e:
                    logger.warning('Activity name update failed: {}'.format(e))

            # Set activity type if specified
            if self.type:
                try:
                    api.set_activity_type(user.session, self)
                except GarminAPIException as e:
                    logger.warning('Activity type update failed: {}'.format(e))

        else:
            logger.info('Activity already uploaded {}'.format(self))

        return True


class Workflow():
    """
    Upload workflow:
     * List activities according to CLI args
     * Load user credentials
     * Authenticate user
     * Upload activities
    """

    def __init__(self, paths, username=None, password=None,
                 activity_type=None, activity_name=None, verbose=3):
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
        Load all activities files:
        Sort out file name args given on command line.  Figure out if they are
        fitness file names, directory names containing fitness files, or names
        of csv file lists.
        Also, expand file name wildcards, if necessary.  Check to see if files
        exist and if the file extension is valid.  Build lists of fitnes
        filenames, directories # which will be further searched for files, and
        list files.
        """

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
                logger.warning("File '{}' does not exist. Skipping...".format(filename))  # noqa
                return False

            # Get file extension from name
            extension = os.path.splitext(filename)[1].lower()
            logger.debug("File '{}' has extension '{}'".format(filename, extension))  # noqa

            # Valid file extensions are .tcx, .fit, and .gpx
            if extension in VALID_GARMIN_FILE_EXTENSIONS:
                logger.debug("File '{}' extension '{}' is valid.".format(filename, extension))  # noqa
                return True
            else:
                logger.warning("File '{}' extension '{}' is not valid. Skipping file...".format(filename, extension))  # noqa
                return False

        valid_paths, csv_files = [], []
        for path in paths:
            path = os.path.realpath(path)
            if is_activity(path):
                # Use file directly
                valid_paths.append(path)

            elif is_csv(path):
                # Use file directly
                logger.info("List file '{}' will be processed...".format(path))
                csv_files.append(path)

            elif os.path.isdir(path):
                # Use files in directory
                # - Does not recursively drill into directories.
                # - Does not search for csv files in directories.
                valid_paths += [
                    f for f in glob.glob(os.path.join(path, '*'))
                    if is_activity(f)
                ]

        # Activity name given on command line only applies if a single filename
        # is given.  Otherwise, ignore.
        if len(valid_paths) != 1 and self.activity_name:
            logger.warning('-a option valid only when one fitness file given. Ignoring -a option.')  # noqa
            self.activity_name = None

        # Build activities from valid paths
        activities = [
           Activity(p, self.activity_name, self.activity_type)
           for p in valid_paths
        ]

        # Pull in file info from csv files and apppend activities
        for csv_file in csv_files:
            with open(csv_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                activities += [
                    Activity(row['filename'], row['name'], row['type'])
                    for row in reader
                    if is_activity(row['filename'])
                ]

        if len(activities) == 0:
            raise Exception('No valid files.')

        return activities

    def run(self):
        """
        Authenticated part of the workflow
        Simply login & upload every activity
        """
        if not self.user.authenticate():
            raise Exception('Invalid credentials')

        for activity in self.activities:
            self.rate_limit()
            activity.upload(self.user)

        logger.info('All done.')

    def rate_limit(self):
        min_period = 1
        if not self.last_request:
            self.last_request = 0.0

        wait_time = max(0, min_period - (time.time() - self.last_request))
        if wait_time <= 0:
            return
        time.sleep(wait_time)

        self.last_request = time.time()
        logger.info("Rate limited for %f" % wait_time)
