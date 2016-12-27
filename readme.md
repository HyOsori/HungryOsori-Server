API
=============================
1. 전체 유저에 대한 정보조회
-----------------------------
url: /users/

2. 회원가입
-----------------------------
- url: /users/ 포스트 형태로 회원가입 요청을 보냄.  

Data|Description
---|--- 
user_id|이메일형식아이디
password|비밀번호
name|사용자 이름

- Response
{
	"message":"Success"
	"ErrorCode":0
}

- ErrorCode

|Data|Description|
---|---
|0|성공|
|-1|에러|
|-100|이미 존재하는 유저|
|-200|잘못된 이메일 포맷|

3. 로그인
-----------------------------
* url: /user/ GET방식으로 보낸다.

|Data|Description|
---|---
|user_id|사용자 아이디|
|user_key|서버에서 발급하는 키, user_key없이 request를 날리면, 서버에서 발급|
|password|비밀번호|
|push_token|Pushtoken|

* Response
{
	"user_key": "...",
	"message":"Success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-1|에러|
|-100|아이디 오류|
|-200|비밀번호 오류|
|-300|인증 필요|	

4. 크롤러 전체 목록
-----------------------------
* url: /crawlers/

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

|Data|Description|
---|---
|0|성공|
|-100|크롤러가 한개도 없음|

5. 유저가 구독중인 크롤러 목록
-----------------------------
* url:/subscription/ 

|Data|Description|
---|---
|user_id|사용자 아이디|
|user_key|서버에서 발급하는 키|

* Response
{
	"message":"success",
	"subscriptions": [
		{
			...
		},
	]
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-100|유효하지 않은 유저|
|-200|구독하고 있는 크롤러 없음|

6. 유저가 구독하려는 크롤러 추가
-----------------------------
* url: /subscriptions/

|Data|Description|
---|---
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키|
|crawler_id|구독하려는 크롤러 id|

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-100|유효하지 않은 유저|
|-1|에러|

7. 유저가 구독하고 있는 크롤러 제거
-----------------------------
* url: /subscription/ 이 url에 delete 메소드 이용

|Data|Description|
---|---
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키|
|crawler_id|구독하려는 크롤러 id|

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-100|유효하지 않은 유저
|-1|에러

9. 푸시토큰 등록
-----------------------------
* url: /tokens/

|Data|Description|
---|---
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키|
|token|firebase cloud message token|

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|성공|
|-100|유효하지 않은 유저|
|-1|에러|

10. 패스워드 변경
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

11. 비밀번호 찾기
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