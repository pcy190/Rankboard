import datetime

from util.core import *
from util.zhihu_billboard import get_billboard
from util.weibo_top import get_top
import pytz
tz = pytz.timezone('Asia/Shanghai')
user_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S  UTC+08:00")

gist = Gist()
gist.auth()
r = gist.read()
print(r)
content = "Weibo rank:\n%s\n\n\nZhihu rank:\n%s\n\nUpdated at %s" % (get_top(), get_billboard(),user_time)
print(content)
gist.update(content)
