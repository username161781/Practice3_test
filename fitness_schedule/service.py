from datetime import datetime

from .models import FitnessClass, ClassStatus

class FitnessSchedule:
    def __init__(self):
        self.classes: dict[int, FitnessClass] = {}
        self._next_id = 1

    def create_class(
        self,
        name: str,
        starts_at: datetime,
        capacity: int,
    ) -> FitnessClass:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название занятия не может быть пустым")

        if not isinstance(starts_at, datetime):
            raise ValueError("Необходимо указать дату и время")

        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Вместимость должна быть положительным числом")

        fitness_class = FitnessClass(
            class_id=self._next_id,
            name=name.strip(),
            starts_at=starts_at,
            capacity=capacity,
        )

        self.classes[fitness_class.class_id] = fitness_class
        self._next_id += 1
        return fitness_class

    def update_class(
        self,
        class_id: int,
        *,
        name: str | None = None,
        starts_at: datetime | None = None,
        capacity: int | None = None,
    ) -> FitnessClass:
        fitness_class = self._get_class(class_id)

        if fitness_class.status == ClassStatus.CANCELLED:
            raise ValueError("Нельзя изменить отменённое занятие")

        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Название занятия не может быть пустым")

        if starts_at is not None and not isinstance(
            starts_at, datetime
        ):
            raise ValueError("Необходимо указать дату и время")

        if capacity is not None:
            if type(capacity) is not int or capacity <= 0:
                raise ValueError(
                    "Вместимость должна быть положительным числом"
                )

            if capacity < len(fitness_class.participants):
                raise ValueError(
                    "Вместимость меньше количества участников"
                )

        if name is not None:
            fitness_class.name = name.strip()

        if starts_at is not None:
            fitness_class.starts_at = starts_at

        if capacity is not None:
            fitness_class.capacity = capacity

        return fitness_class

    def register(self, class_id: int, participant: str) -> FitnessClass:
        fitness_class = self._get_class(class_id)

        if fitness_class.status == ClassStatus.CANCELLED:
            raise ValueError("Занятие отменено")

        if not isinstance(participant, str) or not participant.strip():
            raise ValueError("Имя участника не может быть пустым")

        participant = participant.strip()

        if participant in fitness_class.participants:
            raise ValueError("Участник уже зарегистрирован")

        if len(fitness_class.participants) >= fitness_class.capacity:
            raise ValueError("Свободных мест нет")

        fitness_class.participants.append(participant)
        return fitness_class

    def cancel_class(self, class_id: int) -> FitnessClass:
        fitness_class = self._get_class(class_id)

        if fitness_class.status == ClassStatus.CANCELLED:
            raise ValueError("Занятие уже отменено")

        fitness_class.status = ClassStatus.CANCELLED
        return fitness_class

    def list_classes(self) -> list[FitnessClass]:
        return sorted(
            self.classes.values(),
            key=lambda item: item.starts_at,
        )

    def _get_class(self, class_id: int) -> FitnessClass:
        try:
            return self.classes[class_id]
        except KeyError:
            raise ValueError("Занятие не найдено") from None