from db_operations import *
import datetime


RSS_START = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n<title>Информация о продуктаз</title>\n<link>https://www.FreeBSD.org/press/</link>\n<description>Тут будет размещаться информация о состоянии товаров в холодильнике</description>\nn'
RSS_END = "</channel></rss>"
RSS_SHAB = "<item><title>Срок годности истек</title>\n<description>Товар %s испортился</description></item>"


def gen_rss() -> str:
    rss_ans = RSS_START
    for i in get_products():
        print(i["stop_date"])
        s = list(map(int, i["stop_date"].split("-")))
        stop_date = datetime.date(s[0], s[1], s[2])
        if datetime.date.today() > stop_date:
            rss_ans += RSS_SHAB % f"Срок годности {i['product_name']} истёк"

    rss_ans += RSS_END
    return rss_ans


