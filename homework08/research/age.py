import datetime as dt
import statistics
import typing as tp

import numpy as np

from homework08.vkapi.friends import get_friends


def age_predict(user_id: int = 476830585, test_case: bool = False) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    year = dt.date.today().year
    age = []

    if not test_case:
        friends = get_friends(user_id=user_id, fields=["bdate"], df_return=True)  # кейс для НАСТОЯЩЕЙ ПРОВЕРКИ
        dates = friends["bdate"].to_list()  # type: ignore
        for date in dates:
            try:
                bday = int(date.split(".")[2])
                age.append(year - bday)
            except (AttributeError, IndexError, KeyError):
                pass
    else:
        friends = get_friends(user_id=user_id)  # кейс для ТЕСТОВ
        for friend in friends:
            try:
                bday = int(friend["bdate"].split(".")[2])
                age.append(year - bday)
            except (AttributeError, IndexError, KeyError):
                pass

    return round(np.median(np.array(age)), 1)


if __name__ == "__main__":
    #  100+ friends id: 408461889
    #  my id: 476830585

    print(age_predict(user_id=408461889, test_case=False))
