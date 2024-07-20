import requests
import pandas as pd

from bs4 import BeautifulSoup


def get_basic():
    # Replace XXXXXXX with the stock code you want to fetch data for
    stock_code = '005930'

    # Set the URL for the KRX API
    url = f'https://finance.naver.com/item/main.nhn?code={stock_code}'

    # Make a request to the API and get the HTML response
    response = requests.get(url)

    # Parse the HTML response using a parser such as BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the PER and PBR values in the parsed HTML
    per = soup.find('em', {'id': '_per'}).text
    pbr = soup.find('em', {'id': '_pbr'}).text

    # Print the PER and PBR values
    print(f"PER: {per}, PBR: {pbr}")


def NS_users_crawler(codes, page):
    # User-Agent 설정
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    result_df = pd.DataFrame([])

    n_ = 0
    for page in range(1, page):
        n_ += 1
        if (n_ % 10 == 0):
            print('================== Page ' + str(page) + ' is done ==================')
        url = "https://finance.naver.com/item/board.naver?code=%s&page=%s" % (codes, str(page))
        # html → parsing
        html = requests.get(url, headers=headers).content
        # 한글 깨짐 방지 decode
        soup = BeautifulSoup(html.decode('euc-kr', 'replace'), 'html.parser')
        table = soup.find('table', {'class': 'type2'})
        tb = table.select('tbody > tr')

        for i in range(2, len(tb)):
            if len(tb[i].select('td > span')) > 0:
                date = tb[i].select('td > span')[0].text
                title = tb[i].select('td.title > a')[0]['title']
                views = tb[i].select('td > span')[1].text
                pos = tb[i].select('td > strong')[0].text
                neg = tb[i].select('td > strong')[1].text
                table = pd.DataFrame({'날짜': [date], '제목': [title], '조회': [views], '공감': [pos], '비공감': [neg]})
                result_df = result_df.append(table)

    return result_df


def get_naver_finance_coinfo(code):
    # url = "https://finance.naver.com/item/coinfo.naver?code=%s" % (code)
    url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}".format(code)
    print(' > url : ', url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    req = requests.get(url, headers=headers).content

    # 한글 깨짐 방지 decode
    # soup = BeautifulSoup(req.decode('euc-kr', 'replace'), 'html.parser'))
    soup = BeautifulSoup(req.decode('utf-8', 'replace'), 'html.parser')

    print('-' * 100)
    print(soup.title)
    print(soup.find('title'))
    print(soup.a)
    print(soup.find('a'))

    print('-' * 100)
    print(soup.a.attrs)
    print(soup.a.attrs['href'])

    print('-' * 100)
    print(soup.select_one('title'))
    print(soup.select_one('title').get_text())
    print(soup.select_one('title').string.replace(' ',''))

    print('-' * 100)
    # # print(soup.find_all('a', attrs={'class': 'cmp-table'}))
    # print(soup.select_one('td.line')) # tag.class > tag.class > tag.class ...
    # print(soup.select_one('#contentWrap')) # id > tag.class ...
    # print(soup.select('td[title="지피클럽"]')) # 'tag[type="value"]' > 'tag[type="value"]'

    # 'tag[type="value"]' > 'tag[type="value"]'
    print(soup.select('td[class="cmp-table-cell td0301"] > dl > dt[class="line-left"] > b[class="num"]')[0].get_text())

