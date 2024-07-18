# 문제 관리

## 문제 생성하기

### URL

```
POST /problem/
```

### Body Parameters

지원되는 형식: `multipart/form-data`

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
GET /problem/search?<query_parameters>
```

### Query Parameters

> TODO: 추후 수정 예정

| key | description |
| --- | ----------- |
|     |             |

### Response Example

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "A+B",
            "link": "http://boj.kr/1000",
            "difficulty": {
                "name_en": "EASY",
                "name_ko": "쉬움",
                "value": 1
            },
            "created_at": "2024-07-17T09:23:17.876425Z",
            "created_by": {
                "id": 1,
                "profile_image": "http://localhost:8000/media/user/profile/1/b.png",
                "username": "admin"
            },
            "updated_at": "2024-07-17T09:23:17.876456Z"
        }
    ]
}
```
