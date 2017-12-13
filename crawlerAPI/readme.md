API
=============================

1. 회원가입
-----------------------------
- url: api/signup/ POST METHOD로 회원가입 요청을 보냄.  (이메일 사용시 이 url로 접근)

- 필요 데이터

Data|Description
---|---
email|이메일형식아이디
password|비밀번호
name|사용자 이름
sign_up_type|% 회원가입 타입

% 회원가입 타입은 email로 가입이므로 'email'로

- Response
{
	"message":"Success"
	"ErrorCode":0
}

- ErrorCode

Data|Description|
---|---
0|성공
-1|에러
-100|이미 존재하는 유저
-200|잘못된 이메일 포맷


2.  소셜 회원가입/로그인
-----------------------------
- url : api/social_sign/  POST방식으로
해당 url로 접근시 해당 소셜 매체로 가입된 아이디가 없으면 회원가입 후 로그인 처리, 기존에 가입된 회원은 바로 로그인 처리

- 필요 데이터

Data|Description
---|---
email|이메일형식아이디
name|사용자 이름
sign_up_type|% 회원가입 타입

% 회원 가입 타입은 해당 소셜 매체를 넣음  
ex) facebook, google, 등등

- Response
{'token': token, 'email': email, 'message': "Login success", 'ErrorCode': 0}

- ErrorCode

Data|Description|
---|---
0|성공
-1|에러
-100|이미 존재하는 유저(가입시)
-101|없는 유저(로그인시)
-200|잘못된 이메일 포맷(가입시)
-300|유저 데이터 저장시 오류(가입시)
-201|로그인시 유저 이메일 오류
-400|로그인시 푸시 토큰 없음
-500|로그인시 회원가입타입 없음

3. 로그인
-----------------------------
- url: api/signin/ POST METHOD으로 보낸다.

- 필요 데이터

Data|Description|
---|---
email|사용자 아이디
password|비밀번호
push_token|Pushtoken

* Response
{'token': token, 'email': email, 'message': "Login success", 'ErrorCode': 0}

* ErrorCode

Data|Description
---|---
0|성공
-1|에러
-100|아이디 없음
-200|비밀번호 없음
-300|푸시토큰 없음
-101|가입 안한 유저
-102|이메일 인증 필요
-103|이메일 오류
-201|비밀번호 에러

4. 로그아웃
-----------------------------
- url: api/logout/ POST METHOD로

- 필요 데이터

Data|Description  
---|---
필요없음|필요없음


- response {
	'ErrorCode': 0, 'message': 'Logout success' }


- ErrorCode

Data|Description
---|---
0|성공
-400|그런 유저 없음
-300|토큰 누락(로그인된 유저 아님)
-200|푸시토큰이 등록되지 않은 유저

5. 크롤러 전체 목록
-----------------------------
* url: api/crawlers/ GET METHOD로 요청 HTTP HEADER에 key: Authorization, value: Token {{token}} 의 내용을 포함해줘야 올바르게 리턴

* Response
{
	"message":"Success",
	"crawlers":[
		{
			...
		},
		{
			...
		}
	]
	"ErrorCode":0
}

* ErrorCode

Data|Description
---|---
0|성공
-100|크롤러가 한개도 없음
detail: no authentication credentials|인증되지 않은 유저

6. 유저가 구독중인 크롤러 목록
-----------------------------
* url:/subscription/ get 방식으로 요청

Data|Description
---|---
데이터|노필요

* Response
{
	"message":"Successfully return subscriptions",  
	"subscriptions": [
		{
			...
		},
	]
	"ErrorCode":0
}

* ErrorCode


6. 유저가 구독하려는 크롤러 추가
-----------------------------
* url: /subscriptions/ POST방식으로 요청

Data|Description
---|---
crawler_id|구독하려는 크롤러 id

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

Data|Description
---|---
0|성공
-101|크롤러 데이터 전송좀
-200|그런 크롤러 없음

7. 유저가 구독하고 있는 크롤러 제거
-----------------------------
* url: /subscription/ 이 url에 delete 메소드 이용

Data|Description
---|---
crawler_id|구독하려는 크롤러 id

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

Data|Description
---|---
0|성공
-101|request에 크롤러 데이터 없음
-200|유효하지 않은 구독목록

9. 푸시토큰 등록
-----------------------------
* url: /push_token/ POST방식으로 요청

Data|Description
---|---
push_token|firebase cloud message token

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-100|request에 푸시토큰 데이터 없음|

10. 푸시토큰 삭제
---------------------------
* url: /push_token/ DELETE방식으로 요청

* 필요 데이터 없음, 로그인된 유저의 푸시 토큰을 삭제

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-100|request에 푸시토큰 데이터 없음|


11. 패스워드 변경
-----------------------------
* url:/password/
put method를 사용하여 user_id와 password, new_password를 보낸다.
|Data|Description|
---|---
|user_id|사용자아이디|
|password|현재사용중인 비밀번호|
|new_password|변경할 비밀번호|

* Response
{
	"message":"success", "ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
0|성공
-100|현재 비밀번호와 다름
-1|에러

12. 비밀번호 찾기
-------------------------
* url: password/
임시로 비밀번호를 설정해두고 이를 이메일로 보내주는 형태 포스트 방식으로 user_id를 보낸다

|Data|Description|
---|---
|user_id|사용자아이디|

* Response
{
	"message":"Temp password sent",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
0|성공
-1|에러
