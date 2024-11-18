from invoke import task
from subprocess import call
from sys import platform

@task
def start(ctx):
    ctx.run("python src/main.py")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
    if platform == "win32":
        call(("start", "htmlcov/index.html"), shell=True)
    else:
        call(("xdg-open", "htmlcov/index.html"))