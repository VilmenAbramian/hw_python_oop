class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # m
    M_IN_KM = 1000
    H2M = 60  # hours to minutes

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
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__str__(),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def __str__(self):
        return 'Running'

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.H2M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_K1 = 0.035
    CALORIES_WEIGHT_K2 = 0.029
    K2M = 0.278  # kmph to ms
    SM2M = 100  # sm to m

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def __str__(self):
        return 'SportsWalking'

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_K1 * self.weight
                + ((self.K2M * super().get_mean_speed())**2
                   / (self.height / self.SM2M))
                * self.CALORIES_WEIGHT_K2 * self.weight)
                * self.duration * self.H2M)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # m
    SPEED_SHIFT = 1.1
    SPEED_MULT = 2

    def __init__(self,
                 action: int,
                 duration: float,  # h
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def __str__(self):
        return 'Swimming'

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SPEED_SHIFT)
                * self.SPEED_MULT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    trainings = {'RUN': Running, 'WLK': SportsWalking,
                 'SWM': Swimming}

    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
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
