import pytest
from src.gmail_client import GmailClient

@pytest.mark.parametrize("msg_to, msg_subject", [("ogtest.sit+010414111111111@gmail.com", "The One 數位保險平台—投保認證碼"), 
                                                 ("ogtest.sit+0929180432@gmail.com" ,"皮皮’s coverage is now effective")])
def test_get_message_id(msg_to, msg_subject):
    client = GmailClient()
    msg_id = client.get_message_id(msg_to, msg_subject)
    print (msg_id)

@pytest.mark.parametrize("msg_to, msg_subject", [("ogtest.sit+010414111111111@gmail.com", "The One 數位保險平台—投保認證碼"), 
                                                 ("ogtest.sit+0929180432@gmail.com" ,"皮皮’s coverage is now effective")])
def test_get_message(msg_to, msg_subject):
    client = GmailClient()
    msg = client.get_message(msg_to, msg_subject)
    print(msg)

@pytest.mark.parametrize("msg_to, msg_subject", [("ogtest.sit+010414111111111@gmail.com", "The One 數位保險平台—投保認證碼"), 
                                                 ("ogtest.sit+0929180432@gmail.com" ,"皮皮’s coverage is now effective")])
def test_get_email_html(msg_to, msg_subject):
    client = GmailClient()
    msg_html = client.get_email_html(msg_to, msg_subject)
    print(msg_html)

@pytest.mark.parametrize("msg_to, msg_subject", [("ogtest.sit+010414111111111@gmail.com", "The One 數位保險平台—投保認證碼"), 
                                                 ("ogtest.sit+0929180432@gmail.com" ,"皮皮’s coverage is now effective")])
def test_get_email_content(msg_to, msg_subject):
    client = GmailClient()
    msg = client.get_email_content(msg_to, msg_subject)
    print(msg)