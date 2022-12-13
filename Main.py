import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import MainPy


class Example(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.ui = MainPy.Ui_Dialog()
        self.ui.setupUi(self)
        # 初始化
        self.init_ui()

    # ui初始化
    def init_ui(self):
        # 初始化方法，这里可以写按钮绑定等的一些初始函数
        self.ui.buttonSelectFile.clicked.connect(self.on_select_file)
        self.ui.buttonOutputPath.clicked.connect(self.on_output_path)
        self.ui.buttonStart.clicked.connect(self.on_start)
        self.ui.checkBox.clicked.connect(self.on_checkbox)
        self.ui.lineEdit.setText(os.getcwd())
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue(0)
        self.show()

    def on_select_file(self):
        file_dialog = QFileDialog()
        filenames = file_dialog.getOpenFileNames(file_dialog, "选择视频文件", "./", "Video(*.mp4)")
        #print(filenames)
        for i in filenames[0]:
            tmp = ''.join(i)
            #print(tmp)
            self.ui.listWidget.addItem(tmp)

    def on_output_path(self):
        file_dialog = QFileDialog()
        filenames = file_dialog.getExistingDirectory(file_dialog, "保存路径")
        tmp = ''.join(filenames)
        self.ui.lineEdit.setText(tmp)

    def on_checkbox(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEdit.setDisabled(1)
            self.ui.buttonOutputPath.setDisabled(1)
        else:
            self.ui.lineEdit.setDisabled(0)
            self.ui.buttonOutputPath.setDisabled(0)

    def on_start(self):
        for i in range(self.ui.listWidget.count()):
            self.decode(self, self.ui.listWidget.item(i).text(), self.ui.lineEdit.text())
            #print(i/self.ui.listWidget.count()*100)
            #print(self.ui.listWidget.count())
            self.ui.progressBar.setValue(float((i+1))/(self.ui.listWidget.count())*100)

    @staticmethod
    def decode(self, filepath, output_path):
        filedir = os.path.dirname(filepath)   #获取文件路径
        file_raw_name = os.path.basename(filepath).split('.')[0] #获取文件名，不含后缀
        file_suffix_name = os.path.splitext(filepath)[-1] #获取文件后缀名
        try:
            file = open(filepath, 'rb')
        except:
            QMessageBox().warning(self, "警告", "打开文件失败")
            return
        first_three = file.read(3)
        if first_three == bytes([255, 255, 255]):#检查文件前三个字节是不是ff,ff,ff
            #print("true")
            file.seek(3)
            byte = file.read()
            file.close()
            if self.ui.checkBox.isChecked():
                output_path = filedir + "\\" + file_raw_name + "_1" + file_suffix_name
            else:
                output_path = output_path + "\\" + file_raw_name + file_suffix_name
            #print(output_path)
            file = open(output_path, 'wb')
            file.seek(0)
            file.write(byte)
            file.close()


# 程序入口
if __name__ == '__main__':
    e = Example()
    sys.exit(e.app.exec())