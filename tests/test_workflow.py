def test_listing(activities_dir):
    """
    Test the activities listing used in CLI
    """
    from garmin_uploader.workflow import Workflow

    # Test directory
    w = Workflow([activities_dir], username='test', password='test')
    activities = dict([(repr(a), a) for a in w.activities])
    assert 'a.fit' in activities
    assert 'a.tcx' in activities
    assert 'invalid.txt' not in activities

    # Test csv + name
    w = Workflow([activities_dir + '/list.csv'], username='test', password='test')  # noqa
    activities = dict([(repr(a), a) for a in w.activities])
    assert len(activities) == 1  # no nope
    assert 'AAAA' in activities
    a = activities['AAAA']
    assert a.filename == 'a.fit'
    assert a.type == 'running'

    # Test simple file + name + type
    w = Workflow([activities_dir + '/a.tcx'], activity_name='Test TCX', activity_type='cycling', username='test', password='test')  # noqa
    assert len(w.activities) == 1
    a = w.activities[0]
    assert a.name == 'Test TCX'
    assert a.type == 'cycling'

    # Test simple files + name + type
    # Name must be skipped here
    files = [
      activities_dir + '/a.tcx',
      activities_dir + '/a.fit',
    ]
    w = Workflow(files, activity_name='Test 2 files', activity_type='cycling', username='test', password='test')  # noqa
    activities = dict([(repr(x), x) for x in w.activities])
    assert len(activities) == 2
    assert 'a.fit' in activities
    assert 'a.tcx' in activities
    assert activities['a.fit'].name is None
    assert activities['a.tcx'].name is None
    assert activities['a.fit'].type == 'cycling'
    assert activities['a.tcx'].type == 'cycling'
