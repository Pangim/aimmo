# aimmo 과제_게시물 CRUD

## [배포주소]

3.144.30.193:8000

## [기술스택]

python, django, djongo, mongodb, postman, jwt, bcrypt, AWS ec2, atlas

## [Team] WithCODE
- 박현우 : 회원가입/로그인 
- 김주형 : 게시글 CRUD 
- 이정아 : 댓글 CRUD
----
## 회원가입 / 로그인
### 1. 회원가입
`POST/users/signup`
- bcrypt을 이용한 패스워드 암호화 및 회원가입 기능
### **request**
```json
{
    "email":"aimmo@gmail.com",
    "name":"에이모",
    "password":"aimmo!!!"
}
```
### 2. 로그인
`POST/users/signin`
- 같은 이메일 유저 로그인 불가
- jwt를 이용한 토큰 생성
### **request**
```json
{
    "email":"aimmo@gmail.com",
    "password":"aimmo!!!"
}
```
### **response**
```json
{
   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.BkBGhl60HeVatsYVwjkXFcrr6XYdNaPyICZSXH9nIP0"
}
```
### 3. 로그인 데코레이터 구현
-  로그인 유효성 검사를 위핸 데코레이터 작성
### 4. unit test
![](https://images.velog.io/images/wjddk97/post/25e071ad-5f7c-4f5e-8451-93e87c1b26bf/tests%20in%204.2915.png)




------
## 게시글CRUD

### 1. 게시글 생성
`POST/postings/`

- login_decorator로 유저확인
- body로 보내진 정보 확인하고 게시글 정보와 맞지 않으면 Key error 반환
- posting_id와 일치하는 게시글 없으면 does not exist error 반환
- 보내진 정보를 기반으로 게시글 생성

### **request**
**게시글**

```json
{
    "title":"가입인사 드립니다",
    "content":"안녕하세요"
    "category_id" : 1
}
```

-----

### 2. 게시글 목록 조회
`GET/postings/<posting_id>/list?search="검색어"

- posting_id가 전달 되지 않으면 error 반환
- 검색어에 해당하는 게시글(게시글 명, 연관된 카테고리) 반환
- 주어진 조건에 해당하는 게시글 목록 조회

### **response**
```json
{
    "result": [{
        "id"         : 1,
        "title"      : "가입인사 드립니다",
        "views"      : 0,
        "category"   : "인사게시판",
        "created_at" : "2021-01-01",
        "updated_at" : "2021-01-01",
        },
        {
         "id"         : 2,
        "title"      : "가입인사 ",
        "views"      : 0,
        "category"   : "인사게시판",
        "created_at" : "2021-01-01",
        "updated_at" : "2021-01-01",
        }
    ]
}
```

### 2. 게시글 상세 조회
`GET/postings/<posting_id>

- posting_id가 전달 되지 않으면 error 반환
- postingd_id에 해당하는 게시글 존재하지 않으면, does not exist error 반환
- posting_id가 올바르면 게시글 조회


### **response**
```json
{
    "result": {
        "id"         : 1,
        "title"      : "가입인사 드립니다",
        "content"    : "안녕하세요",
        "category"   : "인사",
        "views"      : 0,
        "created_at" : "2021-01-01",
        "updated_at" : "2021-01-01",
    }
}
```


### 3. 게시글 수정
`PATCH/postings/<posting_id>`

- posting_id가 전달 되지 않으면 error 반환
- postingd_id에 해당하는 게시글 존재하지 않으면, does not exist error 반환
- login_decorator에서 받은 user_id와 게시글 작성자의 id를 비교하여 다르면 forbidden error 반환
- posting_id, user_id 올바르면 body에서 받은 정보를 기반으로 수정

### **request**

```json
{
    "title" : "가입 인사 안합니다"
    "content" : "안녕하세요 수정수정수정수정수정 "
}
```
----
### 4. 게시글 삭제
`DELETE/postings/comments?id=<comment_id>`

- posting_id가 전달 되지 않으면 error 반환
- postingd_id에 해당하는 게시글 존재하지 않으면, does not exist error 반환
- login_decorator에서 받은 user_id와 게시글 작성자의 id를 비교하여 다르면 forbidden error 반환
- posting_id, user_id 올바르면 게시글 삭제

### 5. unit test 
![image](https://user-images.githubusercontent.com/86050295/139955978-44003f15-3a5c-4132-aef0-9a4f663ea385.png)


-----------
## 댓글CRUD
### 1. 댓글 저장
`POST/postings/comments/<posting_id>`

- login_decorator로 유저확인 
- 자기자신을 참조하는 parent_comment 필드
  - 이 값이 null이면 댓글, 만약 값이 6이라면 id값 6인 댓글의 대댓글이다.
- posting(게시물)이 없을 시 에러 반환

### **request**
**댓글**

```json
{
    "parent_comment":"",
    "content":"hi_aimmo!"
}
```
**comment_id 2인 댓글의 대댓글**

```json
{
    "parent_comment":"2",
    "content":"hi_aimmo!"
}
```
-----
### 2. 댓글 조회
`GET/postings/comments/<posting_id>?offset=0&limit=2`

- 댓글 리스트 반환( 대댓글 리스트 포함)
- 페이지 네이션 구현
- posting(게시물)이 없을 시 에러 반환


### **response**
```json
{
    "comment_list": [
        {
            "comment_id": 1,
            "user_name": "이정아",
            "content": "난이정아야",
            "created_at": "2021-11-02",
            "nested_comment_list": [
                {
                    "comment_id": 6,
                    "user_name": "이정아",
                    "content": "난이정아야4",
                    "created_at": "2021-11-02"
                },
                {
                    "comment_id": 8,
                    "user_name": "이정아",
                    "content": "난이정아야6",
                    "created_at": "2021-11-02"
                }
            ]
        },
        {
            "comment_id": 2,
            "user_name": "이정아",
            "content": "수정했따따따따따따ㄸ따따따ㅏ따따",
            "created_at": "2021-11-02",
            "nested_comment_list": []
        }
    ]
}

```
----

### 3. 댓글 수정
`PATCH/postings/comments?id=<comment_id>`

- login_decorator로 유저확인 
- 유저id와 댓글을 쓴 유저id가 같은지 확인, 다를 시 에러 반환
- posting(게시물)이 없을 시 에러 반환
- 모든 조건 통과 시 UPDATE

### **request**

```json
{
    "content" : "수정수정수정수정수정"
}
```
----
### 4. 댓글 삭제
`DELETE/postings/comments?id=<comment_id>`

- login_decorator로 유저확인 
- 유저id와 댓글을 쓴 유저id가 같은지 확인, 다를 시 에러 반환
- posting(게시물)이 없을 시 에러 반환
- 모든 조건 통과 시 삭제

### 5. unit test 
<img width="409" alt="스크린샷 2021-11-03 오전 12 20 12" src="https://user-images.githubusercontent.com/87896537/139876375-cecb81c8-82d8-45dc-a6b6-88fcf927c3f5.png">


> 회고 블로그<br>
> 박현우 : https://velog.io/@pang/aimmo-%EA%B3%BC%EC%A0%9C-%ED%9A%8C%EA%B3%A0
