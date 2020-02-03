import requests
import re
from bs4 import BeautifulSoup


def get_billboard():
    headers = {"User-Agent": "", "Cookie": ""}
    zh_url = "https://www.zhihu.com/billboard"
    zh_response = requests.get(zh_url, headers=headers)

    webcontent = zh_response.text
    soup = BeautifulSoup(webcontent, "html.parser")
    script_text = soup.find("script", id="js-initialData").get_text()
    rule = r'"hotList":(.*?),"guestFeeds"'
    result = re.findall(rule, script_text)

    temp = result[0].replace("false", "False").replace("true", "True")
    hot_list = eval(temp)

    billboard = ""
    for idx in range(len(hot_list)):
        hot = hot_list[idx]
        order = ''
        if idx == 0:
            order = 'Pin '
        else:
            order = "%-3d" % idx
        hot_line = "%s%s  %s" % (
            order, hot['target']['titleArea']['text'], hot['target']['metricsArea']['text'])  # title + metrics
        # hot['target']['titleArea']['excerptArea']['text'] # excerpt text
        billboard+=hot_line+'\n'
    return billboard.rstrip()
