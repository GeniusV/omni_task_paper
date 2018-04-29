#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Created by GeniusV on 4/13/18.
import logging
import queue
import re
import sys
import threading
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from datetime import datetime

import lxml.etree
import lxml.html
import requests

LOG_FORMAT = "%(asctime)s - %(levelname)s <%(filename)s> [%(funcName)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger('DefaultLogger')

logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
logger.addHandler(console_handler)


def save_raw_html(url = "http://www.dilidili.wang/anime/201804/"):
    resp = requests.get(url)
    with open("dilidili_raw.html", 'w', encoding = 'utf-8') as f:
        f.write(resp.content.decode())


def tostring(node):
    lxml.html.tostring(node, pretty_print = True)


def resolve_dilidili_new_bangumi(file):
    page = lxml.html.parse(file)
    # /html/body/div[4]/div[1]/div[3]/div[1]/div[5]/dl[1]/dd/h3/a
    # dls = page.findall(".//div[@class='anime_list']/dl/dd/h3/a")
    div = page.findall(".//div[@class='anime_list']")[0]
    dds = div.findall("./dl/dd")
    result = [{'name': dd.find('./h3/a').text,
               "url": 'http://www.dilidili.wang' + dd.find('./h3/a').attrib['href']}
              for dd in dds]
    logger.debug(result)
    return result


def process_data(queue):
    while True:
        data = queue.get()
        logger.debug(data)
        print(data)
        if data == "no":
            break


def query_raw_data(queue, url):
    queue.put(requests.get(url))


def run():
    now = datetime.now()
    data = resolve_dilidili_new_bangumi('dilidili_raw.html')
    q = queue.Queue()

    process_thread = threading.Thread(target = process_data, args = (q,))

    process_thread.start()

    with ThreadPoolExecutor(max_workers = 50) as executor:
        futures = {executor.submit(query_raw_data, q, item['url']): item for item in data}
        for future in as_completed(futures):  # type: Future
            data_set = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error("{} generate an error: {}".format(data_set['name'], e))
            else:
                logger.debug("{} done".format(data_set['name']))

    q.put("no")
    print(datetime.now() - now)


def test():
    page = lxml.html.parse('dilidili_raw.html')
    div = page.findall(".//div[@class='d_label2']")[2]
    onclick = div.findall('./a')[1]
    text = onclick.attrib['onclick']
    print(text)
    pattern = re.compile('周(.) (\d\d:\d\d)')
    res = re.findall(pattern,text)
    week, time = res[0]
    print(week, time)

    # [print(lxml.html.tostring(onclick, pretty_print = True, encoding = 'utf-8').decode()) for onclick in onclicks]


if __name__ == '__main__':
    test()
