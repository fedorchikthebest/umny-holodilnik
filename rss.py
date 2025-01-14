from db_operations import *
import datetime


RSS_START = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n<title>FreeBSD in the Press</title>\n<link>https://www.FreeBSD.org/press/</link>\n<description>Press Stories about FreeBSD</description>\nn'
RSS_END = "</channel></rss>"
RSS_SHAB = "<item><title>Срок годности истек</title>\n<link>https://www.opennet.me/opennews/art.shtml?num=62503</link>\n<pubDate>Thu, 02 Jan 2025 11:08:19 +0300</pubDate>\n<description>Товар %s испортился</description></item>"


def gen_rss() -> str:
    rss_ans = RSS_START
    for i in get_products():
        print(i["stop_date"])
        s = list(map(int, i["stop_date"].split("-")))
        stop_date = datetime.date(s[0], s[1], s[2])
        if datetime.date.today() > stop_date:
            rss_ans += RSS_SHAB % f"Срок годности {i['product_name']} истёк"
    return rss_ans


