"""
Playwright UI smoke tests.

Run via:
    nox -s e2e
(requires: `uv sync` + `uv run playwright install chromium`)
"""

from playwright.sync_api import Page, expect


def test_home_tab_shows_address(page: Page, shiny_app: str):
    page.goto(shiny_app)

    # House address is set as the navbar title.
    expect(page.locator("text=Nederenamestraat 15, 9700 Oudenaarde")).to_be_visible()
    expect(page.get_by_role("link", name="Home")).to_be_visible()


def test_base_tables_add_appliance_modal(page: Page, shiny_app: str):
    page.goto(shiny_app)

    page.get_by_role("link", name="Base Tables").click()
    page.locator("#table_select").select_option("Devices")

    page.get_by_role("button", name="Add").click()

    # Modal opened with the Type dropdown showing the proper English labels.
    expect(page.locator(".modal")).to_be_visible()
    expect(page.locator("#mf_type option:checked")).to_have_text("Always on")

    page.get_by_role("button", name="Cancel").click()
    expect(page.locator(".modal")).not_to_be_visible()


def test_delete_confirmation_modal(page: Page, shiny_app: str):
    page.goto(shiny_app)

    page.get_by_role("link", name="Base Tables").click()
    page.locator("#table_select").select_option("Tariffs")

    # No row selected → notification "Please select a row first."
    page.get_by_role("button", name="Delete").click()
    expect(page.locator("text=Please select a row first.")).to_be_visible()
