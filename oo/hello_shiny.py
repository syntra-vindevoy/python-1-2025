"""Hello World Example Shiny app.

Simple Shiny for Python example that demonstrates a text input and a reactive greeting label.

This module exposes the following objects at module scope:

- ``app_ui``: UI layout built with ``ui.page_fluid``.
- ``server``: server function with signature ``server(inputs, outputs, session)``.
- ``app``: Shiny ``App`` instance.

UI components
-------------

- ``input_name`` : text input for entering a name.
- ``label_greeting`` : text output showing "Hello, stranger" when empty, otherwise "Hello, <name>".

Usage
-----

Run locally with:

    shiny run 01_introduction/01_hello_world.py

Notes
-----

Version 1.0.0
Date: 2026-04-21
Author: yves.vindevogel.external@arcelormittal.com
Summary: Initial creation of the example app and alignment with project Shiny conventions.
"""

from typing import Any

from shiny import App, ui, render


app_ui = ui.page_fluid(
    # Title
    ui.h1("Hello World Example"),
    # Text input field: text input for name
    ui.input_text(id="input_name", label="Enter your name:"),
    # Output label: reactive text output for greeting
    ui.output_text(id="label_greeting"),
)


def server(inputs: Any, outputs: Any, session: Any) -> None:
    """Server function for the Hello World Shiny app.

    Parameters
    ----------
    inputs : Any
        Shiny `inputs` object providing access to input values.
    outputs : Any
        Shiny `outputs` object used to register output renderers.
    session : Any
        Shiny `session` object. This parameter is asserted to be used.

    Returns
    -------
    None

    Notes
    -----

    Version 1.0.0
    Date: 2026-04-21
    Author: yves.vindevogel.external@arcelormittal.com
    Summary: Implemented server logic; assert session and registered the greeting output function.
    """

    assert session

    @outputs(id="label_greeting")
    @render.text
    def render_label_greeting() -> str:
        """renders the greeting text for the label output.

        Returns
        -------
        str
            Greeting text: "Hello, stranger" if the input is blank, otherwise "Hello, <name>".

        Notes
        -----

        Version 1.0.0
        Date: 2026-04-21
        Author: yves.vindevogel.external@arcelormittal.com
        Summary: Implemented greeting logic.
        """

        name = inputs.input_name()

        if not name:
            return "Hello, stranger"

        return f"Hello, {name}"


app = App(app_ui, server)

# Don't forget to format and check with ruff before committing!
