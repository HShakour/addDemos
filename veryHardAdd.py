from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
import sys
import random
import time

class AddTwoTaskApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add-2 Task")
        self.setGeometry(300, 300, 500, 400)

        # Define the font
        font = QFont()
        font.setPointSize(16)  # You can adjust this size as needed

        self.display_time = 2     # old display timer

        self.digit_display_time = 700  # Time to display each digit in milliseconds
        self.pause_time = 200  # Pause time between digits in milliseconds
        self.response_time = 4 # Time for user to enter answer
        self.trials = 5 # Number of trials performed back-to-back

        self.current_trial = 0
        self.score = 0

        self.layout = QtWidgets.QVBoxLayout()

        self.number_label = QtWidgets.QLabel("Press Start to Begin")
        self.number_label.setAlignment(QtCore.Qt.AlignCenter)
        self.number_label.setFont(font)  # Set font for number_label
        self.layout.addWidget(self.number_label)

        self.timer_label = QtWidgets.QLabel("")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setFont(font)  # Set font for timer_label
        self.layout.addWidget(self.timer_label)

        self.entry = QtWidgets.QLineEdit()
        self.entry.returnPressed.connect(self.check_answer)
        self.entry.setFont(font)  # Set font for the entry
        self.layout.addWidget(self.entry)

        self.feedback_label = QtWidgets.QLabel("")
        self.feedback_label.setAlignment(QtCore.Qt.AlignCenter)
        self.feedback_label.setFont(font)  # Set font for feedback_label
        self.layout.addWidget(self.feedback_label)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.start_task)
        self.start_button.setFont(font)  # Set font for start_button
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)

    def generate_number(self, length=4):
        self.response_time = length * 0.75
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def add_two(self, number):
        return ''.join(str((int(digit) + 2) % 10) for digit in number)

    def start_task(self):
        self.current_trial = 0
        self.score = 0
        self.start_button.setEnabled(False)
        self.next_trial()

    def next_trial(self):
        if self.current_trial < self.trials:
            self.current_number = self.generate_number(6)
            self.correct_answer = self.add_two(self.current_number)
            self.feedback_label.setText("")
            self.entry.clear()
            self.display_digit_index = 0

            self.show_next_digit()
        else:
            self.number_label.setText(f"Final Score: {self.score}/{self.trials}")
            self.start_button.setEnabled(True)

    def show_next_digit(self):
        if self.display_digit_index < len(self.current_number):
            # Display the current digit
            self.number_label.setText(self.current_number[self.display_digit_index])
            self.display_digit_index += 1

            # Schedule to clear the digit after showing it
            QtCore.QTimer.singleShot(self.digit_display_time, self.clear_digit_display)
        else:
            self.show_input_field()

    def clear_digit_display(self):
        # Clear the digit displayed and pause, then schedule to show the next digit
        self.number_label.setText("")
        QtCore.QTimer.singleShot(self.pause_time, self.show_next_digit)

    def update_timer(self, text="Time remaining"):
        if self.time_remaining > 0:
            self.timer_label.setText(f"{text} - {self.time_remaining}s")
            self.time_remaining -= 1
        else:
            self.timer.stop()
            self.timer_label.setText("")

    def show_input_field(self):
        self.number_label.setText("Enter your answer:")
        self.time_remaining = self.response_time
        self.update_timer("Time remaining")
        self.timer.start(1000)
        self.response_deadline = time.time() + self.response_time

    def check_answer(self):
        if time.time() > self.response_deadline:
            self.feedback_label.setText(f"Out of time! Correct answer: {self.correct_answer}")
            self.feedback_label.setStyleSheet("color: red;")
        else:
            response = self.entry.text().strip()
            if response == self.correct_answer:
                self.feedback_label.setText("Correct!")
                self.feedback_label.setStyleSheet("color: green;")
                self.score += 1
            else:
                self.feedback_label.setText(f"Incorrect. Correct answer: {self.correct_answer}")
                self.feedback_label.setStyleSheet("color: red;")

        self.current_trial += 1
        QtCore.QTimer.singleShot(2000, self.next_trial)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddTwoTaskApp()
    window.show()
    sys.exit(app.exec_())