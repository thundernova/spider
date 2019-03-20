#encoding=utf-8
import requests,re,bs4,time,sys,hashlib,uuid,time,json,base64,rsa,platform,datetime,os,urllib

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
def get_time(format_date,time_pull = None):
    if time_pull:
        return int(time.mktime(time.strptime(time_pull, format_date))*1000)
def standard_work_list():
    return_data = []
    headers = {'User-Agent': UserAgent}
    res = requests.get('http://www.1think.com.cn/globalview/default.php?language=0', headers=headers)
    res.raise_for_status()
    reg_content = res.content.decode('GBK')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.find(id='PuBuLiuDIV').findAll('a')
    quanwen = urllib.parse.unquote_plus('%E5%85%A8%E6%96%87')
    for one_info in infos:
        _one_info = str(one_info)
        if 'img' in _one_info or quanwen in _one_info or 'cysdjd_nr_rt' in _one_info or 'copybd_a' in _one_info or '...' in _one_info:
            continue
        content_dir = re.match('<a.+ onclick="(?P<url>.+?)">(?P<title>.+?)</a>', _one_info)
        if content_dir:
            _datetime = 0
            _url_tmp =content_dir['url'].replace('ArticleURLSkip','')
            skips = re.findall(r'\'(.+?)\'', _url_tmp)
            _url_tmp= 'http://www.1think.com.cn/ViewArticle/html/%s_%s_%s.html'%(skips[0],skips[1],skips[3])

            print({'url': _url_tmp, 'title': content_dir['title'].strip()})
            return_data.append({'url': _url_tmp, 'title': content_dir['title'].strip(), 'datetime': _datetime})
    return return_data


def standard_work_article(target_url):
    return_data = []
    headers = {'User-Agent': UserAgent}
    res = requests.get(target_url, headers=headers)
    res.raise_for_status()
    reg_content = res.content.decode('gbk')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.find(id='HTMLTextContent').findAll('p')
    for one_info in infos:
        content_dir = re.search('<p[\\s\\S]+/p>', str(one_info))
        if content_dir:
            need_content = one_info.text
        else:
            if isinstance(one_info, bs4.NavigableString):
                need_content = one_info
            else:
                continue
        if not need_content.strip():
            continue
        return_data.append(need_content.strip())
    nian = urllib.parse.unquote_plus('%E5%B9%B4')
    yue = urllib.parse.unquote_plus('%E6%9C%88')
    ri = urllib.parse.unquote_plus('%E6%97%A5')

    date = re.search(r"(\d{4}%s\d{1,2}%s\d{1,2}%s)"%(nian, yue, ri), reg_content)
    datetime_dir = re.match('(?P<year>\d{4})%s(?P<month>\d+?)%s(?P<day>\d+?)%s' % (nian, yue, ri), date[0])
    tt_tmp = '%s-%s-%s' % (
        datetime_dir['year'], datetime_dir['month'], datetime_dir['day'])
    _datetime = 0
    if datetime_dir:
        _datetime = get_time('%Y-%m-%d', tt_tmp)
    _title = html_page.find('title').text
    return _datetime, '%s<replace title>%s' % (_title, '\n'.join(return_data))

def main():
   list = standard_work_list()
   for url in list:
       print(standard_work_article(url['url']))



if __name__ == '__main__':
    main()
