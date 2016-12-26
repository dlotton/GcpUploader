import os.path


def test_authenticate(user):
    """
    Test Garmin API authentication
    with "real" user
    """
    assert user.authenticate()
    assert user.session is not None


def test_upload(user):
    """
    Test upload of a sample activity
    """
    from garmin_uploader.workflow import Activity

    tcx = os.path.join(os.path.dirname(__file__), 'sample_file.tcx')
    activity = Activity(str(tcx), 'Test upload', 'running')

    # user is already authenticated by test above
    assert activity.upload(user)
