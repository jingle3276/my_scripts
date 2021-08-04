import pytest

from src.time_util import mins_to_hour, local_time_in_timestamp

def test_mins_to_hour():
    assert mins_to_hour(1440) == 0 
    assert mins_to_hour(60) == 1 
    assert mins_to_hour(1320) == 22 
    assert mins_to_hour(1320+30) == 22.5 
    



