API
=============================
1. ��ü ������ ���� ������ȸ
-----------------------------
url: /users/

2. ȸ������
-----------------------------
- url: /users/ ����Ʈ ���·� ȸ������ ��û�� ����.  

Data|Description
---|--- 
user_id|�̸������ľ��̵�
password|��й�ȣ
name|����� �̸�

- Response
{
	"message":"Success"
	"ErrorCode":0
}

- ErrorCode

|Data|Description|
---|---
|0|����|
|-1|����|
|-100|�̹� �����ϴ� ����|
|-200|�߸��� �̸��� ����|


3. ���������� ���� ������ȸ
-----------------------------
* url:  /users/find/?user_id=osori@osori.com

4. �α���
-----------------------------
* url: /login/ user_id=osori@osori.com password=1234

|Data|Description|
---|---
|user_id|����� ���̵�|
|user_key|�������� �߱��ϴ� Ű, user_key���� request�� ������, �������� �߱�|
|password|��й�ȣ|
|token|Pushtoken|

* Response
{
	"user_key": "...",
	"message":"Success",
	"error":0
}

* ErrorCode

|Data|Description|
---|---
|0|����|
|-1|����|
|-100|���̵� ����|
|-200|��й�ȣ ����|
|-300|���� �ʿ�|	

5. ũ�ѷ� ��ü ���
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
|0|����|
|-100|ũ�ѷ��� �Ѱ��� ����|

6. ������ �������� ũ�ѷ� ���
-----------------------------
* url:/subscriptions/item/ user_id=osori@osori.com user_key=asdf

|Data|Description|
---|---
|user_id|����� ���̵�|
|user_key|�������� �߱��ϴ� Ű|

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
|0|����|
|-100|��ȿ���� ���� ����|
|-200|�����ϰ� �ִ� ũ�ѷ� ����|

7. ������ �����Ϸ��� ũ�ѷ� �߰�
-----------------------------
* url: /subscriptions/ user_id=osori@osori.com user_key=asdf crawler_id=...

|Data|Description|
---|---
|user_id|����� ���̵�|
|user_key|�������� �߱޹��� Ű|
|crawler_id|�����Ϸ��� ũ�ѷ� id|

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|����|
|-100|��ȿ���� ���� ����|
|-1|����|

8. ������ �����ϰ� �ִ� ũ�ѷ� ����
-----------------------------
* url: /subscriptions/item/ user_id=osori@osori.com user_key=asdf crawler_id=... (DELETE�̿�)

|Data|Description|
---|---
|user_id|����� ���̵�|
|user_key|�������� �߱޹��� Ű|
|crawler_id|�����Ϸ��� ũ�ѷ� id|

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|����|
|-100|��ȿ���� ���� ����
|-1|����

9. Ǫ����ū ���
-----------------------------
* url: /tokens/ user_id=osori@osori.com user_key=asdf token=...

|Data|Description|
---|---
|user_id|����� ���̵�|
|user_key|�������� �߱޹��� Ű|
|token|firebase cloud message token|

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|����|
|-100|��ȿ���� ���� ����|
|-1|����|

10. �н����� ����
-----------------------------
* url:/password_change/ user_id=osori@osori.com password=1234 new_password=123

|Data|Description|
---|---
|user_id|����ھ��̵�|
|password|���������� ��й�ȣ|
|new_password|������ ��й�ȣ|

* Response
{
	"message":"success", "ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
0|����
-100|���� ��й�ȣ�� �ٸ�
-1|����

11. ��й�ȣ ã��
-------------------------
* url: /send_temp_password/?osori@osori.com/  
�ӽ÷� ��й�ȣ�� �����صΰ� �̸� �̸��Ϸ� �����ִ� ����

* Response
{
	"message":"Temp password sent",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
0|����
-1|����