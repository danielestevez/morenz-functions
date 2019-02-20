import json
from voucher.redeem import get_portal_auth
from voucher.redeem import submit_code


def test_redeem_code(monkeypatch):
    with open('../local.settings.json') as local_settings_file:
        local_settings = json.load(local_settings_file)
        monkeypatch.setenv('club1909_username', local_settings['Values']['club1909_username'])
        monkeypatch.setenv('club1909_password', local_settings['Values']['club1909_password'])

        auth_code = get_portal_auth()
        assert auth_code is not None
        assert auth_code != ""
        print("Auth code was: " + auth_code)

        submitted_code_answer = submit_code('XXXXX', auth_code)
        assert submitted_code_answer is not None
        assert submitted_code_answer != ""
        print("Submitted code answer : " + submitted_code_answer['errorMessage'])
