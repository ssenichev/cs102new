import typing as tp
from collections import defaultdict

import community as community_louvain  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import pandas as pd  # type: ignore

from homework08.vkapi.friends import get_friends, get_mutual


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """
    # if friends is None:
    #     friends = get_friends(user_id=user_id, fields=['sex'])
    #
    # # friends = friends.items
    # # в тестах список друзей не соотвествует классу френдс, который стандартизирован в файле friends.py
    # mutuality = get_mutual(target_uids=friends)
    # print(mutuality)
    #
    # seen = set()
    # mutuality = [item for item in mutuality if item['id'] not in seen and not seen.add(item['id'])]
    #
    # edges = []
    # for mutual in mutuality:
    #
    #     if mutual['common_count'] != 0:
    #         for friend in mutual['common_friends']:
    #             edges.append((mutual['id'], friend))
    #
    # return edges
    if friends is None:
        friends = list(get_friends(user_id=user_id, fields=["sex"]))  # type: ignore

    graph = []
    mutual_list = get_mutual(target_uids=friends)  # type: ignore

    if user_id is None:
        mutual_list = get_mutual(target_uids=friends)  # type: ignore
    elif user_id is not None:
        mutual_list = get_mutual(source_uid=user_id, target_uids=friends)  # type: ignore

    for item in mutual_list:
        assert isinstance(item, dict)
        node = item["id"]
        for friend_id in item["common_friends"]:
            graph.append((node, friend_id))

    return graph


def plot_ego_network(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    nx.draw(graph, layout, node_size=5, node_color="black", alpha=0.5, with_labels=False)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    partition = community_louvain.best_partition(graph)
    nx.draw_networkx(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8)
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)
    partition = community_louvain.best_partition(graph)
    for uid, cluster in partition.items():
        communities[cluster].append(uid)
    return communities


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],
    friends: tp.List[tp.Dict[str, tp.Any]],
    fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])  # type: ignore
                    break
    return pd.DataFrame(data=data, columns=["cluster"] + fields)


if __name__ == "__main__":
    #  100+ friends id: 408461889
    #  my id: 476830585

    ego = ego_network(user_id=408461889)
    plot_ego_network(ego)
