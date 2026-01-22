"""
S&P 500 배당 캘린더 데이터 수집 스크립트
GitHub Actions에서 매일 실행

FMP API로 향후 3개월 배당 데이터를 가져와 JSON으로 저장
"""

import json
import os
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# FMP API 키 (GitHub Secrets에서 가져옴)
FMP_API_KEY = os.environ.get('FMP_API_KEY', '')

# S&P 500 목록 URL
SP500_URL = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'

def get_sp500_tickers():
    """S&P 500 종목 목록 가져오기"""
    req = Request(SP500_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as response:
        csv_text = response.read().decode('utf-8')

    tickers = set()
    lines = csv_text.strip().split('\n')
    for line in lines[1:]:  # 헤더 스킵
        cols = line.split(',')
        if cols:
            tickers.add(cols[0].strip())

    print(f"S&P 500 종목 수: {len(tickers)}")
    return tickers

def fetch_dividend_calendar(start_date, end_date):
    """FMP API에서 배당 캘린더 가져오기"""
    # 새 API 엔드포인트 (stable)
    url = f"https://financialmodelingprep.com/stable/dividends-calendar?from={start_date}&to={end_date}&apikey={FMP_API_KEY}"

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except HTTPError as e:
        print(f"API 에러: {e.code} - {e.reason}")
        # 구버전 API 시도
        try:
            url_legacy = f"https://financialmodelingprep.com/api/v3/stock_dividend_calendar?from={start_date}&to={end_date}&apikey={FMP_API_KEY}"
            req2 = Request(url_legacy, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req2) as response:
                return json.loads(response.read().decode('utf-8'))
        except:
            return []

def main():
    if not FMP_API_KEY:
        print("오류: FMP_API_KEY 환경변수가 설정되지 않았습니다.")
        return

    # S&P 500 목록 가져오기
    sp500_tickers = get_sp500_tickers()

    # 오늘부터 3개월 후까지
    today = datetime.now()
    end_date = today + timedelta(days=90)

    start_str = today.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    print(f"배당 데이터 조회: {start_str} ~ {end_str}")

    # FMP API 호출
    all_dividends = fetch_dividend_calendar(start_str, end_str)
    print(f"전체 배당 데이터: {len(all_dividends)}건")

    # S&P 500만 필터링
    sp500_dividends = [
        d for d in all_dividends
        if d.get('symbol') in sp500_tickers
    ]
    print(f"S&P 500 배당 데이터: {len(sp500_dividends)}건")

    # 날짜별로 그룹화
    calendar = {}
    for div in sp500_dividends:
        ex_date = div.get('date')  # 배당락일
        if not ex_date:
            continue

        if ex_date not in calendar:
            calendar[ex_date] = []

        calendar[ex_date].append({
            'symbol': div.get('symbol'),
            'name': div.get('label', div.get('symbol')),
            'amount': div.get('dividend'),
            'payDate': div.get('paymentDate'),
            'recordDate': div.get('recordDate'),
        })

    # 날짜 정렬
    sorted_calendar = dict(sorted(calendar.items()))

    # 결과 저장
    output = {
        'lastUpdated': today.strftime('%Y-%m-%d %H:%M:%S'),
        'startDate': start_str,
        'endDate': end_str,
        'totalCount': len(sp500_dividends),
        'calendar': sorted_calendar
    }

    # JSON 파일로 저장
    os.makedirs('data', exist_ok=True)

    with open('data/sp500-dividends.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: data/sp500-dividends.json")
    print(f"날짜 수: {len(sorted_calendar)}")

if __name__ == '__main__':
    main()
