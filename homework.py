from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO = ('Тип тренировки: {training_type}; '
            'Длительность: {duration:.3f} ч.; '
            'Дистанция: {distance:.3f} км; '
            'Ср. скорость: {speed:.3f} км/ч; '
            'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.INFO.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # m
    M_IN_KM = 1000
    M_IN_H = 60  # hours to minutes

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_SPEED_MULTIPLIER = 18
    CALORIES_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * self.M_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_RATIO1 = 0.035
    CALORIES_WEIGHT_RATIO2 = 0.029
    KMPH_IN_MS = 0.278  # kmph to ms
    CM_IN_M = 100

    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_WEIGHT_RATIO1
             * self.weight
             + ((self.KMPH_IN_MS * self.get_mean_speed())**2
                / (self.height / self.CM_IN_M))
             * self.CALORIES_WEIGHT_RATIO2 * self.weight)
            * self.duration * self.M_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # m
    SPEED_SHIFT = 1.1
    SPEED_MULT = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SPEED_SHIFT)
                * self.SPEED_MULT * self.weight * self.duration)


WORKOUTS = {'RUN': (Running, 3), 'WLK': (SportsWalking, 4),
            'SWM': (Swimming, 5)}

ERROR_MESSAGE_1 = '{type} - несуществующий тип тренировки'
ERROR_MESSAGE_2 = 'Невероное количество параметров тренировки'


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in WORKOUTS:
        raise ValueError(ERROR_MESSAGE_1.format(type=workout_type))

    if len(data) != WORKOUTS[workout_type][1]:
        raise TypeError(ERROR_MESSAGE_2)

    return WORKOUTS[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
