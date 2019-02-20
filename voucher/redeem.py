import logging
import os

import azure.functions as func

import datetime
import json

from requests import Session
from requests import request
from robobrowser import RoboBrowser

LOGIN_FORM_URL = 'https://api.groupechservices.ca/en/login?client_id=Club1909&redirect_uri=https%3A%2F%2Fclub1909.com%2Fen%2Fsso&response_type=token'

ACCOUNT_INFO_FROM_DATE_TO_DATE = 'https://club1909.canadiens.com/async/loyalty/TransactionListByDate/?dateFrom={0}&dateTo={1}'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    code = req.params.get('dailycode')
    logging.info(f"dailycode retrieved from http request is {code}")

    if not code:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            code = req_body.get('dailycode')

    if code:
        portal_auth = get_portal_auth()
        response_text = submit_code(code, portal_auth)
        logging.info(f"Today's code {code}  was redeemed with response {response_text}!")
        return func.HttpResponse(json.dumps(response_text), status_code=200, mimetype="application/json")
    else:

        return func.HttpResponse(
            "Pretty please pass a dailycode parameter on the query string or in the request body",
            status_code=400
        )


session: Session = Session()


def get_portal_auth() -> str:
    """
    Attempts login to the Club1909 page and retrieves the cookie FortressPortalAuth

    :return:
    """
    browser = RoboBrowser(session, history=True)
    browser.open(LOGIN_FORM_URL)
    login_form = browser.get_forms()[0]
    login_form['email'] = os.environ['club1909_username']
    login_form['password'] = os.environ['club1909_password']

    # TODO: check get_forms returns one value
    # TODO: check login errors / exceptions

    logging.debug(f"Attempt to login with {os.environ['club1909_username']} and {os.environ['club1909_password']} ")

    browser.submit_form(login_form)
    logging.info(f"Found portal Auth code {browser.session.cookies['.FortressPortalAuth']}")
    return browser.session.cookies['.FortressPortalAuth']


def submit_code(code: str = None, fortress_portal_auth_cookie: str = None) -> json:
    """
    Submits voucher points code to the Club1909 loyalty program

    :param code: voucher string to submit
    :param fortress_portal_auth_cookie: session cookie needed to connect (obtained from login)
    :return: json string
        SUCCESS: {"success":true,"errorCode":"0","errorMessage":"Voucher successfully redeemed","data":{"balance":11160.0,"shouldRefreshPartials":false}}
        ERROR: {"success":false,"errorCode":"H","errorMessage":"The voucher you have entered is out of date","providerCode":"","providerMessage":"","providerId":1}
    """

    url = "https://club1909.canadiens.com/async/Loyalty/RedeemVoucher/"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"voucherCode\"\r\n\r\n" \
              + code + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Referer': "https://club1909.canadiens.com/",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7,es;q=0.6",
        'Cookie': "s_cc=true; s_sq=%5B%5BB%5D%5D; ClientType=App; .FortressPortalAuth=" + fortress_portal_auth_cookie,
        'Cache-Control': "no-cache",
        'Postman-Token': "d9a7522a-dbc6-42cf-8e05-a401f3450916"  # probably we don't need this
    }
    response = request("POST", url, data=payload, headers=headers)

    return json.loads(response.content)


def check_current_points():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    browser = RoboBrowser(session, history=True)
    browser.open(
        ACCOUNT_INFO_FROM_DATE_TO_DATE.format(
            current_date, current_date))
    account_info = json.loads(browser.response.content)  # type: object
    return account_info[0]["AccountBalance"]
