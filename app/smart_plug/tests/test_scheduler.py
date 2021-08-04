from src.scheduler import compute_hourly_schedule, group_hourly_power_mins, optimize_grouped_schedule_and_make_command
from src.time_util import hour_to_mins, mins_to_mins

import pytest

@pytest.fixture
def temps():
    return [
        {
            "mins": 60*22,
            "temp": 33,
            "feel_like": 31
        }, 
        {
            "mins": 60*23,
            "temp": 36,
            "feel_like": 35
        }, 
        {
            "mins": 60*0,
            "temp": 35,
            "feel_like": 36
        }, 
        {
            "mins": 60*1,
            "temp": 34,
            "feel_like": 35
        }, 
        {
            "mins": 60*2,
            "temp": 35,
            "feel_like": 36
        }
        
    ]


@pytest.fixture
def hourly_power_mins_1():
    out = []
    base_mins = hour_to_mins(22)
    for i in range(12):
        out.append(
        {
            "mins": base_mins + i*60,
            "optimized_power_on_mins": 32
        })

    return out

@pytest.fixture
def hourly_power_mins_2():
    out = []
    base_mins = hour_to_mins(22)
    for i in range(12):
        out.append(
        {
            "mins": base_mins + i*60,
            "optimized_power_on_mins": 60
        })

    return out


def test_compute_schedule(temps):
    r = compute_hourly_schedule(temps)
    assert len(r) == len(temps)
    for item in r:
        item["power_on_mins"] <= 60
        assert item["optimized_power_on_mins"]  < item["power_on_mins"]


def test_group_hourly_power_mins_case_1(hourly_power_mins_1):
    group_size = 3
    r = group_hourly_power_mins(group_size, hourly_power_mins_1)

    assert len(hourly_power_mins_1)/group_size  == len(r)

def test_group_hourly_power_mins_case_2(hourly_power_mins_2):
    group_size = 3
    r = group_hourly_power_mins(group_size, hourly_power_mins_2)
    assert len(hourly_power_mins_2)/group_size  == len(r)


def test_optimize_grouped_schedule_and_make_command_case1():
    grouped_schedule = [
        (1320, 1440+60, 180),
        (1440+60, 1440+240, 180),
        (1440+240, 1440+420, 180),
        (1440+420, 1440+600, 180)
    ]
    exp = [
        (1320, 1),
        (1440+600, 0)
    ]
    r = optimize_grouped_schedule_and_make_command(grouped_schedule)
    assert len(r) == 2


def test_optimize_grouped_schedule_and_make_command_case2():
    grouped_schedule = [
        (1320, 1440+60, 100),
        (1440+60, 1440+240, 180),
        (1440+240, 1440+420, 170),
    ]
    exp = [
        (1320, 1),
        (1420, 0),
        (1440+60, 1),
        (1440+240+170, 0)
    ]
    r = optimize_grouped_schedule_and_make_command(grouped_schedule)
    assert r == exp

def test_optimize_grouped_schedule_and_make_command_case3():
    grouped_schedule = [
        (1320, 1440+60, 100),
        (1440+60, 1440+240, 180),
        (1440+240, 1440+420, 180)
    ]
    exp = [
        (1320, 1),
        (1420, 0),
        (1440+60, 1),
        (1440+420, 0)
    ]
    r = optimize_grouped_schedule_and_make_command(grouped_schedule)
    assert r == exp


def test_optimize_grouped_schedule_and_make_command_case4():
    grouped_schedule = [
        (1320, 1440+60, 180),
        (1440+60, 1440+240, 160),
        (1440+240, 1440+420, 180)
    ]
    exp = [
        (1320, 1),
        (1440+60+160, 0),
        (1440+240, 1),
        (1440+420, 0)
    ]
    r = optimize_grouped_schedule_and_make_command(grouped_schedule)
    assert r == exp


def test_optimize_grouped_schedule_and_make_command_case4():
    grouped_schedule = [
        (1320, 1440+60, 61),
        (1440+60, 1440+240, 59),
        (1440+240, 1440+420, 100)
    ]
    exp = [
        (1320, 1),
        (1320+61, 0),
        (1440+240, 1),
        (1440+240+100, 0)
    ]
    r = optimize_grouped_schedule_and_make_command(grouped_schedule, 60)
    assert r == exp

