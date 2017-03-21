#! coding:utf-8
import requests
import sys
from bs4 import BeautifulSoup
import csv
import json
import time,datetime
import re
from adsl import Adsl
import codecs

reload(sys)
sys.setdefaultencoding('utf8')
#http头，给爬虫增加人为假象，迷惑服务器
headers = {'Accept': 'image/png, image/svg+xml, image/*;q=0.8, */*;q=0.5',
'Referer': 'http://www.shenzhenair.com/uiue/flightSearch.do',
'Accept-Language': 'zh-CN',
'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
'Accept-Encoding': 'gzip, deflate',
'Host': 'data.cn.coremetrics.com',
'Connection': 'Keep-Alive'
}
headers1 = {
'Accept': 'text/html, application/xhtml+xml, */*',
'Referer': 'http://www.shenzhenair.com/uiue/flightSearch.do',
'Accept-Language': 'zh-CN',
'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
'Cookie':'90409626_clogin=l=1466669827&v=1&e=1466671633403; RadwareP=BQQAeDLICwr6TbMa8P3sBQ$$; verynginx_sign_cookie=21edd0522f8b10155285c7a9f3e98a51; userid_hash=CgtvTFdrPOxfU3YZBTeCAg==; route=ab8f2b4b0aac13fa8231e67aa418e142; JSESSIONID=00006SQbEuUUW_3KCzGcW5sjluw:-1; sessionid_hash=b8b55026eab01d0fa676d7d9109c6646; cmTPSet=Y; verynginx_sign_javascript=08bc1a3293318349c22acd64e86613ea',
'Accept-Encoding': 'gzip, deflate',
'Host': 'www.shenzhenair.com',
'Connection': 'Keep-Alive'
}
headers2 = {
'Accept': 'text/html, application/xhtml+xml, */*',
'Referer': 'http://www.shenzhenair.com/uiue/flightSearch.do',
'Accept-Language': 'zh-CN',
'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
'Cookie':'90409626_clogin=l=1466669827&v=1&e=1466671633403; RadwareP=BQQAeDLICwr6TbMa8P3sBQ$$; verynginx_sign_cookie=21edd0522f8b10155285c7a9f3e98a51; userid_hash=CgtvTFdrPOxfU3YZBTeCAg==; route=ab8f2b4b0aac13fa8231e67aa418e142; JSESSIONID=00006SQbEuUUW_3KCzGcW5sjluw:-1; sessionid_hash=b8b55026eab01d0fa676d7d9109c6646; cmTPSet=Y; verynginx_sign_javascript=08bc1a3293318349c22acd64e86613ea',
'Accept-Encoding': 'gzip, deflate',
'Host': 'www.shenzhenair.com',
'Connection': 'Keep-Alive'
}

headers3 = {
'Accept': 'text/html, application/xhtml+xml, */*',
'Referer': 'http://www.shenzhenair.com/uiue/flightSearch.do?operate=toLoading&originalPage=login',
'Accept-Language': 'zh-CN',
'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
'Cookie':'90409626_clogin=l=1466669827&v=1&e=1466671633403; RadwareP=BQQAeDLICwr6TbMa8P3sBQ$$; verynginx_sign_cookie=21edd0522f8b10155285c7a9f3e98a51; userid_hash=CgtvTFdrPOxfU3YZBTeCAg==; route=ab8f2b4b0aac13fa8231e67aa418e142; JSESSIONID=00006SQbEuUUW_3KCzGcW5sjluw:-1; sessionid_hash=b8b55026eab01d0fa676d7d9109c6646; cmTPSet=Y; verynginx_sign_javascript=08bc1a3293318349c22acd64e86613ea',
'Content-Type': 'application/x-www-form-urlencoded',
'Accept-Encoding': 'gzip, deflate',
'Host': 'www.shenzhenair.com',
#'Content-Length': 64,
'Connection': 'Keep-Alive',
'Pragma': 'no-cache'
}
#爬取数据
def data_Crawling(from_h,to_h,date_h):
    #创建回话，用于重定向，用于三次请求在一个会话中
    s = requests.Session()
    #超时异常处理，若是超时将等待6分钟
    try:
        #第一次请求
        #response0 = s.get("http://data.cn.coremetrics.com/cm?ci=90409626&st=1466388314288&vn1=4.15.18&ec=utf-8&pi=new-step1_flightChoose&ul=http%3A%2F%2Fwww.shenzhenair.com&cjen=1&cjuid=57398592835414660835879&cjsid=1466388133&cjvf=1&tid=8&ti=1466388338458&hr=%2Fservlet%2FSearchEngineServlet%3Fpc%3D"+from_h+"%26pd%3D"+to_h+"%26pe%3D"+date_h+"%26oriPage%3Duiue",headers=headers)
        response = s.get("http://www.shenzhenair.com/servlet/SearchEngineServlet?pc="+from_h+"&pd="+to_h+"&pe="+date_h+"&oriPage=uiue",headers=headers1,timeout=15)

        #第二次请求
        url = 'http://www.shenzhenair.com/uiue/flightSearch.do?waf_search_token=szair&operate=flightSearch&originalPage=loading'
        data = {'waf_search_token': 'szair',
                'originalPage': 'loading',
                'operate': 'flightSearch'}
        response1 = s.get('http://www.shenzhenair.com/uiue/flightSearch.do?operate=toLoading&originalPage=login'
                        ,headers=headers1,timeout=15)
        #print response1.status_code
        time.sleep(1)
        #response3 = s.get( 'http://data.cn.coremetrics.com/cm?ci=90409626&st=1463492988375&vn1=4.15.18&ec=utf-8&vn2=e4.0&pi=new-bookFlightLoading&ul=http%3A%2F%2Fwww.shenzhenair.com%2Fuiue%2FflightSearch.do%3Foperate%3DtoLoading%26originalPage%3Dlogin&cjen=1&cjuid=84891504478414626697084&cjsid=1463488973&cjvf=1&tid=1&cg=Flights&rnd=1463499547693',headers=headers,timeout=30)
        #time.sleep(3)
        #第三次请求
        data = re.search(r'\'cookie\' : \"(.*?)\",',response1.text)
        #print data.group(1)
        #print s.cookies
        headers4 = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Referer': 'http://www.shenzhenair.com/uiue/flightSearch.do?operate=toLoading&originalPage=login',
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Cookie':'90409626_clogin=l=1466669827&v=1&e=1466671633403; RadwareP=BQQAeDLICwr6TbMa8P3sBQ$$; verynginx_sign_cookie=21edd0522f8b10155285c7a9f3e98a51; userid_hash=CgtvTFdrPOxfU3YZBTeCAg==; route=ab8f2b4b0aac13fa8231e67aa418e142; JSESSIONID=00006SQbEuUUW_3KCzGcW5sjluw:-1; sessionid_hash=b8b55026eab01d0fa676d7d9109c6646; cmTPSet=Y; verynginx_sign_javascript='+data.group(1),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.shenzhenair.com',
        #'Content-Length': 64,
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache'
        }
        response2 = s.post(url,headers=headers4,timeout=15)
        
        response2 = s.post(url,headers=headers4,timeout=15)
        #response2 = s.post(url,timeout=15)
        #print response2.status_code
        return response2.text,response2.cookies
    except requests.exceptions.ReadTimeout:
        return -1,-1
    except requests.exceptions.ConnectionError:
        return -2,-2

# 解析数据
def data_analyze(loaddata,filename):
    #美化数据
    loaddata = loaddata.replace("\r\r\t\t\t\t                                    \t\t\t", "")
    loaddata = loaddata.replace("\r\r\t\t\t\t\t\t                                    ", "")
    loaddata = loaddata.replace("\r\r\t\t\t\t\t\t                       \t\t", "")
    loaddata = loaddata.replace("\n\n\t\t\t\t                                    \t\t\t", "")
    loaddata = loaddata.replace("\n\n\t\t\t\t\t\t                                    ", "")
    loaddata = loaddata.replace("\n\n\t\t\t\t\t\t                       \t\t", "")
    loaddata = loaddata.replace("\r\n\t\t\t\t                                    \t\t\t", "")
    loaddata = loaddata.replace("\r\n\t\t\t\t\t\t                                    ", "")
    loaddata = loaddata.replace("\r\n\t\t\t\t\t\t                       \t\t", "")
    # 采用BeautifulSoup解析网页
    soup = BeautifulSoup(loaddata.decode('utf-8'), "html.parser")
    #resultdata = soup.find_all("a", class_="yd_btn")

    # 保存数据生成 csv以逗号隔开的数据,
    #writer = csv.writer(open(filename, "a"), dialect='excel')
    writer = csv.writer(codecs.open(filename, "a",encoding="GBK"), dialect='excel')
    # 设置多少条航班
    jx1 = soup.find_all("span",class_="color999")
    linesCount = len(jx1)/2


    for i in range(0,linesCount):
        jx = str(jx1[2*i-1])
        jxstart = int(jx.find('：'))
        jxend = int(jx.find(' '))
        jx = jx[jxstart+3:jxend]
        #print cy1,cy2,jx
        cyjx ="','"+jx
        carrierInfo = soup.find_all("table",id="carrierInfo"+str(i))
        if(len(carrierInfo) > 0):
            carrierInfo1 = BeautifulSoup(str(carrierInfo[0]),"html.parser")
            cy = str(carrierInfo1.find_all("td")[0])
            cystart = int(cy.find('：'))
            cyend = int(cy.find('   '))
            cy1 = cy[cystart+3:cyend]
            cy2 = cy[cyend:len(cy)-5]
            cyjx += "','"+cy1+"','"+cy2.replace("   ","")

        allprice = soup.find_all("div",id="seatInfoAllPrice"+str(i+1))
        allprice1 = BeautifulSoup(str(allprice[0]),"html.parser")
        resultdata = allprice1.find_all("a", class_="yd_btn")
        for data in resultdata:
            data = str(data)
            start = int(data.find('('))
            end = int(data.find("）"))
            data = data[start:end]
            data = data[6:]
            dataZ = data[len(data) - 4:len(data) - 3]
            end1 = int(data.find(";"))
            data = data[:end1 - 1]
            reData = [data + ",'" + dataZ +cyjx+ "'"]
            writer.writerow(reData)
#将城市名转化成城市代码
def city_to_code(i_orgcity,i_dstCity):
    #设置是否找到代码
    str_szm="WUS,CJU,HND,NRT,ZQZ,TLV,MFM,AKU,ALA,AAT,AMS,AAQ,TSE,AKA,AQG,AKL,MCO,ORL,BAR,BWI,BAK,CDG,DPS,BCN,PER,BAV,BSD,BHY,PEK,AEB,FRU,BOS,PDX,BUD,BHK,BNE,BRU,CZX,CHG,CTU,CIF,OKA,DRW,KIX,DLU,DLC,DAT,DQA,DXB,DIG,DTW,DOY,DUS,DNH,YTO,DSN,ENH,ERL,FRA,PHL,FOC,FUG,KVD,CPH,CAN,KWE,KWL,HRB,HIA,HAK,HMI,HLD,HAM,HZG,HDG,HGH,HFE,HTN,HAN,HEL,HET,WAW,WAS,JGD,JXA,IEV,KUL,TNA,KGD,JMU,JGN,JJN,JZH,KHG,KRT,CAI,CBR,CGN,KJA,CLE,KRL,KMG,LXA,LAS,LHW,RDM,LYS,RIX,LIS,LJG,LLB,LYI,KOJ,LON,LAD,LAX,MAD,MLA,GDX,MNL,NZH,BKK,LUM,MXP,MOW,MEL,MDG,MUC,KHN,NKG,NNG,NAO,NCE,NGB,NYC,PIT,HKT,NDG,JIQ,CIT,TAO,IQN,SYX,XMN,SWA,SHA,PVG,SZX,SHE,LED,SAN,SJW,SYM,STO,STR,ZRH,TCG,TAS,TPE,TYN,TVS,TCZ,TSN,THQ,TGO,TLQ,VAR,WEH,VCE,VIE,WEF,WNZ,WUA,ULN,HLH,URC,WUX,WUH,XIY,XNN,JHG,SEA,SYD,XIL,HKG,SIN,OVB,ACX,HOU,XUZ,YKS,ATL,YNT,ENY,YNJ,YNZ,SVX,IKT,YIN,YIH,INC,UYN,YCU,CTS,ZHA,DYG,CGQ,CSX,CIH,CGO,CHI,ZHY,CKG,ZUH,GVA,BKI,TYO,ADD,NBO,AUH,PUS,XNT,AOG,JNZ,LYA,NNY,IST,CCU,KOW,HTA,PO1,HAJ,ES1,DO1,DU1,DR1,BO1,MA1,BN1,HE1,HG1,CMB,BOM,KCA,BHX,ABJ,NUE,ODS,ROM,SFO,TRN,SCN,ATH,MEM,MAN,PHX,YVR,MLE,JIU,LYG,FLR,NTG,MIG,DEN,OAK,YYJ,BER,XFN,OSL,GOT,ZAG,BUH,PRG,CKY,MLW,DKR,FNA,FIH,BJL,YAO,TLS,BIO,PUW,GEG,ANC,EUG,SAC,SJC,BOI,PSC,YUL,ADL,WLG,KRY,DFW,YTY,JNG,MSO,RNO,MRS,SHP,BPE,NLT,YOW,ZYI,HJJ,MSP,HYN,BPL,YZY,HZH,IQM,YYC,MIA,YYT,YYG,YQM,YQT,YQB,YHZ,WNH,YIW,LZH,JUH,CGD,DDG,HEK,JDZ,JIL,KJI,LZO,MXZ,OHE,RLK,TEN,YBP,TXN,YIC,YIE,ZJO,LLV,JUZ,KHH,HEL,KHV,LYS,LCX,LPF,WDS"
    str_cs_cn="武夷山|济州|东京羽田|东京成田|张家口|特拉维夫|澳门|阿克苏|阿拉木图|阿勒泰|阿姆斯特丹|阿纳帕|阿斯塔纳|安康|安庆|奥克兰(新西兰)|奥兰多|奥兰多赫恩登|博鳌|巴尔蒂摩|巴库|巴黎|巴厘岛|巴塞罗那|柏斯|包头|保山|北海|北京|百色|比什凯克|波士顿|波特兰|布达佩斯|布哈拉|布里斯本|布鲁塞尔|常州|朝阳|成都|赤峰|冲绳|达尔文|大阪|大理|大连|大同|大庆|迪拜|迪庆|底特律|东营|杜塞尔多夫|敦煌|多伦多|鄂尔多斯|恩施|二连浩特|法兰克福|费城|福州|阜阳|甘贾|哥本哈根|广州|贵阳|桂林|哈尔滨|淮安|海口|哈密|海拉尔|汉堡|汉中|邯郸|杭州|合肥|和田|河内|赫尔辛基|呼和浩特|华沙|华盛顿|加格达奇|鸡西|基辅|吉隆坡|济南|加里宁格勒|佳木斯|嘉峪关|泉州|九寨沟|喀什|喀土穆|开罗|堪培拉|科隆|克拉斯诺亚尔斯克|克利夫兰|库尔勒|昆明|拉萨|拉斯维加斯|兰州|雷德蒙德|里昂|里加|里斯本|丽江|荔波|临沂|鹿儿岛|伦敦|罗安达|洛杉矶|马德里|马尔他|马加丹|马尼拉|满洲里|曼谷|芒市|米兰|莫斯科|墨尔本|牡丹江|慕尼黑|南昌|南京|南宁|南充|尼斯|宁波|纽约|匹兹堡|普吉|齐齐哈尔|黔江|奇姆肯特|青岛|庆阳|三亚|厦门|揭阳|上海虹桥|上海浦东|深圳|沈阳|圣彼得堡|圣地亚哥|石家庄|思茅|斯德哥尔摩|斯图加特|苏黎世|塔城|塔什干|台北桃园|太原|唐山|腾冲|天津|天水|通辽|吐鲁番|瓦纳|威海|威尼斯|维也纳|潍坊|温州|乌海|乌兰巴托|乌兰浩特|乌鲁木齐|无锡|武汉|西安|西宁|西双版纳|西雅图|悉尼|锡林浩特|香港|新加坡|新西伯利亚|兴义|休斯顿|徐州|雅库茨克|亚特兰大|烟台|延安|延吉|盐城|叶卡捷琳堡|伊尔库茨克|伊宁|宜昌|银川|榆林|运城|札幌|湛江|张家界|长春|长沙|长治|郑州|芝加哥|中卫|重庆|珠海|日内瓦|沙巴|东京|亚的斯亚贝巴|内罗毕|阿布扎比|釜山|邢台|鞍山|锦州|洛阳|南阳|伊斯坦布尔|加尔各答|赣州|赤塔|波茨坦|汉诺威|埃森|多特蒙德|杜伊斯堡|德累斯顿|波鸿|曼海姆|波恩|海德堡|哈根|科伦坡|孟买|库车|伯明翰|阿比让|纽伦堡|奥德萨|罗马|旧金山|都灵|萨尔布吕肯|雅典|孟菲斯|曼彻斯特|菲尼克斯|温哥华|马累|九江|连云港|佛罗伦萨|南通|绵阳|丹佛|奥克兰（美国）|维多利亚|柏林|襄阳|奥斯陆|哥德堡|萨格勒布|布加勒斯特|布拉格|科纳克里|蒙罗维亚|达喀尔|弗里敦|金沙萨|班珠尔|雅温得|图卢兹|毕尔巴鄂|普尔曼|斯波坎|安克雷奇|尤金|萨克拉门托|圣何塞|博伊西|帕斯科|蒙特利尔|阿德莱德|惠灵顿|克拉玛依|达拉斯|扬州|济宁|米苏拉|雷诺|马赛|秦皇岛(山海关)|秦皇岛(北戴河)|那拉提|渥太华|遵义|怀化|明尼阿波利斯|台州|博乐|张掖|黎平|且末|卡尔加里|迈阿密|圣约翰斯|夏洛特|蒙克顿|雷湾|魁北克|哈利法克斯|文山|义乌|柳州|九华山|常德|丹东|黑河|景德镇|吉林|喀纳斯|泸州|梅州|漠河|巴彦淖尔|铜仁|宜宾|黄山|宜春|阿尔山|张家口|吕梁|衢州|高雄|赫尔辛基|哈巴罗夫斯克|里昂|龙岩|六盘水|十堰"
    list_szm = str_szm.split(',')
    list_cs_cn = str_cs_cn.split('|')
    try:
        oflag = list_cs_cn.index(i_orgcity)
    except ValueError:
        print "对不起，不支持该出发地".encode("GBK")
        return -1,-1
    try:
        dflag = list_cs_cn.index(i_dstCity)
    except ValueError:
        print "对不起，不支持该目的地".encode("GBK")
        return -1,-1
    return (list_szm[oflag],list_szm[dflag])

fairleCount = 0 #失败次数
#往返城市
def swap_o_d(i_dstCity, i_orgcity, i_startDate):
    # 出发城市代码
    # orgcity = "PEK"
    # 到达城市代码
    # dstCity = "CGO"
    # 将城市名转换成城市代码
    (orgcity, dstCity) = city_to_code(i_orgcity, i_dstCity)
    if(orgcity == -1 or dstCity == -1):
        return -1
    # 出发日期，格式为：2016-05-15
    startDate = i_startDate
    # 保存数据文件名
    currdatatime = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = "SH-"+currdatatime+"-"+ startDate + ".csv"
    print "正在抓取和解析数据...".encode("GBK")
    for n in range(9):
        loaddata, status_code = data_Crawling(orgcity, dstCity, startDate)
        #超时异常处理，若是超时将等待6分钟
        if( loaddata == -1 or status_code == -1 ):
            print "请求超时,下次请求将在1分钟后进行,请耐心等待...".encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue
        elif( loaddata == -2 or status_code == -2 ):
            print "连接中断,下次请求将在1分钟后进行,请耐心等待...".encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue

        soup = BeautifulSoup(loaddata.decode('utf-8'), "html.parser")
        if (len(soup.find_all("div",id="flightItem1",class_="item")) < 1):
            if (len(soup.find_all("div",class_="price_list")) >= 1):
                return 0
            else:
                print("抓取失败，10s后尝试第%d次抓取数据.....".encode("GBK") % n)
                print loaddata,status_code
                time.sleep(3)
        else:
            break
    if (n >= 8):
        print "抓取失败次数在太多了，无能为力...".encode("GBK")
        #fairleCount = fairleCount+1
        return -1

    # fp = open("data2.html",'w')
    # fp.write(loaddata)
    # fp.close()
    # fpr = open("data2.html")
    # loaddata = fpr.read()
    # fpr.close()
    data_analyze(loaddata, filename)
    # data_analyze(loaddata,"PEK-CAN2016-05-20.csv")
    return 1

#主函数
def main():

    # i_orgcity = raw_input("出发城市:\n")
    # i_dstCity = raw_input("到达城市:\n")
    # i_startDate = raw_input("出发日期，格式为：2016-05-15:\n")
    list_o_d = [('广州','上海浦东'),
                ('广州','上海虹桥'),
                ('上海浦东','厦门'),
                ('上海虹桥','厦门'),
                ('成都','深圳'),
                ('重庆','深圳'),
                ('杭州','深圳'),
                ('长沙','北京'),
                ('长沙','上海浦东'),
                ('长沙','上海虹桥'),
                ('喀什','乌鲁木齐'),
                ('成都','拉萨'),
                ('郑州','昆明'),
                ('贵阳','北京'),
                ('兰州','北京'),
                ('成都','杭州'),
                ('贵阳','深圳'),
                ('银川','北京'),
                ('昆明','丽江'),
                ('成都','南京'),
                ('重庆','西安'),
                ('重庆','长沙'),
                ('阿克苏','乌鲁木齐'),
                ('南昌','上海虹桥'),
                ('南昌','上海浦东'),
                ('武汉','厦门'),
                ('成都','长沙'),
                ('北京','珠海'),
                ('海拉尔','北京'),
                ('成都','丽江'),
                ('上海虹桥','揭阳'),
                ('杭州','贵阳'),
                ('重庆','济南'),
                ('杭州','厦门'),
                ('成都','青岛'),
                ('重庆','乌鲁木齐'),
                ('济南','西安'),
                ('西双版纳','丽江'),
                ('广州','义乌'),
                ('天津','西安'),
                ('杭州','天津'),
                ('广州','长春'),
                ('成都','兰州'),
                ('南昌','昆明'),
                ('广州','揭阳'),
                ('广州','桂林'),
                ('郑州','贵阳'),
                ('成都','石家庄'),
                ('大庆','北京'),
                ('贵阳','南京'),
                ('重庆','贵阳'),
                ('沈阳','深圳'),
                ('武夷山','厦门')]
    days = [3,7,14,21]
    for day in days:
        
        i_startDate = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        for data in list_o_d:
            i_orgcity = data[0]
            i_dstCity = data[1]
            #i_startDate = "2016-05-29"
            print "目前采集的数据信息为（往来航班）：".encode("GBK"), i_orgcity.encode("GBK"),i_dstCity.encode("GBK"),i_startDate
            flag1 = swap_o_d(i_dstCity, i_orgcity, i_startDate) 
            if(flag1 == 0):
                print "抱歉，该日期无座位或航班。".encode("GBK")
                continue
            elif(flag1 == -1):
                continue
            else:
                print '*********往，结束*********'.encode("GBK")
            #半中场休息
            time.sleep(3)
            flag2 = swap_o_d(i_orgcity, i_dstCity, i_startDate)
            if(flag2 == 0):
                print "抱歉，该日期无座位或航班。".encode("GBK")
                continue
            elif(flag2 == -1):
                continue
            else:
                print '*********来，结束*********'.encode("GBK")
            #中场休息
            time.sleep(3)


    print "任务完成".encode("GBK")
    #print "失败次数： ".encode("GBK"),fairleCount

if __name__ == "__main__":
    main()
