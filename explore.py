# DON'T DELETE!
# useful to start smth without pytest and not to run in main script!


from alerts_msg.http import AlertHttp

Victim = AlertHttp
assert Victim({}).result_wait() is True
