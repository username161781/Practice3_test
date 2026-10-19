from datetime import datetime

from behave import given, when, then

from fitness_schedule import FitnessSchedule

@given("фитнес-класс запланирован")
def step_class_planned(context):
    context.schedule = FitnessSchedule()
    context.item = context.schedule.create_class(
        "Йога",
        datetime(2026, 11, 5, 10, 0),
        2,
    )
    context.error = None

@given("в классе есть свободные места")
def step_free_places(context):
    assert len(context.item.participants) < context.item.capacity

@given("все места заняты")
def step_class_full(context):
    while len(context.item.participants) < context.item.capacity:
        name = f"Участник {len(context.item.participants) + 1}"
        context.schedule.register(context.item.class_id, name)

@when("участник регистрируется на класс")
def step_register(context):
    context.schedule.register(context.item.class_id, "Анна")

@when("новый участник регистрируется на класс")
def step_register_new(context):
    try:
        context.schedule.register(context.item.class_id, "Мария")
    except ValueError as error:
        context.error = error

@then("участник отображается в списке")
def step_participant_visible(context):
    assert "Анна" in context.item.participants

@then("система отклоняет регистрацию")
def step_registration_rejected(context):
    assert context.error is not None
    assert "Свободных мест нет" in str(context.error)