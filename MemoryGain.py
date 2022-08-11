"""
MemoryGain (c) is a flashcards app.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os
import urllib.request
import sys
import cards
import decks
import stats
import settings
import backups


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self, check_for_update=True):
        if check_for_update:
            # Update checker.
            try:
                html = urllib.request.urlopen("https://memorygain.app")
                if "Version 1.0.2" not in str(html.read()):
                    update_msg = QMessageBox()
                    update_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                    update_msg.setWindowTitle("Update")
                    update_msg.setText("There is an updated version available at https://memorygain.app. Would you like to download the updated version?")
                    update_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    update_msg.setIcon(QMessageBox.Information)
                    update_msg.exec_()
                    if update_msg.clickedButton().text() == "&Yes":
                        os.system("START https://memorygain.app")
                        sys.exit()

            except urllib.error.URLError as e:
                print(e)

            except urllib.error.HTTPError as e:
                print(e)

        self.setWindowTitle("MemoryGain")
        self.setObjectName("main_window")
        self.setMinimumSize(1100, 600)
        self.resize(1100, 600)

        self.setStyleSheet('''
                            QPushButton{
                                padding: 5px;
                                width: 150px;
                                height: 50px;
                            }
                            QLineEdit{
                                height: 60px;
                            }
                            QSpinBox{
                                height: 60px;
                            }
                            ''')

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        self.root_grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.root_grid_layout.setObjectName("root_grid_layout")

        self.main_frame = QtWidgets.QFrame(self.central_widget)
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        self.main_frame_grid_layout = QtWidgets.QGridLayout(self.main_frame)
        self.main_frame_grid_layout.setObjectName("main_frame_grid_layout")

        self.root_grid_layout.addWidget(self.main_frame, 0, 2, 1, 1)

        self.menu_frame = QtWidgets.QFrame(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy)
        self.menu_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.menu_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu_frame.setObjectName("menu_frame")
        self.menu_frame_grid_layout = QtWidgets.QGridLayout(self.menu_frame)
        self.menu_frame_grid_layout.setObjectName("menu_frame_grid_layout")

        self.menu_study_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_study_btn.setObjectName("menu_study_btn")
        self.menu_study_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")
        self.menu_study_btn.clicked.connect(lambda: self.menu_study_btn_clicked())
        self.menu_frame_grid_layout.addWidget(self.menu_study_btn, 0, 0, 1, 1)

        self.menu_add_cards_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_add_cards_btn.setObjectName("menu_add_cards_btn")
        self.menu_add_cards_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_add_cards_btn.setText("Add Cards")
        self.menu_add_cards_btn.clicked.connect(lambda: self.menu_add_cards_btn_clicked())
        self.menu_frame_grid_layout.addWidget(self.menu_add_cards_btn, 1, 0, 1, 1)

        self.menu_decks_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_decks_btn.setObjectName("menu_decks_btn")
        self.menu_decks_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_decks_btn.setText("Decks")
        self.menu_decks_btn.clicked.connect(lambda: self.menu_decks_btn_clicked())
        self.menu_frame_grid_layout.addWidget(self.menu_decks_btn, 2, 0, 1, 1)

        self.menu_search_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_search_btn.setObjectName("menu_search_btn")
        self.menu_search_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_search_btn.setText("Search")
        self.menu_search_btn.clicked.connect(lambda: self.menu_search_btn_clicked())
        self.menu_frame_grid_layout.addWidget(self.menu_search_btn, 3, 0, 1, 1)

        self.menu_stats_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_stats_btn.setObjectName("menu_stats_btn")
        self.menu_stats_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_stats_btn.setText("Statistics")
        self.menu_stats_btn.clicked.connect(lambda: self.menu_stats_btn_clicked())
        self.menu_frame_grid_layout.addWidget(self.menu_stats_btn, 4, 0, 1, 1)

        self.menu_settings_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_settings_btn.setObjectName("menu_settings_btn")
        self.menu_settings_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_settings_btn.setText("Settings")
        self.menu_settings_btn.clicked.connect(lambda: self.menu_settings_btn_clicked())
        self.menu_frame_grid_layout.addWidget(self.menu_settings_btn, 5, 0, 1, 1)

        menu_frame_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.menu_frame_grid_layout.addItem(menu_frame_spacer, 6, 0, 1, 1)

        self.root_grid_layout.addWidget(self.menu_frame, 0, 0, 1, 1)
        self.menu_separator_line = QtWidgets.QFrame(self.central_widget)
        self.menu_separator_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.menu_separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.menu_separator_line.setObjectName("menu_separator_line")

        self.root_grid_layout.addWidget(self.menu_separator_line, 0, 1, 1, 1)
        self.setCentralWidget(self.central_widget)

        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.menu_study_btn_clicked()

    def menu_settings_btn_clicked(self):
        self.clear_layout(self.main_frame_grid_layout)

        self.font_size_label = QtWidgets.QLabel()
        # Minimum width will apply to everything else in column.
        self.font_size_label.setMinimumWidth(260)
        self.font_size_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.font_size_label.setText('Font size:')
        self.main_frame_grid_layout.addWidget(self.font_size_label, 0, 0, 1, 1)

        font_label_selector_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_frame_grid_layout.addItem(font_label_selector_spacer, 0, 1, 1, 1)

        self.font_size_selector = QtWidgets.QSpinBox()
        self.font_size_selector.setMinimum(8)
        self.font_size_selector.setMaximum(14)
        font_size_selector_line_edit = self.font_size_selector.lineEdit()
        font_size_selector_line_edit.setReadOnly(True)
        # QSpinBox font is smaller than regular, so 2 point is added to font.
        self.font_size_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 2))
        self.font_size_selector.setValue(settings.get_font_size())
        self.main_frame_grid_layout.addWidget(self.font_size_selector, 0, 2, 1, 1)

        horizontal_line_1 = QtWidgets.QFrame(self.central_widget)
        horizontal_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        horizontal_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_frame_grid_layout.addWidget(horizontal_line_1, 1, 0, 1, 3)

        self.target_retention_rate_label = QtWidgets.QLabel()
        self.target_retention_rate_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.target_retention_rate_label.setText('Retention rate %:')
        self.main_frame_grid_layout.addWidget(self.target_retention_rate_label, 2, 0, 1, 1)

        self.target_retention_rate_selector = QtWidgets.QSpinBox()
        self.target_retention_rate_selector.setMinimum(50)
        self.target_retention_rate_selector.setMaximum(99)
        target_retention_rate_selector_line_edit = self.target_retention_rate_selector.lineEdit()
        target_retention_rate_selector_line_edit.setReadOnly(True)
        # QSpinBox font is smaller than regular, so 2 point is added to font.
        self.target_retention_rate_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 2))
        self.target_retention_rate_selector.setValue(settings.get_target_retention_rate())
        self.main_frame_grid_layout.addWidget(self.target_retention_rate_selector, 2, 2, 1, 1)

        horizontal_line_2 = QtWidgets.QFrame(self.central_widget)
        horizontal_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        horizontal_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_frame_grid_layout.addWidget(horizontal_line_2, 3, 0, 1, 3)

        self.create_backup_label = QtWidgets.QLabel()
        self.create_backup_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.create_backup_label.setText('Create backup:')
        self.main_frame_grid_layout.addWidget(self.create_backup_label, 4, 0, 1, 1)

        self.create_backup_btn = QtWidgets.QPushButton()
        self.create_backup_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.create_backup_btn.setText('Backup')
        self.create_backup_btn.clicked.connect(lambda: self.create_backup_btn_clicked())
        self.main_frame_grid_layout.addWidget(self.create_backup_btn, 4, 2, 1, 1)

        self.del_backup_label = QtWidgets.QLabel()
        self.del_backup_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.del_backup_label.setText('Delete backup:')
        self.main_frame_grid_layout.addWidget(self.del_backup_label, 5, 0, 1, 1)

        self.del_backup_selector = QtWidgets.QComboBox()
        # The drop down list on ComboBoxes is unusually small so 4 point is added.
        self.del_backup_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 4))
        self.del_backup_selector.setMinimumHeight(60)
        backup_names = backups.get_backup_names()
        for name in backup_names:
            self.del_backup_selector.addItem(name)
        self.main_frame_grid_layout.addWidget(self.del_backup_selector, 5, 1, 1, 1)

        self.del_backup_btn = QtWidgets.QPushButton()
        self.del_backup_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.del_backup_btn.setText('Delete')
        self.del_backup_btn.clicked.connect(lambda: self.del_backup_btn_clicked())
        self.main_frame_grid_layout.addWidget(self.del_backup_btn, 5, 2, 1, 1)

        self.restore_backup_label = QtWidgets.QLabel()
        self.restore_backup_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.restore_backup_label.setText('Restore backup:')
        self.main_frame_grid_layout.addWidget(self.restore_backup_label, 6, 0, 1, 1)

        self.restore_backup_selector = QtWidgets.QComboBox()
        # The drop down list on ComboBoxes is unusually small so 4 point is added.
        self.restore_backup_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 4))
        self.restore_backup_selector.setMinimumHeight(60)
        backup_names = backups.get_backup_names()
        for name in backup_names:
            self.restore_backup_selector.addItem(name)
        self.main_frame_grid_layout.addWidget(self.restore_backup_selector, 6, 1, 1, 1)

        self.restore_backup_btn = QtWidgets.QPushButton()
        self.restore_backup_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.restore_backup_btn.setText('Restore')
        self.restore_backup_btn.clicked.connect(lambda: self.restore_backup_btn_clicked())
        self.main_frame_grid_layout.addWidget(self.restore_backup_btn, 6, 2, 1, 1)

        settings_spacer_above_lower_frame = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(settings_spacer_above_lower_frame, 7, 0, 1, 3)

        self.settings_lower_frame = QtWidgets.QFrame()
        self.settings_lower_frame_grid_layout = QtWidgets.QGridLayout(self.settings_lower_frame)

        self.settings_save_btn = QtWidgets.QPushButton()
        self.settings_save_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.settings_save_btn.setText('Save')
        self.settings_save_btn.clicked.connect(lambda: self.settings_save_btn_clicked())
        self.settings_lower_frame_grid_layout.addWidget(self.settings_save_btn, 0, 0, 1, 1)

        self.settings_cancel_btn = QtWidgets.QPushButton()
        self.settings_cancel_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.settings_cancel_btn.setText('Cancel')
        self.settings_cancel_btn.clicked.connect(lambda: self.settings_cancel_btn_clicked())
        self.settings_lower_frame_grid_layout.addWidget(self.settings_cancel_btn, 0, 1, 1, 1)

        settings_lower_frame_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.settings_lower_frame_grid_layout.addItem(settings_lower_frame_right_spacer, 0, 2, 1, 1)

        self.main_frame_grid_layout.addWidget(self.settings_lower_frame, 8, 0, 1, 3)

    def restore_backup_btn_clicked(self):
        confirm_restore_backup_msg = QMessageBox()
        confirm_restore_backup_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        confirm_restore_backup_msg.setWindowTitle('Confirm Deletion')
        confirm_restore_backup_msg.setText(f'Are you sure you want to restore the app to the state when \'{self.restore_backup_selector.currentText()}\' was created?')
        confirm_restore_backup_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_restore_backup_msg.setDefaultButton(QMessageBox.Cancel)
        confirm_restore_backup_msg.exec_()
        if confirm_restore_backup_msg.clickedButton().text() == 'OK':
            backups.restore_backup(self.restore_backup_selector.currentText())

            self.clear_layout(self.root_grid_layout)
            self.setup_ui(False)
            self.menu_settings_btn_clicked()

    def del_backup_btn_clicked(self):
        confirm_del_backup_msg = QMessageBox()
        confirm_del_backup_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        confirm_del_backup_msg.setWindowTitle('Confirm Deletion')
        confirm_del_backup_msg.setText(f'Are you sure you want to delete \'{self.del_backup_selector.currentText()}\'?')
        confirm_del_backup_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_del_backup_msg.setDefaultButton(QMessageBox.Cancel)
        confirm_del_backup_msg.exec_()
        if confirm_del_backup_msg.clickedButton().text() == 'OK':
            backups.del_backup(self.del_backup_selector.currentText())

            backup_names = backups.get_backup_names()
            self.del_backup_selector.clear()
            self.restore_backup_selector.clear()
            for name in backup_names:
                self.del_backup_selector.addItem(name)
                self.restore_backup_selector.addItem(name)

    def create_backup_btn_clicked(self):
        while True:
            backup_name_input_dialog = QtWidgets.QInputDialog()
            backup_name_input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            backup_name_input_dialog.setWindowTitle('Create Backup')
            backup_name_input_dialog.setLabelText('Name of backup:')
            backup_name_input_dialog.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            ok = backup_name_input_dialog.exec_()
            backup_name = backup_name_input_dialog.textValue()
            backup_name = backup_name.strip()

            if backup_name == '' and ok:
                no_name_msg = QMessageBox()
                no_name_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                no_name_msg.setWindowTitle('Empty Name')
                no_name_msg.setText('Please enter a name.')
                no_name_msg.exec_()
                continue

            if ok:
                backups.create_back_up(backup_name)

            break

        backup_names = backups.get_backup_names()
        self.del_backup_selector.clear()
        self.restore_backup_selector.clear()
        for name in backup_names:
            self.del_backup_selector.addItem(name)
            self.restore_backup_selector.addItem(name)

    def settings_save_btn_clicked(self):
        settings.set_font_size(self.font_size_selector.value())
        settings.set_target_retention_rate(self.target_retention_rate_selector.value())

        self.clear_layout(self.root_grid_layout)
        self.setup_ui(False)
        self.menu_settings_btn_clicked()

    def settings_cancel_btn_clicked(self):
        self.menu_settings_btn_clicked()

    def menu_stats_btn_clicked(self):
        self.clear_layout(self.main_frame_grid_layout)

        self.stats_total_cards_label = QtWidgets.QLabel()
        self.stats_total_cards_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.stats_total_cards_label.setText(f'Total number of cards: {len(cards.search_for_cards(""))}')
        self.stats_total_cards_label.setMinimumHeight(60)
        self.main_frame_grid_layout.addWidget(self.stats_total_cards_label, 0, 0, 1, 1)

        self.stats_retention_label = QtWidgets.QLabel()
        self.stats_retention_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        if type(stats.get_retention_1440()) == float:
            self.stats_retention_label.setText(f'Retention rate: {stats.get_retention_1440()}%')
        else:
            self.stats_retention_label.setText(f'Retention rate: N/A')
        self.stats_retention_label.setMinimumHeight(60)
        self.main_frame_grid_layout.addWidget(self.stats_retention_label, 1, 0, 1, 1)

        self.stats_retention_30_label = QtWidgets.QLabel()
        self.stats_retention_30_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        if type(stats.get_retention_1440()) == float:
            self.stats_retention_30_label.setText(f'Retention rate (previous 30 days): {stats.get_retention_1440(30)}%')
        else:
            self.stats_retention_30_label.setText(f'Retention rate (previous 30 days): N/A')
        self.stats_retention_30_label.setMinimumHeight(60)
        self.main_frame_grid_layout.addWidget(self.stats_retention_30_label, 2, 0, 1, 1)

        stats_lower_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(stats_lower_spacer, 3, 0, 1, 1)

    def menu_search_btn_clicked(self):
        self.search_up_to = 0
        self.clear_layout(self.main_frame_grid_layout)

        self.search_line_edit = QtWidgets.QLineEdit()
        # Line edit needs font to be 3 bigger to match other items.
        self.search_line_edit.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 3))
        self.main_frame_grid_layout.addWidget(self.search_line_edit, 0, 0, 1, 1)

        self.search_btn = QtWidgets.QPushButton()
        self.search_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.search_btn.setText('Search')
        self.search_btn.clicked.connect(lambda: self.search_btn_clicked(self.search_line_edit.text()))
        self.main_frame_grid_layout.addWidget(self.search_btn, 0, 1, 1, 1)

        search_lower_left_spacer =QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(search_lower_left_spacer, 1, 0, 1, 1)

        search_lower_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(search_lower_right_spacer, 1, 1, 1, 1)

    def search_btn_clicked(self, query):
        self.searched_cards = cards.search_for_cards(query)

        if len(self.searched_cards) != 0:
            self.clear_layout(self.main_frame_grid_layout)

            self.search_line_edit = QtWidgets.QLineEdit()
            self.search_line_edit.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_line_edit.setText(query)
            self.main_frame_grid_layout.addWidget(self.search_line_edit, 0, 0, 1, 1)

            self.search_btn = QtWidgets.QPushButton()
            self.search_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_btn.setText('Search')
            self.search_btn.clicked.connect(lambda: self.search_btn_clicked(self.search_line_edit.text()))
            self.main_frame_grid_layout.addWidget(self.search_btn, 0, 1, 1, 1)

            self.search_deck_selector = QtWidgets.QComboBox()
            # The drop down list on ComboBoxes is unusually small so 4 point is added.
            self.search_deck_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 4))
            self.search_deck_selector.setMinimumHeight(60)
            deck_names = decks.get_deck_lines()
            for name in deck_names:
                self.search_deck_selector.addItem(name.replace('\n', ''))
            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.main_frame_grid_layout.addWidget(self.search_deck_selector, 1, 0, 1, 2)

            self.search_qst_text = QtWidgets.QTextEdit()
            self.search_qst_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_qst_text.setText(self.searched_cards[self.search_up_to]['Question'])
            self.search_qst_text.setTabChangesFocus(True)
            self.main_frame_grid_layout.addWidget(self.search_qst_text, 2, 0, 1, 2)

            self.search_ans_text = QtWidgets.QTextEdit()
            self.search_ans_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_ans_text.setText(self.searched_cards[self.search_up_to]['Answer'])
            self.search_ans_text.setTabChangesFocus(True)
            self.main_frame_grid_layout.addWidget(self.search_ans_text, 3, 0, 1, 2)

            self.search_lower_frame = QtWidgets.QFrame()
            self.search_lower_frame_grid_layout = QtWidgets.QGridLayout(self.search_lower_frame)

            self.search_save_btn = QtWidgets.QPushButton()
            self.search_save_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_save_btn.setText('Save')
            self.search_save_btn.clicked.connect(lambda: self.search_save_btn_clicked())
            self.search_lower_frame_grid_layout.addWidget(self.search_save_btn, 0, 0, 1, 1)

            self.search_del_btn = QtWidgets.QPushButton()
            self.search_del_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_del_btn.setText('Delete')
            self.search_del_btn.clicked.connect(lambda: self.search_del_btn_clicked())
            self.search_lower_frame_grid_layout.addWidget(self.search_del_btn, 0, 1, 1, 1)

            search_lower_frame_center_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.search_lower_frame_grid_layout.addItem(search_lower_frame_center_spacer, 0, 2, 1, 1)

            self.search_previous_btn = QtWidgets.QPushButton()
            self.search_previous_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_previous_btn.setText('<')
            self.search_previous_btn.clicked.connect(lambda: self.search_previous_btn_clicked())
            self.search_lower_frame_grid_layout.addWidget(self.search_previous_btn, 0, 3, 1, 1)

            self.search_card_num_label = QtWidgets.QLabel()
            self.search_card_num_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_card_num_label.setText(f'{self.search_up_to + 1} of {len(self.searched_cards)}')
            self.search_card_num_label.setAlignment(Qt.AlignCenter)
            self.search_card_num_label.setMinimumWidth(100)
            self.search_lower_frame_grid_layout.addWidget(self.search_card_num_label, 0, 4, 1, 1)

            self.search_next_btn = QtWidgets.QPushButton()
            self.search_next_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_next_btn.setText('>')
            self.search_next_btn.clicked.connect(lambda: self.search_next_btn_clicked())
            self.search_lower_frame_grid_layout.addWidget(self.search_next_btn, 0, 5, 1, 1)

            self.main_frame_grid_layout.addWidget(self.search_lower_frame, 4, 0, 1, 2)
        else:
            query_not_found_msg = QMessageBox()
            query_not_found_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            query_not_found_msg.setWindowTitle('Query not found')
            query_not_found_msg.setText('There were no cards that contained that query.')
            query_not_found_msg.exec_()

    def search_save_btn_clicked(self):
        if self.search_qst_text.toPlainText().strip() == '':
            enter_qst_msg = QMessageBox()
            enter_qst_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            enter_qst_msg.setWindowTitle('Enter Question')
            enter_qst_msg.setText('Please enter a question')
            enter_qst_msg.exec_()
            return

        if self.search_qst_text.toPlainText() == self.searched_cards[self.search_up_to]['Question']:
            cards.write_card_edit_save(self.searched_cards[self.search_up_to], self.search_qst_text.toPlainText(), self.search_ans_text.toPlainText())
        # Makes sure an edited question does not already exist.
        else:
            if cards.check_qst_exists(self.search_qst_text.toPlainText()):
                duplicate_qst_msg = QMessageBox()
                duplicate_qst_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                duplicate_qst_msg.setWindowTitle('Duplicate Question')
                duplicate_qst_msg.setText('That question already exists, please enter a different question.')
                duplicate_qst_msg.exec_()
                return
            else:
                cards.write_card_edit_save(self.searched_cards[self.search_up_to], self.search_qst_text.toPlainText(), self.search_ans_text.toPlainText())

        cards.change_deck(self.searched_cards[self.search_up_to]['Deck'], self.search_deck_selector.currentText(), self.searched_cards[self.search_up_to]['Question'])

        self.searched_cards[self.search_up_to]['Question'] = self.search_qst_text.toPlainText()
        self.searched_cards[self.search_up_to]['Answer'] = self.search_ans_text.toPlainText()
        self.searched_cards[self.search_up_to]['Deck'] = self.search_deck_selector.currentText()

    def search_del_btn_clicked(self):
        cards.del_card(self.searched_cards[self.search_up_to])
        self.searched_cards.pop(self.search_up_to)

        if len(self.searched_cards) == 0:
            self.menu_search_btn_clicked()
        elif len(self.searched_cards) == self.search_up_to:
            self.search_up_to = self.search_up_to - 1

            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setText(self.searched_cards[self.search_up_to]['Answer'])

            self.search_card_num_label.setText(f'{self.search_up_to + 1} of {len(self.searched_cards)}')
        else:
            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setText(self.searched_cards[self.search_up_to]['Answer'])

            self.search_card_num_label.setText(f'{self.search_up_to + 1} of {len(self.searched_cards)}')

        self.menu_study_btn.setText(f'Study {cards.get_num_to_study()}')

    def search_previous_btn_clicked(self):
        if self.search_up_to > 0:
            self.search_up_to = self.search_up_to - 1

            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setText(self.searched_cards[self.search_up_to]['Answer'])

            self.search_card_num_label.setText(f'{self.search_up_to + 1} of {len(self.searched_cards)}')

    def search_next_btn_clicked(self):
        if self.search_up_to < len(self.searched_cards) - 1:
            self.search_up_to = self.search_up_to + 1

            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setText(self.searched_cards[self.search_up_to]['Answer'])

            self.search_card_num_label.setText(f'{self.search_up_to + 1} of {len(self.searched_cards)}')

    def menu_study_btn_clicked(self, deck=False):
        self.clear_layout(self.main_frame_grid_layout)

        self.current_card = cards.get_card(deck)

        if self.current_card:
            self.study_qst_text = QtWidgets.QTextEdit(self.main_frame)
            self.study_qst_text.setTabChangesFocus(True)
            self.study_qst_text.setObjectName("study_qst_text")
            self.study_qst_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_qst_text.setText(self.current_card['Question'])
            self.study_qst_text.setReadOnly(True)
            self.study_qst_text.setStyleSheet('''
                                            #study_qst_text{
                                                background-color: transparent;
                                                border: none;
                                                color: black;
                                            }
            ''')
            self.main_frame_grid_layout.addWidget(self.study_qst_text, 0, 0, 1, 1)

            self.study_ans_text = QtWidgets.QTextEdit(self.main_frame)
            self.study_ans_text.setTabChangesFocus(True)
            self.study_ans_text.setObjectName("study_ans_text")
            self.study_ans_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_ans_text.setReadOnly(True)
            self.study_ans_text.setStyleSheet('''
                                                #study_ans_text{
                                                    background-color: transparent;
                                                    border: none;
                                                    color: black;
                                                }
            ''')
            self.main_frame_grid_layout.addWidget(self.study_ans_text, 1, 0, 1, 1)

            self.study_lower_btns_frame = QtWidgets.QFrame(self.main_frame)
            self.study_lower_btns_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.study_lower_btns_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.study_lower_btns_frame.setObjectName("study_lower_btns_frame")
            self.study_lower_btns_frame_grid_layout = QtWidgets.QGridLayout(self.study_lower_btns_frame)
            self.study_lower_btns_frame_grid_layout.setObjectName("study_lower_btns_frame_grid_layout")

            self.study_ans_btn = QtWidgets.QPushButton(self.study_lower_btns_frame)
            self.study_ans_btn.setObjectName("study_ans_btn")
            self.study_ans_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_ans_btn.setText("Answer")
            self.study_ans_btn.setFocus()
            self.study_ans_btn.clicked.connect(lambda: self.study_ans_btn_clicked())
            self.study_lower_btns_frame_grid_layout.addWidget(self.study_ans_btn, 0, 1, 1, 1)

            study_lower_btns_frame_right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_right_spacer, 0, 2, 1, 1)

            study_lower_btns_frame_left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_left_spacer, 0, 0, 1, 1)

            self.main_frame_grid_layout.addWidget(self.study_lower_btns_frame, 2, 0, 1, 1)
        else:
            self.study_completed_label = QtWidgets.QLabel()
            self.study_completed_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_completed_label.setText('Study completed.')
            self.study_completed_label.setMinimumHeight(60)
            self.main_frame_grid_layout.addWidget(self.study_completed_label, 0, 0, 1, 1)

            completed_lower_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.main_frame_grid_layout.addItem(completed_lower_spacer, 1, 0, 1, 1)

    def study_ans_btn_clicked(self):
        self.study_ans_text.setText(self.current_card["Answer"])

        # Done to change focus off of self.study_ans_btn before it is cleared.
        self.menu_study_btn.setFocus()

        self.clear_layout(self.study_lower_btns_frame_grid_layout)

        study_lower_btns_frame_left_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_left_spacer, 0, 0, 1, 1)

        self.study_correct_btn = QtWidgets.QPushButton()
        self.study_correct_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.study_correct_btn.setText('Correct')
        self.study_correct_btn.clicked.connect(lambda: self.study_correct_btn_clicked())
        self.study_lower_btns_frame_grid_layout.addWidget(self.study_correct_btn, 0, 1, 1, 1)
        self.study_correct_btn.setFocus()

        study_lower_btns_frame_center_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_center_spacer, 0, 2, 1, 1)

        self.study_again_btn = QtWidgets.QPushButton()
        self.study_again_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.study_again_btn.setText('Again')
        self.study_again_btn.clicked.connect(lambda: self.study_again_btn_clicked())
        self.study_lower_btns_frame_grid_layout.addWidget(self.study_again_btn, 0, 3, 1, 1)

        study_lower_btns_frame_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_right_spacer, 0, 4, 1, 1)

    def study_correct_btn_clicked(self):
        cards.correct_ans(self.current_card)
        self.menu_study_btn_clicked(self.current_card['Deck'])
        self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")

    def study_again_btn_clicked(self):
        cards.again_ans(self.current_card)
        self.menu_study_btn_clicked(self.current_card['Deck'])
        self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")

    def menu_add_cards_btn_clicked(self):
        self.clear_layout(self.main_frame_grid_layout)

        # decks.get_deck_lines() returns a list of deck names. If there are names the list will be True, if not, False.
        if decks.get_deck_lines():
            self.add_cards_upper_frame = QtWidgets.QFrame()
            self.add_cards_upper_frame_grid_layout = QtWidgets.QGridLayout(self.add_cards_upper_frame)
            self.main_frame_grid_layout.addWidget(self.add_cards_upper_frame, 0, 0, 1, 1)

            self.add_cards_deck_selector = QtWidgets.QComboBox()
            # The drop down list on ComboBoxes is unusually small so 4 point is added.
            self.add_cards_deck_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 4))
            # UP TO HERE, trying to get combobox text to not be cut.
            self.add_cards_deck_selector.setMinimumHeight(60)
            deck_lines = decks.get_deck_lines()
            for deck in deck_lines:
                deck = deck.replace('\n', '')
                self.add_cards_deck_selector.addItem(deck)
            self.add_cards_upper_frame_grid_layout.addWidget(self.add_cards_deck_selector, 0, 0, 1, 1)

            self.add_cards_qst_text = QtWidgets.QTextEdit()
            self.add_cards_qst_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.add_cards_qst_text.setTabChangesFocus(True)
            self.main_frame_grid_layout.addWidget(self.add_cards_qst_text, 1, 0, 1, 1)

            self.add_cards_ans_text = QtWidgets.QTextEdit()
            self.add_cards_ans_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.add_cards_ans_text.setTabChangesFocus(True)
            self.main_frame_grid_layout.addWidget(self.add_cards_ans_text, 2, 0, 1, 1)

            self.add_cards_lower_frame = QtWidgets.QFrame()
            self.add_cards_lower_frame_grid_layout = QtWidgets.QGridLayout(self.add_cards_lower_frame)
            self.main_frame_grid_layout.addWidget(self.add_cards_lower_frame, 3, 0, 1, 1)

            self.add_card_btn = QtWidgets.QPushButton()
            self.add_card_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.add_card_btn.setText('Add Card')
            self.add_card_btn.clicked.connect(lambda: self.add_card_btn_clicked())
            self.add_cards_lower_frame_grid_layout.addWidget(self.add_card_btn, 0, 1, 1, 1)

            add_cards_lower_frame_left_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.add_cards_lower_frame_grid_layout.addItem(add_cards_lower_frame_left_spacer, 0, 0, 1, 1)

            add_cards_lower_frame_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.add_cards_lower_frame_grid_layout.addItem(add_cards_lower_frame_right_spacer, 0, 2, 1, 1)
        else:
            self.make_deck_label = QtWidgets.QLabel()
            self.make_deck_label.setText('Please make a deck to put cards into.')
            self.make_deck_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.make_deck_label.setMinimumHeight(60)
            self.main_frame_grid_layout.addWidget(self.make_deck_label, 0, 0, 1, 1)

            add_cards_lower_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.main_frame_grid_layout.addItem(add_cards_lower_spacer, 1, 0, 1, 1)

    def add_card_btn_clicked(self):
        if not cards.add_card(self.add_cards_deck_selector.currentText(), self.add_cards_qst_text.toPlainText(), self.add_cards_ans_text.toPlainText()):
            duplicate_qst_msg = QMessageBox()
            duplicate_qst_msg.setWindowTitle('Duplicate')
            duplicate_qst_msg.setText('A card with that question already exists, card not added.')
            duplicate_qst_msg.exec_()
        else:
            self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")
            self.add_cards_qst_text.clear()
            self.add_cards_ans_text.clear()

    def menu_decks_btn_clicked(self):
        self.clear_layout(self.main_frame_grid_layout)

        self.add_deck_line_edit = QtWidgets.QLineEdit()
        # Line edit needs font to be 3 bigger to match other items.
        self.add_deck_line_edit.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 3))
        self.main_frame_grid_layout.addWidget(self.add_deck_line_edit, 0, 0, 1, 1)

        self.add_deck_btn = QtWidgets.QPushButton()
        self.add_deck_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.add_deck_btn.setText('Add Deck')
        self.add_deck_btn.clicked.connect(lambda: self.add_deck_btn_clicked())
        self.main_frame_grid_layout.addWidget(self.add_deck_btn, 0, 1, 1, 1)

        self.del_deck_selector = QtWidgets.QComboBox()
        # The drop down list on ComboBoxes is unusually small so 4 point is added.
        self.del_deck_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 4))
        self.del_deck_selector.setMinimumHeight(60)
        deck_lines = decks.get_deck_lines()
        for deck in deck_lines:
            self.del_deck_selector.addItem(deck.replace('\n', ''))
        self.main_frame_grid_layout.addWidget(self.del_deck_selector, 1, 0, 1, 1)

        self.del_deck_btn = QtWidgets.QPushButton()
        self.del_deck_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.del_deck_btn.setText('Delete')
        self.del_deck_btn.clicked.connect(lambda: self.del_deck_btn_clicked())
        self.main_frame_grid_layout.addWidget(self.del_deck_btn, 1, 1, 1, 1)

        self.rename_deck_selector = QtWidgets.QComboBox()
        # The drop down list on ComboBoxes is unusually small so 4 point is added.
        self.rename_deck_selector.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 4))
        self.rename_deck_selector.setMinimumHeight(60)
        deck_lines = decks.get_deck_lines()
        for deck in deck_lines:
            self.rename_deck_selector.addItem(deck.replace('\n', ''))
        self.main_frame_grid_layout.addWidget(self.rename_deck_selector, 2, 0, 1, 1)

        self.rename_deck_btn = QtWidgets.QPushButton()
        self.rename_deck_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.rename_deck_btn.setText('Rename')
        self.rename_deck_btn.clicked.connect(lambda: self.rename_deck_btn_clicked())
        self.main_frame_grid_layout.addWidget(self.rename_deck_btn, 2, 1, 1, 1)

        deck_lower_left_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(deck_lower_left_spacer, 3, 0, 1, 1)

        deck_lower_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(deck_lower_right_spacer, 3, 1, 1, 1)

    def add_deck_btn_clicked(self):
        deck_name = self.add_deck_line_edit.text().strip()
        if deck_name == '':
            empty_deck_line_msg = QMessageBox()
            empty_deck_line_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            empty_deck_line_msg.setWindowTitle('Deck name')
            empty_deck_line_msg.setText('Please enter a deck name.')
            empty_deck_line_msg.exec_()
            return
        not_duplicate = decks.add_deck(deck_name)
        if not not_duplicate:
            duplicate_deck_msg = QMessageBox()
            duplicate_deck_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            duplicate_deck_msg.setWindowTitle('Duplicate')
            duplicate_deck_msg.setText('Deck already exists.')
            duplicate_deck_msg.exec_()
        self.menu_decks_btn_clicked()

    def del_deck_btn_clicked(self):
        selected_deck_del = self.del_deck_selector.currentText().strip()
        if selected_deck_del == '':
            return

        confirm_del_deck_msg = QMessageBox()
        confirm_del_deck_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        confirm_del_deck_msg.setWindowTitle('Confirm')
        confirm_del_deck_msg.setText(f'Are you sure you want to delete the \'{selected_deck_del}\' deck and all cards in this deck?')
        confirm_del_deck_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_del_deck_msg.setDefaultButton(QMessageBox.Cancel)
        confirm_del_deck_msg.exec_()
        if confirm_del_deck_msg.clickedButton().text() == 'OK':
            decks.del_deck(selected_deck_del)
            self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")
            self.menu_decks_btn_clicked()

    def rename_deck_btn_clicked(self):
        selected_deck_rename = self.rename_deck_selector.currentText().strip()
        if selected_deck_rename == '':
            return
        while True:
            deck_name_input_dialog = QtWidgets.QInputDialog()
            deck_name_input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            deck_name_input_dialog.setWindowTitle('Rename Deck')
            deck_name_input_dialog.setLabelText('Enter the new name for deck:')
            deck_name_input_dialog.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            ok = deck_name_input_dialog.exec_()
            new_deck_name = deck_name_input_dialog.textValue()
            new_deck_name = new_deck_name.strip()

            if new_deck_name == '' and ok:
                no_name_msg = QMessageBox()
                no_name_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                no_name_msg.setWindowTitle('Empty name')
                no_name_msg.setText('Please enter a name.')
                no_name_msg.exec_()
                continue

            if ok:
                cards.change_deck(selected_deck_rename, new_deck_name)
                decks.rename_deck(selected_deck_rename, new_deck_name)

            break

        add_deck_value = self.add_deck_line_edit.text()
        self.menu_decks_btn_clicked()
        self.add_deck_line_edit.setText(add_deck_value)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())


if __name__ == "__main__":
    decks.decks_on_device()
    cards.cards_on_device()
    stats.stats_on_device()
    settings.settings_on_device()
    backups.backups_on_device()
    backups.create_back_up()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
