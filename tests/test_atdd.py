from datetime import datetime

import pytest

from fitness_schedule import FitnessSchedule, ClassStatus

def create_schedule(capacity=2):
    schedule = FitnessSchedule()
    item = schedule.create_class(
        "Пилатес",
        datetime(2026, 11, 2, 18, 0),
        capacity,
    )
    return schedule, item

def test_participant_appears_after_registration():
    schedule, item = create_schedule()

    schedule.register(item.class_id, "Анна")

    assert "Анна" in item.participants

def test_registration_rejected_when_full():
    schedule, item = create_schedule(capacity=1)
    schedule.register(item.class_id, "Анна")

    with pytest.raises(ValueError, match="Свободных мест нет"):
        schedule.register(item.class_id, "Мария")

    assert item.participants == ["Анна"]

def test_duplicate_registration_is_rejected():
    schedule, item = create_schedule()
    schedule.register(item.class_id, "Анна")

    with pytest.raises(ValueError, match="уже зарегистрирован"):
        schedule.register(item.class_id, "Анна")

    assert item.participants == ["Анна"]

def test_cancelled_class_rejects_registration():
    schedule, item = create_schedule()
    schedule.cancel_class(item.class_id)

    with pytest.raises(ValueError, match="Занятие отменено"):
        schedule.register(item.class_id, "Анна")

    assert item.status == ClassStatus.CANCELLED
    assert item.participants == []