from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template   # type: ignore
from db import News, session
from scraputils import get_news
from sqlalchemy import exists  # type: ignore


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    r = str(request).split()[-1]
    query_string = r.split("?")[1]
    params = query_string.split("&")
    param_dict = {}

    for param in params:
        key_value = param.split("=")
        param_dict[key_value[0]] = key_value[1]

    label = param_dict["label"]
    id = param_dict["id"][:-1]

    s = session()
    row = s.query(News).get(id)
    row.label = label
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 3)

    for n in news:
        new = News(title=n["title"], author=n["author"], url=n["url"], comments=n["comments"], points=n["points"])
        subquery = s.query(exists().where((News.author == new.author) & (News.title == new.title))).scalar()
        if not subquery:
            s.add(new)

    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    bayes = NaiveBayesClassifier(1)

    train = s.query(News).filter(News.label is not None).all()
    x = [i.title for i in train]
    y = [i.label for i in train]
    bayes.fit(x, y)

    news = s.query(News).filter(News.label is None).all()
    X = [i.title for i in news]
    y = bayes.predict(X)

    for i, item in enumerate(news):
        item.label = y[i]

    s.commit()

    return sorted(news, key=lambda x: x.label)


@route("/recommendations")
def recommendations():
    s = session()
    _ = classify_news()
    news = s.query(News).filter(News.label is not None).all()
    first, second, third = [], [], []

    for piece in news:
        if piece.label == "good":
            first.append(piece)
        elif piece.label == "maybe":
            second.append(piece)
        elif piece.label == "never":
            third.append(piece)
    res = first + second + third

    return template("news_recommendations", rows=res)


if __name__ == "__main__":
    run(host="localhost", port=8080)
