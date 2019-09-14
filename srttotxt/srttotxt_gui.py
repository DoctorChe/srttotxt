#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PySide2 import QtWidgets
from PySide2 import QtCore

from .ui.ui_mainwindow import Ui_MainWindow
from .scripts.youtube_subtitle_downloader import download_subtitle
from .scripts import srttotxt


class MainWindow(QtWidgets.QMainWindow):
    """Основной класс программы"""

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @QtCore.Slot()
    def download_subtitle(self):
        url = self.ui.lineEdit_url.text()
        file_name = download_subtitle(url)
        if file_name:
            self.ui.lineEdit_input_file.setText(file_name)
            self.ui.statusbar.showMessage("Процесс загрузки файла с субтитрами закончен")
        else:
            self.ui.statusbar.showMessage("Программа youtube-dl не установлена или видео не содержит субтитров")

    @QtCore.Slot()
    def set_txt_file_name(self):
        """
        Установить имя для сохранения файла
        :return:
        """
        input_file = self.ui.lineEdit_input_file.text()
        if input_file:
            base, _ = os.path.splitext(input_file)
            output_file = f"{base}.txt"
            self.ui.lineEdit_output_file.setText(output_file)
        else:
            self.ui.statusbar.showMessage("Задайте имя исходного файла")

    @QtCore.Slot()
    def convert_srt_to_txt(self):
        """
        Перевод текста формата SRT в формат TXT
        :return:
        """
        self.ui.plainTextEdit_output.clear()
        srt_data = self.ui.plainTextEdit_input.toPlainText()
        join = self.ui.checkBox_join.isChecked()
        txt_data = srttotxt.convert_srt_to_txt(srt_data, join)
        self.ui.plainTextEdit_output.setPlainText(txt_data)

    @QtCore.Slot()
    def clean_srt(self):
        """
        Очистка файла от HTML-разметки
        :return:
        """
        self.ui.plainTextEdit_output.clear()
        srt_data = self.ui.plainTextEdit_input.toPlainText()
        srt_data_cleaned = srttotxt.clean_srt(srt_data)
        self.ui.plainTextEdit_input.setPlainText(srt_data_cleaned)

    @QtCore.Slot()
    def paste_from_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        self.ui.lineEdit_url.setText(clipboard.text())

    @QtCore.Slot()
    def copy_to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.ui.plainTextEdit_output.toPlainText())
        self.ui.statusbar.showMessage("Субтитры скопированы в буфер обмена")

    @QtCore.Slot()
    def load_file(self):
        self.ui.plainTextEdit_output.clear()
        srt_path = self.ui.lineEdit_input_file.text()
        if srt_path:
            try:
                with open(srt_path, "r") as f:
                    srt_data = f.read()
                self.ui.plainTextEdit_input.setPlainText(srt_data)
            except IOError:
                print("An IOError has occurred!")
        else:
            self.ui.statusbar.showMessage("Задайте имя файла для загрузки")

    @QtCore.Slot()
    def save_file(self):
        txt_path = self.ui.lineEdit_output_file.text()
        if txt_path:
            txt_data = self.ui.plainTextEdit_output.toPlainText()
            try:
                with open(txt_path, "w") as f:
                    f.write(txt_data)
                self.ui.statusbar.showMessage(f"Файл сохранен ({txt_path})")
            except IOError:
                print("An IOError has occurred!")
        else:
            self.ui.statusbar.showMessage("Задайте имя файла для сохранения")

    @QtCore.Slot()
    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        intput_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Считать данные из файла", "",
                                                               # "SRT Files (*.srt)",
                                                               options=options)
        if intput_file:
            self.ui.lineEdit_input_file.setText(intput_file)
            self.load_file()

    @QtCore.Slot()
    def save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        output_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить файл с текущими данными", "",
                                                               "TXT Files (*.txt)", options=options)

        if output_file:
            self.ui.lineEdit_output_file.setText(output_file)
            self.save_file()

    @QtCore.Slot()
    def show_about_window(self):
        """Отображение окна сведений о программе"""
        return QtWidgets.QMessageBox.about(
            self,
            "О программе",
            f"Конвертер файлов из формата SRT в TXT\nВерсия {srttotxt.version}")

    @QtCore.Slot()
    def show_aboutqt_window(self):
        """Отображение окна сведений о библиотеке Qt"""
        return QtWidgets.QMessageBox.aboutQt(self)


def main():
    app = QtWidgets.QApplication(sys.argv)  # pylint: disable=invalid-name
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
