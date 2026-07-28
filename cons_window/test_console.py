# # from console import LogWindow, StreamWorker

# # import sys
# # import random
# # from PyQt6.QtCore import QObject, pyqtSignal
# # from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
# # import time
# # app = QApplication(sys.argv)
# # log_window = LogWindow()
# # log_window.show()

# # worker = StreamWorker()
# # worker.text_written.connect(log_window.append_log)
# # sys.stdout = worker

# # print("Debug")

# # time.sleep(1)
# # for i in range(10):
# #     print(f"Console log {i}")
# # sys.exit(app.exec())
# # # print("DEbug")

# # file_2.py

# # importing subprocess module 
# import sys
# import subprocess
# from console import StreamWorker
# # running other file using run()


# worker = StreamWorker()
# worker.text_written.connect(subprocess.run(["python", "cons_window/console.py"]))
# sys.stdout = worker

# for i in range(20):
#     print(f"Debug: {i}")


import sys
import time

from PyQt6.QtWidgets import QApplication

from console import ConsoleWindow


class TestConsole:
    def __init__(self, console):
        self.console = console

    def run(self):
        for i in range(100):
            self.console.log(f"Debug {i}")

            # Allow UI updates
            QApplication.processEvents()

            time.sleep(0.5)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    console = ConsoleWindow()
    console.show()

    test = TestConsole(console)
    test.run()

    sys.exit(app.exec())