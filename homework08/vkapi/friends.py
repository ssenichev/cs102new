import dataclasses
import time
import typing as tp
import warnings

import pandas as pd  # type: ignore
import requests  # type: ignore

from homework08.vkapi import config, session
from homework08.vkapi.config import VK_CONFIG

warnings.simplefilter(action="ignore", category=FutureWarning)
QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return self.count


def get_friends(
    user_id: int = 476830585, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    user_id = user_id
    # columns = ['id'] + fields
    # я не понимаю почему, но методом выше не работает
    fields = ", ".join(fields) if type(fields) == list else ""  # type: ignore
    columns = ["id"] + fields.split(", ") if fields != "" else ["id"]  # type: ignore
    df = pd.DataFrame(columns=columns)

    query = (
        f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&count={count}"
        f"&offset={offset}&fields={fields}&v={v}"
    )

    response = requests.get(query)
    people = response.json()["response"]["items"]

    if fields != "":
        for person in people:
            try:
                person["deactivated"]
            except KeyError:
                new_dict = {key: person[key] for key in columns if key in person and person["can_access_closed"]}
                df = df.append(new_dict, ignore_index=True)
    else:
        df["id"] = people

    df.dropna(inplace=True)
    friends_response = FriendsResponse(count=len(df["id"].tolist()), items=df["id"].tolist())
    # return df['id'].tolist()
    return friends_response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.List[tp.Optional[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя
     с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    query_params = {
        "access_token": config.VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
    }

    if type(target_uid) == int:
        response = session.get("friends.getMutual", **query_params)
        mutual = response.json()["response"]
        return mutual

    elif type(target_uid) != int or type(target_uids) is not None:
        if len(target_uids) > 100:  # type: ignore
            commons = []  # type: ignore
            performed_num = 0
            to_perform = len(target_uids)  # type: ignore

            while to_perform > 0:
                response = session.get("friends.getMutual", **query_params)
                new_cmns = response.json()
                try:
                    commons = commons + new_cmns["response"] if new_cmns["response"] not in commons else commons
                    performed_num += query_params["offset"]
                except KeyError:
                    performed_num += query_params["offset"]

                to_perform = len(target_uids) - performed_num  # type: ignore
                query_params["offset"] += 100
                time.sleep(4)

            return commons

        else:
            response = session.get("friends.getMutual", **query_params)
            try:
                check = response.json()
                return check["response"]
            except KeyError:
                return []  # type: ignore

    else:
        return []  # type: ignore


if __name__ == "__main__":
    list = get_friends(user_id=408461889, fields=["sex"])
    print(list.count)

    mutual_friends = get_mutual(target_uids=list.items)  # type: ignore
    print(mutual_friends)
