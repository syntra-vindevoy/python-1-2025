"""Shiny Application Classes.

Object-oriented approach to building Shiny for Python applications.

This module provides:

- `ShinyApp`: Base class for all Shiny applications.
- `HelloWorldApp`: Hello World example implementation.

Usage
-----

Run the Hello World app with:

    from shiny_app import HelloWorldApp
    hello_app = HelloWorldApp()
    hello_app.run()

Notes
-----

Version 1.0.0
Date: 2026-04-22
Author: robinvorsselmans1@hotmail.com
Summary: Object-oriented implementation of Shiny applications.
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import Any

from shiny import App, ui, render

# Add the parent directory to sys.path to access the oo module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oo.loggerfactory import LoggingObject


class ShinyApp(ABC, LoggingObject):
    """Base class for Shiny applications.

    This abstract base class provides the foundational structure for building
    Shiny applications using object-oriented principles.

    Attributes
    ----------
    app : App
        The Shiny App instance created from the UI and server.
    logger : Logger
        Logger instance for this application.

    Methods
    -------
    create_ui()
        Abstract method to create the UI layout.
    create_server(inputs, outputs, session)
        Abstract method to create the server function.
    run(**kwargs)
        Run the Shiny application.
    """

    def __init__(self) -> None:
        """Initialize the Shiny application.

        Creates the UI and server, then initializes the App instance.
        """
        super().__init__()
        self.logger.info(f"Initializing {self.__class__.__name__} application")
        self.ui = self.create_ui()
        self.logger.info("UI created successfully")
        self.app = App(self.ui, self.create_server)
        self.logger.info("Shiny App instance created successfully")

    @abstractmethod
    def create_ui(self) -> ui.Tag:
        """Create the UI layout for the application.

        Returns
        -------
        ui.Tag
            The UI layout object.
        """
        pass

    @abstractmethod
    def create_server(self, inputs: Any, outputs: Any, session: Any) -> None:
        """Create the server function for the application.

        Parameters
        ----------
        inputs : Any
            Shiny inputs object providing access to input values.
        outputs : Any
            Shiny outputs object used to register output renderers.
        session : Any
            Shiny session object.
        """
        pass

    def run(self, **kwargs) -> None:
        """Run the Shiny application.

        Parameters
        ----------
        **kwargs
            Additional arguments to pass to the app run method.
        """
        self.logger.info(f"Starting {self.__class__.__name__} application")
        self.app.run(**kwargs)


class HelloWorldApp(ShinyApp):
    """Hello World Shiny application.

    Simple Shiny for Python example that demonstrates a text input and a reactive greeting label.
    Provides the same functionality as the original functional implementation.

    UI components
    -------------
    - `input_name` : text input for entering a name.
    - `label_greeting` : text output showing "Hello, stranger" when empty, otherwise "Hello, <name>".
    """

    def create_ui(self) -> ui.Tag:
        """Create the UI layout for the Hello World application.

        Returns
        -------
        ui.Tag
            The UI layout with title, text input, and text output.

        Notes
        -----

        Version 1.0.0
        Date: 2026-04-22
        Author: robinvorsselmans
        Summary: Created UI layout matching the original functional implementation.
        """
        self.logger.info("Creating Hello World UI layout")
        ui_layout = ui.page_fluid(
            # Title
            ui.h1("Hello World Example"),
            # Text input field: text input for name
            ui.input_text(id="input_name", label="Enter your name:"),
            # Output label: reactive text output for greeting
            ui.output_text(id="label_greeting"),
        )
        self.logger.info("Hello World UI layout created with input_name and label_greeting components")
        return ui_layout

    def create_server(self, inputs: Any, outputs: Any, session: Any) -> None:
        """Create the server function for the Hello World application.

        Parameters
        ----------
        inputs : Any
            Shiny inputs object providing access to input values.
        outputs : Any
            Shiny outputs object used to register output renderers.
        session : Any
            Shiny session object. This parameter is asserted to be used.

        Returns
        -------
        None

        Notes
        -----

        Version 1.0.0
        Date: 2026-04-22
        Author: robinvorsselmans
        Summary: Implemented server logic matching the original functional implementation.
        """

        assert session
        self.logger.info("Setting up Hello World server function")

        @outputs(id="label_greeting")
        @render.text
        def render_label_greeting() -> str:
            """Render the greeting text for the label output.

            Returns
            -------
            str
                Greeting text: "Hello, stranger" if the input is blank, otherwise "Hello, <name>".

            Notes
            -----

            Version 1.0.0
            Date: 2026-04-22
            Author: robinvorsselmans
            Summary: Implemented greeting logic matching the original functional implementation.
            """

            name = inputs.input_name()

            if not name:
                self.logger.info("User input is empty, returning greeting for stranger")
                return "Hello, stranger"

            self.logger.info(f"User entered name: '{name}', returning personalized greeting")
            return f"Hello, {name}"

        self.logger.info("Hello World server function setup complete with greeting renderer")


# Create an instance for direct usage
hello_app = HelloWorldApp()
hello_app.logger.info("HelloWorldApp instance created and ready for use")
app = hello_app.app

# Don't forget to format and check with ruff before committing!