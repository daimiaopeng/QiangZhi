import requests
import time
import urllib3

global  token

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.session()


url_school = {
    '吉首大学': r'https://jwxt.jsu.edu.cn/',
    '中南林业科技大学涉外学院': r'http://zswxyjw.minghuaetc.com/znlykjdxswxy/',
    '海南大学': r'http://jxgl.hainu.edu.cn/',
    '中南大学': r'http://csujwc.its.csu.edu.cn/',
    '衡阳师范学院': r'http://59.51.24.46/hysf/',
    '湖南科技大学': r'http://kdjw.hnust.cn/kdjw/',
}

url_token = r'http://1787005804808765.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/qiangzhi/main/token'
url_get_jwcs = 'http://app.qzdatasoft.com:9876/qzkjapp//phone/provinceData'

token = session.get(url=url_token, verify=False,timeout=5).json()['token']
url_jwcs_list = session.get(url=url_get_jwcs, verify=False,timeout=5).json()['school']
for jwc in url_jwcs_list:
    try:
        name = jwc['name']
        jwurl = jwc['jwurl']
        url_school[name] = jwurl.replace("/app.do?method=sendsms","")
    except Exception as e:
        continue


date_list = ['当前学期','所有学期','2021-2020-2','2021-2020-1','2020-2021-2','2020-2021-1','2019-2020-2','2019-2020-1','2018-2019-2','2018-2019-1','2017-2018-2','2017-2018-1','2016-2017-2',
             '2016-2017-1','2015-2016-2','2015-2016-1','2014-2015-2','2014-2015-1']


def from_txt_get_xh(name):
    xh = []
    with open(name, 'r', encoding='utf-8') as f:
        a = f.readlines()
        for i in a:
            xh.append(dict(eval(i))['xh'])
    return xh


class School:
    def __init__(self, url_school, xh):

        if url_school[-1] != '/':
            url_school = url_school + '/'
        self.xh = xh
        self.url_school = url_school
        self.header = {
            "token":token
        }



    def getUserInfo(self):
        # 学生基本信息 参数：学号
        url_infor = self.url_school + 'app.do?method=getUserInfo&xh=%s' % self.xh
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getCurrentTime(self, time=time.strftime("%Y-%m-%d", time.localtime())):
        # 获取当前时间、周次、学年等信息 参数：查询时间
        url_infor = self.url_school + 'app.do?method=getCurrentTime&currDate=%s' % (time)
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getGrade(self, xq='2019-2020-1'):
        # 获取成绩信息 参数：学号 学期（2017-2018-1）
        url_infor = self.url_school + 'app.do?method=getCjcx&xh=%s&xnxqid=%s' % (self.xh, xq)
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        if isinstance(json,list):
            return json
        else:
            if json.get('result') != None:
                return json.get('result')
            else:
                return []
    def getKb(self, zhou):
        # 课表 参数：学号 周数
        url_infor = self.url_school + 'app.do?method=getKbcxAzc&xh=%s&xnxqid=2019-2020-1&zc=%s' % (self.xh, zhou)
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getKscx(self):
        # 获取考试信息 参数：学号
        url_infor = self.url_school + 'app.do?method=getKscx&xh=%s' % (self.xh)
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getKxJscx(self, time=time.strftime("%Y-%m-%d", time.localtime()), idleTime='allday', xiaoquid='', jxlid='',
                  classroomNumber=''):
        # 获取空教室 参数：时间（2018-12-13）时间参数(allday：全天, am：上午pm：下午, night：晚上) 校区ID 教学楼 可容纳人数(30：30人以下
        # 30-40：30-40人#40-50：40-50人# 60：60人以上)
        url_infor = self.url_school + 'app.do?method=getKxJscx&time=%s&idleTime=%s' % (time, idleTime)
        if len(xiaoquid) > 0:
            url_infor = url_infor + '&xqid=%s' % xiaoquid
        if len(jxlid) > 0:
            url_infor = url_infor + '&jxlid=%s' % jxlid
        if len(str(classroomNumber)) > 0:
            url_infor = url_infor + '&classroomNumber=%s' % classroomNumber
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getJxlcx(self, xiaoquid):
        # 获取校区教学楼信息 参数：校区ID
        url_infor = self.url_school + 'app.do?method=getJxlcx&xqid=%s' % (xiaoquid)
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getXqcx(self):
        # 获取校区
        url_infor = self.url_school + 'app.do?method=getXqcx'
        # json = session.get(url=url_infor, headers=self.header).json()
        json = session.get(url=url_infor, headers=self.header,verify=False,timeout=5).json()
        return json

    def getEarlyWarnInfo(self, num=0):
        # 获取学籍预警信息 参数：学号 history取值（0：当前预警 # 1：历史预警）
        url_infor = self.url_school + 'app.do?method=getEarlyWarnInfo&xh=%s&history=%s' % (self.xh, num)
        json = session.get(url=url_infor, headers=self.header, verify=False,timeout=5).json()
        return json

    def write(self, name, infor):
        # 把信息写入文件中去
        infor = str(infor)
        with open('%s.txt' % name, 'a+', encoding='utf-8') as f:
            if len(infor) <= 2:
                pass
            else:
                f.write(infor + '\n')
        return 1

    def guake(self, infor):
        # 打印挂科科目
        try:
            if infor.get('result'):
                infor = infor['result']
        except:
            pass
        for i in infor:
            if float(i['zcj']) < 60:
                print(i['xm'] + ' ' + i['kcmc'] + ' ' + str(i['zcj']))

if __name__ == '__main__':
    pass

