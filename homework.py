class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = format(duration, ".3f")
        self.distance = format(distance, ".3f")
        self.speed = format(speed, ".3f")
        self.calories = format(calories, ".3f")

    def get_message(self):
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration} ч.; "
            f"Дистанция: {self.distance} км; "
            f"Ср. скорость: {self.speed} км/ч; "
            f"Потрачено ккал: {self.calories}."
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(None, self.duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    training_type = "Running"

    def get_spent_calories(self):
        v = super().get_mean_speed()
        calories = (18 * v - 20) * self.weight / self.M_IN_KM
        return calories * self.duration * 60

    def show_training_info(self) -> InfoMessage:
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.training_type, self.duration,
                           distance, speed, calories)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = "SportsWalking"

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        v2 = 2 * super().get_mean_speed()
        cal = 0.035 * self.weight + (v2 // self.height) * 0.029 * self.weight
        return cal * self.duration * 60

    def show_training_info(self) -> InfoMessage:
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage("SportsWalking",
                           self.duration, distance, speed, calories)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    training_type = "Swimming"

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        v = self.get_mean_speed()
        return (v + 1.1) * 2 * self.weight

    def show_training_info(self) -> InfoMessage:
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.training_type,
                           self.duration, distance, speed, calories)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training):
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
