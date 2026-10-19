from datetime import datetime

import pytest

from fitness_schedule import FitnessSchedule

@pytest.mark.parametrize(
    "capacity, participants, new_name, new_capacity, expected",
    [
        (10, [], "Йога", 10, "success"),
        (2, ["Анна"], "Пилатес", 2, "success"),
        (2, ["Анна", "Мария"], "Фитнес", 1, "error"),
        (1, ["Анна"], "Растяжка", 1, "success"),
    ],
)
def test_update_specification(
    capacity,
    participants,
    new_name,
    new_capacity,
    expected,
):
    schedule = FitnessSchedule()
    item = schedule.create_class(
        "Исходное занятие",
        datetime(2026, 11, 3, 10, 0),
        capacity,
    )

    for participant in participants:
        schedule.register(item.class_id, participant)

    if expected == "error":
        with pytest.raises(ValueError):
            schedule.update_class(
                item.class_id,
                name=new_name,
                capacity=new_capacity,
            )
        assert item.name == "Исходное занятие"
    else:
        schedule.update_class(
            item.class_id,
            name=new_name,
            capacity=new_capacity,
        )
        assert item.name == new_name
        assert item.capacity == new_capacity

@pytest.mark.parametrize(
    "capacity, should_register",
    [
        (2, True),
        (1, True),
    ],
)
def test_registration_examples(capacity, should_register):
    schedule = FitnessSchedule()
    item = schedule.create_class(
        "Функциональная тренировка",
        datetime(2026, 11, 4, 9, 0),
        capacity,
    )

    if should_register:
        schedule.register(item.class_id, "Алексей")

    assert item.participants == ["Алексей"]