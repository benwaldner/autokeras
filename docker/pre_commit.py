from subprocess import CalledProcessError
from subprocess import check_call


def check_bash_call(string):
    check_call(["bash", "-c", string])


def _run_format_and_flake8():
    files_changed = False

    try:
        check_bash_call("isort -sl -rc -c autokeras tests")
    except CalledProcessError:
        check_bash_call("isort -y -sl -rc autokeras tests")
        files_changed = True

    try:
        check_bash_call("autopep8 -r -i autokeras tests")
    except CalledProcessError as error:
        if error.returncode == 2:
            files_changed = True
        else:
            # there was another type of error
            raise

    if files_changed:
        print("Some files have changed.")
        print("Please do git add and git commit again")
    else:
        print("No formatting needed.")

    print("Running flake8.")
    check_bash_call("flake8 autokeras tests")
    print("Done")

    if files_changed:
        exit(1)


def run_format_and_flake8():
    try:
        _run_format_and_flake8()
    except CalledProcessError as error:
        print("Pre-commit returned exit code", error.returncode)
        exit(error.returncode)


if __name__ == "__main__":
    run_format_and_flake8()
