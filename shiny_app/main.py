import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shiny_app.core.application import ShinyApp
from shiny_app.core.globals import LOGGING_CONFIG
from shiny_app.core.utils import enable_tracing, enable_logging
from shiny_app.controllers.hello_world import HelloWorldController
from shiny_app.models.hello_world import HelloWorldModel
from shiny_app.views.hello_world import HelloWorldView


@enable_logging
@enable_tracing
class HelloWorldApp(ShinyApp):
    def __init__(self):
        super().__init__(
            model=HelloWorldModel,
            view=HelloWorldView,
            controller=HelloWorldController,
        )


app = HelloWorldApp()


def main():
    app.run(log_config=LOGGING_CONFIG)


if __name__ == "__main__":
    main()
