import datetime as dt
import statistics
import typing as tp

import numpy as np

from homework08.vkapi.friends import get_friends


def age_predict(user_id: int = 476830585) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    # friends = get_friends(user_id=user_id, fields=["bdate"])  # кейс для НАСТОЯЩЕЙ ПРОВЕРКИ
    # dates = friends["bdate"].to_list()
    # age = []
    # for date in dates:
    #     try:
    #         bday = int(date.split(".")[2])
    #         age.append(year - bday)
    #     except (AttributeError, IndexError, KeyError):
    #         pass
    # return round(np.median(np.array(age)), 1)

    friends = get_friends(user_id=user_id)  # кейс для ТЕСТОВ
    age = []
    year = dt.date.today().year

    for friend in friends:
        try:
            bday = int(friend["bdate"].split(".")[2])
            age.append(year - bday)
        except (AttributeError, IndexError, KeyError):
            pass

    print(age)
    return round(np.median(np.array(age)), 1)


if __name__ == "__main__":
    print(age_predict())
