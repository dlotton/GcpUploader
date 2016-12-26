import os.path
try:
    # Python 3
    from configparser import ConfigParser
except ImportError:
    # Python 2
    from ConfigParser import RawConfigParser as ConfigParser
from garmin_uploader import logger, CONFIG_FILE
from garmin_uploader.api import GarminAPI


class User(object):
    """
    Garmin Connect user model
    Authenticates through web api as a browser
    """
    def __init__(self, username=None, password=None):
        """
        ---- GC login credential order of precedence ----
        1) Credentials given on command line
        2) Credentials given in config file in current working directory
        3) Credentials given in config file in user's home directory

        Command line overrides all, config in cwd overrides config in home dir
        """
        # Authenticated API session
        self.session = None

        configCurrentDir = os.path.abspath(
            os.path.normpath('./' + CONFIG_FILE)
        )
        configHomeDir = os.path.expanduser(
            os.path.normpath('~/' + CONFIG_FILE)
        )

        if username and password:
            logger.debug('Using credentials from command line.')
            self.username = username
            self.password = password
        elif os.path.isfile(configCurrentDir):
            logger.debug('Using credentials from \'%s\'.' % configCurrentDir)
            config = ConfigParser()
            config.read(configCurrentDir)
            self.username = config.get('Credentials', 'username')
            self.password = config.get('Credentials', 'password')
        elif os.path.isfile(configHomeDir):
            logger.debug('Using credentials from \'%s\'.' % configHomeDir)
            config = ConfigParser()
            config.read(configHomeDir)
            self.username = config.get('Credentials', 'username')
            self.password = config.get('Credentials', 'password')
        else:
            cwd = os.path.abspath(os.path.normpath('./'))
            homepath = os.path.expanduser(os.path.normpath('~/'))
            raise Exception("'{}' file does not exist in current directory {}"
                            "or home directory {}.  Use login options.".format(
                                CONFIG_FILE, cwd, homepath))

    def authenticate(self):
        """
        Authenticate on Garmin API
        """
        logger.info('Try to login on GarminConnect...')
        logger.debug('Username: {}'.format(self.username))
        logger.debug('Password: {}'.format('*'*len(self.password)))

        api = GarminAPI()
        try:
            self.session = api.authenticate(self.username, self.password)
            logger.debug('Login Successful.')
        except Exception as e:
            logger.critical('Login Failure: {}'.format(e))
            return False

        return True
