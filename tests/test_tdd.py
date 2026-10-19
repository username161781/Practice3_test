from datetime import datetime

import pytest

from fitness_schedule import FitnessSchedule, ClassStatus

def test_create_class():
    schedule = FitnessSchedule()

    item = schedule.create_class(
        "Йога",
        datetime(2026, 11, 1, 10, 0),
        10,
    )

    assert item.name == "Йога"
    assert item.capacity == 10
    assert item.participants == []
    assert item.status == ClassStatus.PLANNED

def test_create_class_with_empty_name():
    schedule = FitnessSchedule()

    with pytest.raises(ValueError):
        schedule.create_class(
            "   ",
            datetime(2026, 11, 1, 10, 0),
            10,
        )

def test_create_class_with_zero_capacity():
    schedule = FitnessSchedule()

    with pytest.raises(ValueError):
        schedule.create_class(
            "Йога",
            datetime(2026, 11, 1, 10, 0),
            0,
        )

def test_update_class_time():
    schedule = FitnessSchedule()
    item = schedule.create_class(
        "Йога",
        datetime(2026, 11, 1, 10, 0),
        10,
    )

    updated = schedule.update_class(
        item.class_id,
        starts_at=datetime(2026, 11, 1, 12, 0),
    )

    assert updated.starts_at == datetime(2026, 11, 1, 12, 0)

def test_capacity_cannot_be_less_than_participants():
    schedule = FitnessSchedule()
    item = schedule.create_class(
        "Йога",
        datetime(2026, 11, 1, 10, 0),
        3,
    )

    schedule.register(item.class_id, "Анна")
    schedule.register(item.class_id, "Ирина")

    with pytest.raises(ValueError):
        schedule.update_class(item.class_id, capacity=1)

    assert item.capacity == 3