#!/usr/bin/env python2.6
import os
import sys

activate_this = \
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), ".venv", "bin", "activate_this.py"
        )
    )
execfile(activate_this, dict(__file__=activate_this))

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "project.settings.development"
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
