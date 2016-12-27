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

3. �α���
-----------------------------
* url: /user/ GET������� ������.

|Data|Description|
---|---
|user_id|����� ���̵�|
|user_key|�������� �߱��ϴ� Ű, user_key���� request�� ������, �������� �߱�|
|password|��й�ȣ|
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
|0|����|
|-1|����|
|-100|���̵� ����|
|-200|��й�ȣ ����|
|-300|���� �ʿ�|	

4. ũ�ѷ� ��ü ���
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

5. ������ �������� ũ�ѷ� ���
-----------------------------
* url:/subscription/ 

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

6. ������ �����Ϸ��� ũ�ѷ� �߰�
-----------------------------
* url: /subscriptions/

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

7. ������ �����ϰ� �ִ� ũ�ѷ� ����
-----------------------------
* url: /subscription/ �� url�� delete �޼ҵ� �̿�

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
* url: /tokens/

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
* url:/password/ 
put method�� ����Ͽ� user_id�� password, new_password�� ������.
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
* url: password/ 
�ӽ÷� ��й�ȣ�� �����صΰ� �̸� �̸��Ϸ� �����ִ� ���� ����Ʈ ������� user_id�� ������

|Data|Description|
---|---
|user_id|����ھ��̵�|

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