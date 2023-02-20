# encoding=utf8

from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow, QAction, QInputDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import QTimer
import sys
import openai
import datetime

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("ChatGPT Client")
        # self.apikey = "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"
        self.resize(800, 600)
        self.apikey = ""
        self.data = ""

        bar = self.menuBar()
        file = bar.addMenu("文件")
        barset = QAction("设置APIKey", file)
        barset.setShortcut("Ctrl+S")
        barset.triggered.connect(self.showDialog)
        file.addAction(barset)

        self.bwindow = ChatGPT()
        centerw = QWidget()
        self.setCentralWidget(centerw)
        lay = QVBoxLayout(centerw)
        lay.addWidget(self.bwindow)

    def showDialog(self):
        text, ok = QInputDialog.getText(self, "Setting APIKey", "输入APIKey:", QLineEdit.Normal, self.bwindow.apikey)
        if ok:
            self.bwindow.apikey = text
            print(text)


class ChatGPT(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apikey = ""
        self.setWindowTitle("ChatGPT Client")
        self.resize(800, 600)
        self.data = ""

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()

        self.textEdit1 = QTextEdit()
        self.textEdit1.setReadOnly(True)
        self.textEdit2 = QTextEdit()
        self.textEdit2.setFixedHeight(100)
        self.textEdit2.textCursor()
        self.textEdit2.setPlaceholderText("请在这里输入内容...")
        self.btnPress1 = QPushButton("发送问题")
        self.btnPress1.setFixedHeight(90)
        self.btnPress1.clicked.connect(self.btnPress1_Clicked)

        layout1.addWidget(self.textEdit1)
        layout1.addLayout(layout2)
        layout2.addWidget(self.textEdit2)
        layout2.addWidget(self.btnPress1)
        self.setLayout(layout1)

    def chatAsk(self):
        if self.apikey == "":
            reply = QMessageBox.information(self, "提示", "APIKey 为空，请设置！！！", QMessageBox.Close, QMessageBox.Close)
            if reply == QMessageBox.Close:
                self.btnPress1.setEnabled(True)
                self.btnPress1.setText("发送问题")
            else:
                pass
        else:
            openai.api_key = self.apikey
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.textEdit2.toPlainText(),
                max_tokens=2048,
                temperature=0.5,
                stop=[" Human:", " AI:"]
            )
            resdata = response["choices"][0]["text"]
            self.data += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n' + resdata.lstrip() + '\n\n'
            self.textEdit1.setPlainText(self.data)
            self.btnPress1.setEnabled(True)
            self.btnPress1.setText("发送问题")

    def btnPress1_Clicked(self):
        self.btnPress1.setEnabled(False)
        self.btnPress1.setText("发送中...")
        QTimer.singleShot(500, self.chatAsk)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
