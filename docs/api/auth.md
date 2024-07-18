# 사용자 인증

## 회원 가입하기

### URL

```
POST /auth/signup
```

### Body Parameters

지원되는 형식: `multipart/form-data`

| key           | type   | required | example         |
| ------------- | ------ | -------- | --------------- |
| email         | string | yes      | "test@test.com" |
| username      | string | yes      | "test"          |
| password      | string | yes      | "test1234"      |
| boj_username  | string | yes      | "test"          |
| profile_image | file   | no       | "test"          |

### Response Example

| status | description                            |
| ------ | -------------------------------------- |
| 201    | 정상적으로 가입됨                      |
| 400    | 일부 필드의 정보가 누락되었거나 잘못됨 |

```json
{
    "id": 1,
    "email": "test@test.com",
    "profile_image": "http://localhost:8000/media/user/profile/1/b.png",
    "username": "test",
    "boj": {
        "username": "test",
        "profile_url": "https://boj.kr/test",
        "tier": 30,
        "tier_updated_at": "2024-07-17T07:02:29Z"
    },
    "created_at": "2024-07-17T06:53:57Z",
    "last_login": "2024-07-18T04:52:42.892169Z"
}
```

## 로그인 하기

### URL

```
POST /auth/signin
```

### Body Parameters

지원되는 형식: `multipart/form-data`, `application/json`

| key      | type   | required | example         |
| -------- | ------ | -------- | --------------- |
| email    | string | yes      | "test@test.com" |
| password | string | yes      | "test1234"      |

### Response Example

### Response Example

| status | description                                                       |
| ------ | ----------------------------------------------------------------- |
| 200    | 로그인에 성공함                                                   |
| 400    | 로그인에 실패함 (누락되었거나 잘못된 사용자 이메일 혹은 비밀번호) |

```json
{
    "id": 1,
    "email": "test@test.com",
    "profile_image": "http://localhost:8000/media/user/profile/1/b.png",
    "username": "test",
    "boj": {
        "username": "test",
        "profile_url": "https://boj.kr/test",
        "tier": 30,
        "tier_updated_at": "2024-07-17T07:02:29Z"
    },
    "created_at": "2024-07-17T06:53:57Z",
    "last_login": "2024-07-18T04:52:42.892169Z"
}
```

## 로그아웃 하기

### URL

```
GET /auth/signout
```

### Response Example

| status | description       |
| ------ | ----------------- |
| 200    | 로그아웃에 성공함 |

```json
{
    "id": 1,
    "email": "test@test.com",
    "profile_image": "http://localhost:8000/media/user/profile/1/b.png",
    "username": "test",
    "boj": {
        "username": "test",
        "profile_url": "https://boj.kr/test",
        "tier": 30,
        "tier_updated_at": "2024-07-17T07:02:29Z"
    },
    "created_at": "2024-07-17T06:53:57Z",
    "last_login": "2024-07-18T04:52:42.892169Z"
}
```
