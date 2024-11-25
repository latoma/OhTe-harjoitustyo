from invoke import task
from subprocess import call
from sys import platform

@task
def start(ctx):
    ctx.run("python src/main.py")

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
    if platform == "win32":
        call(("start", "htmlcov/index.html"), shell=True)
    else:
        call(("xdg-open", "htmlcov/index.html"))

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")
