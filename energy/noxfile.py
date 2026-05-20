import nox


@nox.session(venv_backend="none")
def run(session):
    session.run("uv", "run", "shiny", "run", "src/energy/main.py", env={"PYTHONPATH": "src"})


@nox.session(venv_backend="none")
def test(session):
    session.run(
        "uv", "run", "python", "-m", "unittest", "discover",
        "-s", "tests", "-t", ".",
        "-p", "test_*.py",
    )


@nox.session(venv_backend="none")
def e2e(session):
    session.run("uv", "run", "playwright", "install", "chromium", external=True)
    session.run("uv", "run", "pytest", "tests/views", "-v", env={"PYTHONPATH": "src"})


@nox.session(venv_backend="none")
def lint(session):
    session.run("uv", "run", "ruff", "check", "--fix", "src", "tests")
    session.run("uv", "run", "ruff", "format", "src", "tests")
