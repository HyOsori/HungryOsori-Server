1. ��ü ������ ���� ������ȸ
	url: /users/

2. ȸ������
url: /users/ 
�ʿ��׸�(POST)
user_id : �̸������ľ��̵� 
password: ��й�ȣ
name	: ����� �̸�

Response
{
	"message":"Success"
	"ErrorCode":0
}

ErrorCode
0	����
-1	����
-100	�̹� �����ϴ� ����
-200	�߸��� �̸��� ����


3. ���������� ���� ������ȸ
	url:  /users/find/?user_id=osori@osori.com

4. �α���
url: /login/ user_id=osori@osori.com password=1234
user_id		����� ���̵�
user_key	�������� �߱��ϴ� Ű, user_key���� request�� ������, �������� �߱�
password	��й�ȣ
token		Pushtoken

Response
{
	"user_key": "...",
	"message":"Success",
	"error":0
}

ErrorCode
0	����
-1	����
-100	
-200	
-300	

5. ũ�ѷ� ��ü ���
/crawlers/

Response
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

ErrorCode
0	����
-100	ũ�ѷ��� �Ѱ��� ���� 

6. ������ �������� ũ�ѷ� ���
/subscriptions/item/ user_id=osori@osori.com user_key=asdf
user_id		����� ���̵�
user_key	�������� �߱��ϴ� Ű

Response
{
	"message":"success",
	"subscriptions": [
		{
			...
		},
	]
	"ErrorCode":0
}

ErrorCode
0	����
-100	��ȿ���� ���� ����
-200	�����ϰ� �ִ� ũ�ѷ� ����

7. ������ �����Ϸ��� ũ�ѷ� �߰�
/subscriptions/ user_id=osori@osori.com user_key=asdf crawler_id=...
user_id		����� ���̵�
user_key	�������� �߱޹��� Ű
crawler_id	�����Ϸ��� ũ�ѷ� id

Response
{
	"message":"success",
	"ErrorCode":0
}

ErrorCode
0	����
-100	��ȿ���� ���� ����
-1	����

8. ������ �����ϰ� �ִ� ũ�ѷ� ����
/subscriptions/item/ user_id=osori@osori.com user_key=asdf crawler_id=... (DELETE�̿�)
user_id		����� ���̵�
user_key	�������� �߱޹��� Ű
crawler_id	�����Ϸ��� ũ�ѷ� id

Response
{
	"message":"success",
	"ErrorCode":0
}

ErrorCode
0	����
-100	��ȿ���� ���� ����
-1	����

9. Ǫ����ū ���
/tokens/ user_id=osori@osori.com user_key=asdf token=...
user_id		����� ���̵�
user_key	�������� �߱޹��� Ű
token		firebase cloud message token

Response
{
	"message":"success",
	"ErrorCode":0
}

ErrorCode
0	����
-100	��ȿ���� ���� ����
-1	����

10. �н����� ����
/password_change/ user_id=osori@osori.com password=1234 new_password=123
