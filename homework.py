from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MSG = ('Тип тренировки: {training_type}; '
                'Длительность: {duration:.3f} ч.; '
                'Дистанция: {distance:.3f} км; '
                'Ср. скорость: {speed:.3f} км/ч; '
                'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return (self.INFO_MSG.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # m
    M_IN_KM = 1000
    H_IN_M = 60  # hours to minutes

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
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * self.H_IN_M
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_COEFF1 = 0.035
    CALORIES_WEIGHT_COEFF2 = 0.029
    K_IN_M = 0.278  # kmph to ms
    CM_IN_M = 100  # cm to m

    action: int
    duration: float
    weight: float
    height: float
    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_WEIGHT_COEFF1 * self.weight
                + ((self.K_IN_M * super().get_mean_speed())**2
                    / (self.height / self.CM_IN_M))
                * self.CALORIES_WEIGHT_COEFF2 * self.weight)
            * self.duration * self.H_IN_M
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # m
    SPEED_SHIFT = 1.1
    SPEED_MULT = 2

    action: int
    duration: float  # h
    weight: float
    length_pool: float
    count_pool: int
    length_pool: float
    count_pool: int

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SPEED_SHIFT)
                * self.SPEED_MULT * self.weight * self.duration)


TRAIN_DICT = {'RUN': Running, 'WLK': SportsWalking,
              'SWM': Swimming}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAIN_DICT:
        raise KeyError('Несуществующий тип тренировки')

    return TRAIN_DICT[workout_type](*data)


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
