from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    show_attribute = ('Тип тренировки: {training_type}; '
                      'Длительность: {duration:.3f} ч.; '
                      'Дистанция: {distance:.3f} км; '
                      'Ср. скорость: {speed:.3f} км/ч; '
                      'Потрачено ккал: {calories:.3f}.'
                      )

    def get_message(self) -> str:
        return self.show_attribute.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество калорий за тренировку (заготовка)."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращает объект класса сообщения (InfoMessage(заготовка)"""
        training_type: str = type(self).__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить истраченное количество калорий за тренировку."""
        speed: float = super().get_mean_speed()
        calories: float = (self.coeff_calorie_1 * speed
                           - self.coeff_calorie_2) * self.weight / self.M_IN_KM
        return calories * self.duration * self.H_IN_M


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    const_1: float = 0.035
    const_2: int = 2
    const_3: float = 0.029

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество калорий за тренировку."""
        speed: float = super().get_mean_speed()
        cal: float = (self.const_1 * self.weight
                      + (speed ** self.const_2 // self.height)
                      * self.const_3 * self.weight)
        return cal * self.duration * self.H_IN_M


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    const_1: float = 1.1
    const_2: int = 2

    def __init__(self, action, duration, weight,
                 length_pool, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить истраченное количество калорий за тренировку."""
        speed = self.get_mean_speed()
        return (speed + self.const_1) * self.const_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    choice: Dict[str, __name__] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    assert workout_type in choice, "Тип указан неверно"
    return choice[workout_type](*data)


def main(training: Training) -> None:
    """Распечатывает данные в консоль о параметрах тренировки"""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
