from playwright.sync_api import Page

from shiny.pytest import create_app_fixture
from shiny.playwright import controller


app = create_app_fixture("hello_shiny.py")


def test_default_greeting(page: Page, app):
    page.goto(app.url)

    label = controller.OutputText(page, "label_greeting")
    label.expect_value("Hello, stranger")


def test_greeting_with_name(page: Page, app):
    page.goto(app.url)

    name_input = controller.InputText(page, "input_name")
    label = controller.OutputText(page, "label_greeting")

    name_input.set("Yves")
    label.expect_value("Hello, Yves")


def test_greeting_clears_to_stranger(page: Page, app):
    page.goto(app.url)

    name_input = controller.InputText(page, "input_name")
    label = controller.OutputText(page, "label_greeting")

    name_input.set("Alice")
    label.expect_value("Hello, Alice")

    name_input.set("")
    label.expect_value("Hello, stranger")
