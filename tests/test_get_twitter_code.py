import json

from twittercode.getcode import get_daily_code


def test_get_twitter_daily_code(monkeypatch):
    with open('../local.settings.json') as local_settings_file:
        local_settings = json.load(local_settings_file)
        monkeypatch.setenv('twitter_app_key', local_settings['Values']['twitter_app_key'])
        monkeypatch.setenv('twitter_app_secret', local_settings['Values']['twitter_app_secret'])

    code = get_daily_code()
    assert code is not None
    assert code != ""
    print("Code was: " + code)
