from db_operations import *
import datetime
import os


RSS_START = f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<ttl>1</ttl>\n<channel>\n<title>Информация о продуктах</title>\n<description>Тут будет размещаться информация о состоянии товаров в холодильнике</description>\n<link>{os.getenv("HOLODILNIK_HOST")}</link>\n'
RSS_END = "</channel></rss>"
RSS_SHAB = "<item><title>%s</title>\n<pubDate>%s</pubDate>\n<description>%s</description><guid>%s</guid><link>%s</link></item>"


def gen_rss() -> str:
    rss_ans = RSS_START
    for i in get_products():
        print(i["stop_date"])
        s = list(map(int, i["stop_date"].split("-")))
        stop_date = datetime.date(s[0], s[1], s[2])
        if datetime.date.today() > stop_date:
            rss_ans += RSS_SHAB % ("Срок годности истёк", f"{stop_date.strftime('%a, %d %b %Y')} 00:00:00", f"Срок годности {i['product_name']} истёк", i['id'], os.getenv("HOLODILNIK_HOST") + '/' + i['id'])
        elif stop_date - datetime.date.today() <= datetime.timedelta(days=3):
            rss_ans += RSS_SHAB % ("Срок годности скоро истечёт", f"{stop_date.strftime('%a, %d %b %Y')} 00:00:00", f"Срок годности {i['product_name']} скоро истечёт", i['id'], os.getenv("HOLODILNIK_HOST") + '/' + i['id'])


    rss_ans += RSS_END
    return rss_ans


