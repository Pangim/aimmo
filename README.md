# aimmo 과제_게시물 CRUD

## [Team] WithCODE
- 김주형 : 게시글 CRUD 
- 박현우 : 회원가입/로그인  
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
`POST/users/sign`
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
