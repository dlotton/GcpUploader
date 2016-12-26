def test_types(api):
    """
    Test activity types listing
    Non authenticated
    """
    types = api.load_activity_types()
    assert isinstance(types, dict)
    assert len(types) > 0
    assert 'all' in types
    assert 'running' in types
    assert 'track_cycling' in types
    assert 'track cycling' in types
    assert types['track_cycling'] == types['track cycling']
