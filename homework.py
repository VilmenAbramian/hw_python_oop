from dataclasses import asdict, dataclass, fields


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
            (
                self.CALORIES_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_SPEED_SHIFT
            )
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
            (
                self.CALORIES_WEIGHT_RATIO1
                * self.weight
                + (
                  (
                      self.KMPH_IN_MS * self.get_mean_speed()
                  )**2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_WEIGHT_RATIO2 * self.weight
            )
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


WORKOUTS = {'RUN': (Running, len(fields(Running))),
            'WLK': (SportsWalking, len(fields(SportsWalking))),
            'SWM': (Swimming, len(fields(Swimming)))}

ERROR_TRAIN_TYPE = '{type} - несуществующий тип тренировки'
ERROR_ARGS_LEN = ('Для тренировки {type} передано неверное'
                  'количество аргументов: {err_args}, '
                  'так как требуется {right_args}')


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train, args_len = WORKOUTS[workout_type]
    if workout_type not in WORKOUTS:
        raise ValueError(ERROR_TRAIN_TYPE.format(type=workout_type))
    if len(data) != args_len:
        raise ValueError(
            ERROR_ARGS_LEN.format(
                type=workout_type,
                err_args=len(data),
                right_args=args_len)
        )
    return train(*data)


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
