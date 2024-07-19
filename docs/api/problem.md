# 문제 관리

## 문제 생성하기

### URL

```
POST /problems/
```

### Permission

| Not Authenticated | Authenticated | Admin |
| :---------------: | :-----------: | :---: |
|         X         |       O       |   O   |

### Body Parameters

지원되는 형식: `multipart/form-data`, `application/json`

| key                | type   | required | example               | description  |
| ------------------ | ------ | -------- | --------------------- | ------------ |
| title              | string | yes      | "A+B"                 |              |
| link               | string | yes      | "https://boj.kr/1000" |              |
| description        | string | yes      | "A+B를 출력한다."     |              |
| input_description  | string | yes      | "첫 번째 줄에..."     |              |
| output_description | string | yes      | "첫 번째 줄에..."     |              |
| memory_limit       | float  | yes      | 128.0                 | MB 단위이다. |
| time_limit         | float  | yes      | 1.0                   | 초 단위이다. |

### Response Example

| status | description |
| ------ | ----------- |
| 200    | OK          |
| 400    | BAD REQUEST |
| 403    | FORBIDDEN   |

```json
{
    "id": 2,
    "analysis": null,
    "title": "A+B",
    "link": "https://www.acmicpc.net/problem/1000",
    "description": "두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.",
    "input_description": "첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
    "output_description": "첫째 줄에 A+B를 출력한다.",
    "memory_limit": 128.0,
    "memory_limit_unit": {
        "name_ko": "메가 바이트",
        "name_en": "Mega Bytes",
        "abbr": "MB"
    },
    "time_limit": 1.0,
    "time_limit_unit": {
        "name_ko": "초",
        "name_en": "Seconds",
        "abbr": "s"
    },
    "created_at": "2024-07-17T10:10:55.275762Z",
    "created_by": {
        "id": 1,
        "profile_image": "http://localhost:8000/media/user/profile/1/b.png",
        "username": "admin"
    },
    "updated_at": "2024-07-17T10:11:06.957807Z"
}
```

## 문제 목록 조회하기 (문제검색)

```
GET /problems/search
```

### Permission

| Not Authenticated | Authenticated | Admin |
| :---------------: | :-----------: | :---: |
|         X         |       O       |   O   |

### Query Parameters

| key | description                                      | example                      |
| --- | ------------------------------------------------ | ---------------------------- |
| q   | 제목의 시작부분이 일치하는 항목을 필터링 합니다. | `/problems/search?q={query}` |

### Response Example

| status | description |
| ------ | ----------- |
| 200    | OK          |
| 400    | BAD REQUEST |
| 403    | FORBIDDEN   |

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "A+B",
            "difficulty": {
                "name_en": "EASY",
                "name_ko": "쉬움",
                "value": 1
            },
            "created_at": "2024-07-17T09:23:17.876425Z",
            "updated_at": "2024-07-17T09:23:17.876456Z"
        }
    ]
}
```

## 문제 상세 정보 조회하기

```
GET /problems/{problemId}/detail
```

문제 상세 정보를 조회합니다.

### Permission

| Not Authenticated |               Authenticated                | Admin |
| :---------------: | :----------------------------------------: | :---: |
|         X         | 자신이 만든 문제 / 속한 크루의 문제만 가능 |   O   |

### Response Example

| status | description |
| ------ | ----------- |
| 200    | OK          |
| 404    | NOT FOUND   |

#### 문제 분석이 존재하지 않는 경우

```json
{
    "id": 1,
    "analysis": null,
    "title": "A+B",
    "link": "https://www.acmicpc.net/problem/1000",
    "description": "두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.",
    "input_description": "첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
    "output_description": "첫째 줄에 A+B를 출력한다.",
    "memory_limit": 128.0,
    "memory_limit_unit": {
        "name_ko": "메가 바이트",
        "name_en": "Mega Bytes",
        "abbr": "MB"
    },
    "time_limit": 1.0,
    "time_limit_unit": {
        "name_ko": "초",
        "name_en": "Seconds",
        "abbr": "s"
    },
    "created_at": "2024-07-17T10:10:55.275762Z",
    "updated_at": "2024-07-17T10:11:06.957807Z"
}
```

#### 문제 분석이 존재하는 경우

```json
{
    "id": 1,
    "analysis": {
        "difficulty": {
            "name_en": "EASY",
            "name_ko": "쉬움",
            "value": 1
        },
        "difficulty_description": "[이 기능은 아직 추가할 예정이 없습니다] 기초적인 계산적 사고와 프로그래밍 문법만 있어도 해결 가능한 수준",
        "tags": [
            {
                "parent": null,
                "key": "math",
                "name_ko": "수학",
                "name_en": "mathematics"
            }
        ],
        "time_complexity": "1",
        "time_complexity_description": "[이 기능은 아직 추가할 예정이 없습니다] 선형시간에 풀이가 가능한 문제. N의 크기에 주의하세요.",
        "hint": [
            "우선 정수를 입력받는 방법에 대해서 찾아보는게 좋을 것 같아요.",
            "정수를 입력받는 방법을 찾았다면, 다음으로는 한 줄에 공백으로 구분된 여러 개의 값을 입력 받는 방법을 찾아보세요."
        ],
        "created_at": "2024-07-18T02:03:24.987329Z"
    },
    "title": "A+B",
    "link": "http://boj.kr/1000",
    "description": "A+B를 출력한다.",
    "input_description": "하나의 줄에 공백을 기준으로 두 정수 A와 B가 주어진다.",
    "output_description": "A+B를 출력한다.",
    "memory_limit": 128.0,
    "memory_limit_unit": {
        "name_ko": "메가 바이트",
        "name_en": "Mega Bytes",
        "abbr": "MB"
    },
    "time_limit": 1.0,
    "time_limit_unit": {
        "name_ko": "초",
        "name_en": "Seconds",
        "abbr": "s"
    },
    "created_at": "2024-07-17T09:23:17.876425Z",
    "updated_at": "2024-07-17T09:23:17.876456Z"
}
```

## 문제 수정하기

```
PUT /problems/{problemId}/detail
```

```
PATCH /problems/{problemId}/detail
```

### Permission

| Not Authenticated |      Authenticated      | Admin |
| :---------------: | :---------------------: | :---: |
|         X         | 자신이 만든 문제만 가능 |   O   |

### Body Parameters

지원되는 형식: `multipart/form-data`, `application/json`

| key                | type   | required | example               | description  |
| ------------------ | ------ | -------- | --------------------- | ------------ |
| title              | string | yes      | "A+B"                 |              |
| link               | string | yes      | "https://boj.kr/1000" |              |
| description        | string | yes      | "A+B를 출력한다."     |              |
| input_description  | string | yes      | "첫 번째 줄에..."     |              |
| output_description | string | yes      | "첫 번째 줄에..."     |              |
| memory_limit       | float  | yes      | 128.0                 | MB 단위이다. |
| time_limit         | float  | yes      | 1.0                   | 초 단위이다. |

### Response Example

| status | description |
| ------ | ----------- |
| 200    | OK          |
| 400    | BAD REQUEST |
| 403    | FORBIDDEN   |
| 404    | NOT FOUND   |

```json
{
    "id": 1,
    "analysis": null,
    "title": "A+B",
    "link": "https://www.acmicpc.net/problem/1000",
    "description": "두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.",
    "input_description": "첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
    "output_description": "첫째 줄에 A+B를 출력한다.",
    "memory_limit": 128.0,
    "memory_limit_unit": {
        "name_ko": "메가 바이트",
        "name_en": "Mega Bytes",
        "abbr": "MB"
    },
    "time_limit": 1.0,
    "time_limit_unit": {
        "name_ko": "초",
        "name_en": "Seconds",
        "abbr": "s"
    },
    "created_at": "2024-07-17T10:10:55.275762Z",
    "updated_at": "2024-07-17T10:11:06.957807Z"
}
```
