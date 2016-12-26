import pytest


@pytest.fixture(scope='session')
def api():
    """
    Garmin API Instance
    """
    from garmin_uploader.api import GarminAPI
    return GarminAPI()


@pytest.fixture(scope='session')
def user():
    """
    Garmin Connect test user
    """
    from garmin_uploader.user import User

    # please do not abuse this account...
    login = 'guploader@yopmail.com'
    password = 'GuploaderTest51'[::-1]
    return User(login, password)


@pytest.fixture(scope='session')
def activities_dir(tmpdir_factory):
    """
    Build empty activities file
    Used to test cli listing functions
    """
    workdir = tmpdir_factory.mktemp('activities')

    # Build csv
    csv = workdir.join('list.csv')
    csv.write('\n'.join([
        'filename,name,type',
        '{}/a.fit,AAAA,running'.format(workdir),
        'nope.fit,nope,nope',
    ]))

    # Build a fit file
    fit = workdir.join('a.fit')
    fit.write('')

    # Build a tcx file
    tcx = workdir.join('a.tcx')
    tcx.write('')

    # Build an invalid file
    invalid = workdir.join('invalid.txt')
    invalid.write('')

    # Gives workdir to test
    yield str(workdir)

    # Cleanup
    workdir.remove()
