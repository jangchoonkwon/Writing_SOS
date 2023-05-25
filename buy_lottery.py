from playwright.sync_api import Playwright, sync_playwright
import time
import PySimpleGUI as sg

def run_lottery(playwright: Playwright, user_id: str, user_pw: str, count: int) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://dhlottery.co.kr/user.do?method=login")
    page.fill("[placeholder=\"아이디\"]", user_id)
    page.press("[placeholder=\"아이디\"]", "Tab")
    page.fill("[placeholder=\"비밀번호\"]", user_pw)
    page.press("[placeholder=\"비밀번호\"]", "Tab")
    with page.expect_navigation():
        page.press("form[name=\"jform\"] >> text=로그인", "Enter")
    page.goto(url="https://ol.dhlottery.co.kr/olotto/game/game645.do")
    page.click("text=자동선택")
    page.select_option("select", str(count))
    page.click("text=확인")
    page.click("input:has-text(\"구매하기\")")
    time.sleep(2)
    page.click("text=확인 취소 >> input[type=\"button\"]")
    page.click("input[name=\"closeLayer\"]")
    context.close()
    browser.close()

sg.theme('Dark2')
font_basic = 'D2Coding, 12'
col_1 = [
        [sg.Text('사용자 아이디:', font=font_basic)],
        [sg.Text('사용자 비밀번호:', font=font_basic)],
        [sg.Text('구매 할 개수:', font=font_basic)]
]
col_2 = [
        [sg.InputText(key='user_id', default_text='seendo', size=(14,2))],
        [sg.InputText(key='user_pw', default_text='jang7018!', password_char='*', size=(14,2))],
        [sg.Spin(values=[i for i in range(1, 11)], initial_value=5, key='count', font=font_basic, size=(4,2))]
]
layout = [
        [sg.Column(col_1), sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button('시작', size=(8,1), font=font_basic), sg.Button('종료', size=(8,1), font=font_basic)]
]

window = sg.Window('로또 자동 구매 프로그램', layout, size=(400,140), font=font_basic)

with sync_playwright() as playwright:
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '종료':
            break
        if event == '시작':
            run_lottery(playwright, values['user_id'], values['user_pw'], values['count'])

window.close()
