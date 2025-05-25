#!/bin/bash
if [ ! -f "ui_form.py" ]; then
    if command -v pyside6-uic &> /dev/null; then
        pyside6-uic form.ui -o ui_form.py
    else
        python3.10 -m PySide6.scripts.uic form.ui -o ui_form.py
    fi

    if [ ! -f "ui_form.py" ]; then
        exit 1
    fi
fi

python3.10 mainwindow.py