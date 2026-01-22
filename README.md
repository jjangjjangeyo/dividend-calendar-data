# S&P 500 Dividend Calendar Data

S&P 500 종목의 배당락일 데이터를 매일 자동으로 수집하여 JSON으로 제공합니다.

## 데이터 사용법

```javascript
const response = await fetch('https://raw.githubusercontent.com/{username}/dividend-calendar-data/main/data/sp500-dividends.json');
const data = await response.json();
console.log(data.calendar);  // 날짜별 배당 데이터
```

## 데이터 구조

```json
{
  "lastUpdated": "2026-01-22 09:00:00",
  "startDate": "2026-01-22",
  "endDate": "2026-04-22",
  "totalCount": 150,
  "calendar": {
    "2026-01-23": [
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "amount": 0.24,
        "payDate": "2026-02-13",
        "recordDate": "2026-01-24"
      }
    ]
  }
}
```

## 설정 방법

1. 이 레포를 Fork
2. Settings > Secrets and variables > Actions
3. `FMP_API_KEY` 시크릿 추가 (Financial Modeling Prep API 키)
4. Actions 탭에서 워크플로우 활성화

## 데이터 출처

- [Financial Modeling Prep](https://financialmodelingprep.com/) - 배당 캘린더 API
- [S&P 500 Companies](https://github.com/datasets/s-and-p-500-companies) - 종목 목록

## 라이선스

MIT License
