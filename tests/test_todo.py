import re
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"


def add_todo(page: Page, text: str):
    new_todo = page.get_by_placeholder("What needs to be done?")
    new_todo.fill(text)
    new_todo.press("Enter")


def test_add_item(page: Page):
    page.goto(URL)
    add_todo(page, "Buy milk")
    expect(page.get_by_test_id("todo-title")).to_have_text(["Buy milk"])


def test_complete_item(page: Page):
    page.goto(URL)
    add_todo(page, "Buy milk")
    item = page.get_by_test_id("todo-item").filter(has_text="Buy milk")
    item.get_by_role("checkbox").check()
    expect(item).to_have_class(re.compile("completed"))


def test_active_filter_hides_completed(page: Page):
    page.goto(URL)
    add_todo(page, "Buy milk")
    add_todo(page, "Buy eggs")
    page.get_by_test_id("todo-item").filter(has_text="Buy milk").get_by_role("checkbox").check()
    page.get_by_role("link", name="Active").click()
    expect(page.get_by_test_id("todo-title")).to_have_text(["Buy eggs"])