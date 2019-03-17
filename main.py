#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout
import business
from models import WohnungenModel
from controller import Controller
from ui import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    #window.btnBox.layout().setDirection(QHBoxLayout.RightToLeft)
    ctrl = Controller(window)
    ctrl.initialize()
    window.set_controller(ctrl)

    window.show()
    sys.exit(app.exec_())