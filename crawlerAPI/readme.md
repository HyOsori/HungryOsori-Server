API
=============================

1. ȸ������
-----------------------------
- url: api/signup/ POST METHOD�� ȸ������ ��û�� ����.  (�̸��� ���� �� url�� ����)

- �ʿ� ������

Data|Description
---|---
email|�̸������ľ��̵�
password|��й�ȣ
name|����� �̸�
sign_up_type|% ȸ������ Ÿ��

% ȸ������ Ÿ���� email�� �����̹Ƿ� 'email'��

- Response
{
	"message":"Success"
	"ErrorCode":0
}

- ErrorCode

Data|Description|
---|---
0|����
-1|����
-100|�̹� �����ϴ� ����
-200|�߸��� �̸��� ����


2.  �Ҽ� ȸ������/�α���
-----------------------------
- url : api/social_sign/  POST�������
�ش� url�� ���ٽ� �ش� �Ҽ� ��ü�� ���Ե� ���̵� ������ ȸ������ �� �α��� ó��, ������ ���Ե� ȸ���� �ٷ� �α��� ó��

- �ʿ� ������

Data|Description
---|---
email|�̸������ľ��̵�
name|����� �̸�
sign_up_type|% ȸ������ Ÿ��

% ȸ�� ���� Ÿ���� �ش� �Ҽ� ��ü�� ����  
ex) facebook, google, ���

- Response
{'token': token, 'email': email, 'message': "Login success", 'ErrorCode': 0}

- ErrorCode

Data|Description|
---|---
0|����
-1|����
-100|�̹� �����ϴ� ����(���Խ�)
-101|���� ����(�α��ν�)
-200|�߸��� �̸��� ����(���Խ�)
-300|���� ������ ����� ����(���Խ�)
-201|�α��ν� ���� �̸��� ����
-400|�α��ν� Ǫ�� ��ū ����
-500|�α��ν� ȸ������Ÿ�� ����

3. �α���
-----------------------------
- url: api/signin/ POST METHOD���� ������.

- �ʿ� ������

Data|Description|
---|---
email|����� ���̵�
password|��й�ȣ
push_token|Pushtoken

* Response
{'token': token, 'email': email, 'message': "Login success", 'ErrorCode': 0}

* ErrorCode

Data|Description
---|---
0|����
-1|����
-100|���̵� ����
-200|��й�ȣ ����
-300|Ǫ����ū ����
-101|���� ���� ����
-102|�̸��� ���� �ʿ�
-103|�̸��� ����
-201|��й�ȣ ����

4. �α׾ƿ�
-----------------------------
- url: api/logout/ POST METHOD��

- �ʿ� ������

Data|Description  
---|---
�ʿ����|�ʿ����


- response {
	'ErrorCode': 0, 'message': 'Logout success' }


- ErrorCode

Data|Description
---|---
0|����
-400|�׷� ���� ����
-300|��ū ����(�α��ε� ���� �ƴ�)
-200|Ǫ����ū�� ��ϵ��� ���� ����

5. ũ�ѷ� ��ü ���
-----------------------------
* url: api/crawlers/ GET METHOD�� ��û HTTP HEADER�� key: Authorization, value: Token {{token}} �� ������ ��������� �ùٸ��� ����

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
0|����
-100|ũ�ѷ��� �Ѱ��� ����
detail: no authentication credentials|�������� ���� ����

6. ������ �������� ũ�ѷ� ���
-----------------------------
* url:/subscription/ get ������� ��û

Data|Description
---|---
������|���ʿ�

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


6. ������ �����Ϸ��� ũ�ѷ� �߰�
-----------------------------
* url: /subscriptions/ POST������� ��û

Data|Description
---|---
crawler_id|�����Ϸ��� ũ�ѷ� id

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

Data|Description
---|---
0|����
-101|ũ�ѷ� ������ ������
-200|�׷� ũ�ѷ� ����

7. ������ �����ϰ� �ִ� ũ�ѷ� ����
-----------------------------
* url: /subscription/ �� url�� delete �޼ҵ� �̿�

Data|Description
---|---
crawler_id|�����Ϸ��� ũ�ѷ� id

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

Data|Description
---|---
0|����
-101|request�� ũ�ѷ� ������ ����
-200|��ȿ���� ���� �������

9. Ǫ����ū ���
-----------------------------
* url: /push_token/ POST������� ��û

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
|0|����|
|-100|request�� Ǫ����ū ������ ����|

10. Ǫ����ū ����
---------------------------
* url: /push_token/ DELETE������� ��û

* �ʿ� ������ ����, �α��ε� ������ Ǫ�� ��ū�� ����

* Response
{
	"message":"success",
	"ErrorCode":0
}

* ErrorCode

|Data|Description|
---|---
|0|����|
|-100|request�� Ǫ����ū ������ ����|


11. �н����� ����
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

12. ��й�ȣ ã��
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
