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
import sys
from subprocess import PIPE, Popen
import cards
import decks
import stats
import settings
import backups
import update


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self, check_for_update=True, maximize=True):
        if check_for_update:
            if update.update_available():
                update_msg = QMessageBox()
                update_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                update_msg.setWindowTitle("Update")
                update_msg.setText("An updated version of MemoryGain is available, would you like to update?")
                update_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                update_msg.setIcon(QMessageBox.Information)
                update_msg.exec_()
                if update_msg.clickedButton().text() == "&Yes":
                    update.go_to_memorygain_site()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("MemoryGain")
        self.setObjectName("main_window")
        self.setMinimumSize(1000, 700)

        self.setStyleSheet('''
                            QPushButton{
                                padding: 5px;
                                width: 150px;
                                height: 50px;
                                background-color: rgba(255, 255, 255, 0.1)
                            }
                            QLineEdit{
                                height: 60px;
                            }
                            QScrollBar{
                                background-color: rgba(255, 255, 255, 0.1);
                                width: 8px;
                            }
                            QSpinBox{
                                height: 60px;
                            }
                            ''')
        QtWidgets.QToolTip.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet('''
                                        #central_widget{
                                            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(36, 73, 65, 255), stop:1 rgba(31, 97, 125, 255));
                                        }
        ''')

        self.root_grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.root_grid_layout.setObjectName("root_grid_layout")
        self.root_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.dragable_title_frame = QtWidgets.QFrame()
        self.dragable_title_frame.setObjectName('dragable_title_frame')
        self.dragable_title_frame.setStyleSheet('''#dragable_title_frame{background-color: #447777}''')
        self.dragable_title_frame.setMinimumHeight(30)
        self.root_grid_layout.addWidget(self.dragable_title_frame, 0, 0, 1, 4)

        # Makes it so user can drag by title frame.
        self.mousePressEvent = self.mouse_press_event
        self.dragable_title_frame.mouseMoveEvent = self.move_window

        self.dragable_title_horizontal_layout = QtWidgets.QHBoxLayout(self.dragable_title_frame)
        self.dragable_title_horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.title_app_name_label = QtWidgets.QLabel()
        self.title_app_name_label.setObjectName('title_app_name_label')
        self.title_app_name_label.setStyleSheet('''
                                                #title_app_name_label{
                                                    color: white;
                                                }
        ''')
        self.title_app_name_label.setText('   MemoryGain')
        self.title_app_name_label.setFont(QFont('MS Shell Dlg 2', 10))
        self.dragable_title_horizontal_layout.addWidget(self.title_app_name_label)

        dragable_title_horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dragable_title_horizontal_layout.addItem(dragable_title_horizontal_spacer)

        self.non_dragable_title_frame = QtWidgets.QFrame()
        # 3 70px buttons = 210px.
        self.non_dragable_title_frame.setMaximumSize(210, 40)
        self.non_dragable_title_frame.setObjectName('non_dragable_title_frame')
        self.non_dragable_title_frame.setStyleSheet('''#non_dragable_title_frame{background-color: #447777}''')
        self.non_dragable_title_frame.setMinimumHeight(30)
        self.root_grid_layout.addWidget(self.non_dragable_title_frame, 0, 3, 1, 1)

        self.non_dragable_title_horizontal_layout = QtWidgets.QHBoxLayout(self.non_dragable_title_frame)
        self.non_dragable_title_horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.title_minimize_btn = QtWidgets.QPushButton()
        self.title_minimize_btn.setMaximumSize(70, 40)
        self.title_minimize_btn.clicked.connect(self.title_minimize_btn_clicked)
        self.title_minimize_btn.setFont(QFont('MS Shell Dlg 2', 14))
        self.title_minimize_btn.setText('-')
        self.title_minimize_btn.setObjectName('title_minimize_btn')
        self.title_minimize_btn.setStyleSheet('''
                            #title_minimize_btn{
                                background-color: transparent;
                                color: white;
                            }
                            #title_minimize_btn::hover{
                                background-color: rgba(255, 255, 255, 0.1);
                            }
        ''')
        self.non_dragable_title_horizontal_layout.addWidget(self.title_minimize_btn)

        self.title_maximize_btn = QtWidgets.QPushButton()
        self.title_maximize_btn.setMaximumSize(70, 40)
        self.title_maximize_btn.clicked.connect(self.title_maximize_btn_clicked)
        self.title_maximize_btn.setText('☐')
        self.title_maximize_btn.setFont(QFont('MS Shell Dlg 2', 10))
        self.title_maximize_btn.setObjectName('title_maximize_btn')
        self.title_maximize_btn.setStyleSheet('''
                                    #title_maximize_btn{
                                        background-color: transparent;
                                        color: white;
                                    }
                                    #title_maximize_btn::hover{
                                       background-color: rgba(255, 255, 255, 0.1);
                                    }
                ''')
        self.non_dragable_title_horizontal_layout.addWidget(self.title_maximize_btn)

        self.title_close_btn = QtWidgets.QPushButton()
        self.title_close_btn.setMaximumSize(70, 40)
        self.title_close_btn.clicked.connect(self.title_close_btn_clicked)
        self.title_close_btn.setFont(QFont('MS Shell Dlg 2', 9))
        self.title_close_btn.setText('X')
        self.title_close_btn.setObjectName('title_close_btn')
        self.title_close_btn.setStyleSheet('''
                                            #title_close_btn{
                                                background-color: transparent;
                                                color: white;
                                            }
                                            #title_close_btn::hover{
                                                background-color: rgba(255, 255, 255, 0.1);
                                            }
                        ''')
        self.non_dragable_title_horizontal_layout.addWidget(self.title_close_btn)

        self.main_frame = QtWidgets.QFrame()
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        self.main_frame_grid_layout = QtWidgets.QGridLayout(self.main_frame)
        self.main_frame_grid_layout.setObjectName("main_frame_grid_layout")

        self.root_grid_layout.addWidget(self.main_frame, 1, 2, 1, 2)

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
        self.menu_study_btn.setStyleSheet('''#menu_study_btn{color: white;}''')
        self.menu_study_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")
        self.menu_study_btn.clicked.connect(self.menu_study_btn_clicked)
        self.menu_frame_grid_layout.addWidget(self.menu_study_btn, 0, 0, 1, 1)

        self.menu_add_cards_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_add_cards_btn.setObjectName("menu_add_cards_btn")
        self.menu_add_cards_btn.setStyleSheet('''#menu_add_cards_btn{color: white;}''')
        self.menu_add_cards_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_add_cards_btn.setText("Add Cards")
        self.menu_add_cards_btn.clicked.connect(self.menu_add_cards_btn_clicked)
        self.menu_frame_grid_layout.addWidget(self.menu_add_cards_btn, 1, 0, 1, 1)

        self.menu_decks_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_decks_btn.setObjectName("menu_decks_btn")
        self.menu_decks_btn.setStyleSheet('''#menu_decks_btn{color: white;}''')
        self.menu_decks_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_decks_btn.setText("Decks")
        self.menu_decks_btn.clicked.connect(self.menu_decks_btn_clicked)
        self.menu_frame_grid_layout.addWidget(self.menu_decks_btn, 2, 0, 1, 1)

        self.menu_search_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_search_btn.setObjectName("menu_search_btn")
        self.menu_search_btn.setStyleSheet('''#menu_search_btn{color: white;}''')
        self.menu_search_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_search_btn.setText("Search")
        self.menu_search_btn.clicked.connect(self.menu_search_btn_clicked)
        self.menu_frame_grid_layout.addWidget(self.menu_search_btn, 3, 0, 1, 1)

        self.menu_stats_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_stats_btn.setObjectName("menu_stats_btn")
        self.menu_stats_btn.setStyleSheet('''#menu_stats_btn{color: white;}''')
        self.menu_stats_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_stats_btn.setText("Statistics")
        self.menu_stats_btn.clicked.connect(self.menu_stats_btn_clicked)
        self.menu_frame_grid_layout.addWidget(self.menu_stats_btn, 4, 0, 1, 1)

        self.menu_settings_btn = QtWidgets.QPushButton(self.menu_frame)
        self.menu_settings_btn.setObjectName("menu_settings_btn")
        self.menu_settings_btn.setStyleSheet('''#menu_settings_btn{color: white;}''')
        self.menu_settings_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.menu_settings_btn.setText("Settings")
        self.menu_settings_btn.clicked.connect(self.menu_settings_btn_clicked)
        self.menu_frame_grid_layout.addWidget(self.menu_settings_btn, 5, 0, 1, 1)

        menu_frame_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.menu_frame_grid_layout.addItem(menu_frame_spacer, 6, 0, 1, 1)

        self.root_grid_layout.addWidget(self.menu_frame, 1, 0, 1, 1)
        self.menu_separator_line = QtWidgets.QFrame(self.central_widget)
        self.menu_separator_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.menu_separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.menu_separator_line.setObjectName("menu_separator_line")
        self.root_grid_layout.addWidget(self.menu_separator_line, 1, 1, 1, 1)

        self.resizer_horizontal_layout = QtWidgets.QHBoxLayout()

        resizer_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.resizer_horizontal_layout.addItem(resizer_spacer)

        self.resize_window_frame = QtWidgets.QFrame()
        self.resize_window_frame.setMinimumSize(20, 20)
        QtWidgets.QSizeGrip(self.resize_window_frame)
        self.resizer_horizontal_layout.addWidget(self.resize_window_frame)

        self.root_grid_layout.addLayout(self.resizer_horizontal_layout, 2, 0, 1, 4)

        self.setCentralWidget(self.central_widget)

        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.menu_study_btn_clicked()

        if maximize:
            self.show_maximized()

    def show_maximized(self):
        self.showMaximized()
        self.title_maximize_btn.setText('◱')
        self.title_maximize_btn.setFont(QFont('MS Shell Dlg 2', 10))

    def show_normal(self):
        self.showNormal()
        self.title_maximize_btn.setText('☐')
        self.title_maximize_btn.setFont(QFont('MS Shell Dlg 2', 10))

    def move_window(self, e):
        if self.isMaximized() and e.buttons() == Qt.LeftButton:
            self.show_normal()
            cursor_x = e.globalPos().x()
            cursor_y = e.globalPos().y()
            self.move(cursor_x - 500, cursor_y - 10)

        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.click_position)
            self.click_position = e.globalPos()

    def mouse_press_event(self, e):
        self.click_position = e.globalPos()

    def title_minimize_btn_clicked(self):
        self.showMinimized()

    def title_maximize_btn_clicked(self):
        if self.isMaximized():
            self.show_normal()
        else:
            self.show_maximized()

    def title_close_btn_clicked(self):
        self.close()

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
        self.font_size_selector.textChanged.connect(self.settings_save)
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
        self.target_retention_rate_selector.textChanged.connect(self.settings_save)
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
        self.create_backup_btn.clicked.connect(self.create_backup_btn_clicked)
        self.main_frame_grid_layout.addWidget(self.create_backup_btn, 4, 2, 1, 1)

        self.backup_list_widget = QtWidgets.QListWidget()
        self.backup_list_widget.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 2))
        backup_names = backups.get_backup_names()
        for name in backup_names:
            self.backup_list_widget.addItem(name)
        self.main_frame_grid_layout.addWidget(self.backup_list_widget, 5, 0, 2, 2)

        self.del_backup_btn = QtWidgets.QPushButton()
        self.del_backup_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.del_backup_btn.setText('Delete')
        self.del_backup_btn.clicked.connect(self.del_backup_btn_clicked)
        self.main_frame_grid_layout.addWidget(self.del_backup_btn, 5, 2, 1, 1)

        self.restore_backup_btn = QtWidgets.QPushButton()
        self.restore_backup_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.restore_backup_btn.setText('Restore')
        self.restore_backup_btn.clicked.connect(self.restore_backup_btn_clicked)
        self.main_frame_grid_layout.addWidget(self.restore_backup_btn, 6, 2, 1, 1)

        settings_lower_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(settings_lower_spacer, 7, 0, 1, 3)

    def restore_backup_btn_clicked(self):
        # Returns if nothing selected.
        if not self.backup_list_widget.selectedIndexes():
            return

        confirm_restore_backup_msg = QMessageBox()
        confirm_restore_backup_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        confirm_restore_backup_msg.setWindowTitle('Confirm Deletion')
        confirm_restore_backup_msg.setText(f'Are you sure you want to restore the app to the state when \'{self.backup_list_widget.currentItem().text()}\' was created?')
        confirm_restore_backup_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_restore_backup_msg.setDefaultButton(QMessageBox.Cancel)
        confirm_restore_backup_msg.exec_()
        if confirm_restore_backup_msg.clickedButton().text() == 'OK':
            backups.restore_backup(self.backup_list_widget.currentItem().text())

            self.clear_layout(self.root_grid_layout)
            self.setup_ui(check_for_update=False, maximize=False)
            self.menu_settings_btn_clicked()

    def del_backup_btn_clicked(self):
        # Returns if nothing selected.
        if not self.backup_list_widget.selectedIndexes():
            return

        confirm_del_backup_msg = QMessageBox()
        confirm_del_backup_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        confirm_del_backup_msg.setWindowTitle('Confirm Deletion')
        confirm_del_backup_msg.setText(f'Are you sure you want to delete \'{self.backup_list_widget.currentItem().text()}\'?')
        confirm_del_backup_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_del_backup_msg.setDefaultButton(QMessageBox.Cancel)
        confirm_del_backup_msg.exec_()
        if confirm_del_backup_msg.clickedButton().text() == 'OK':
            backups.del_backup(self.backup_list_widget.currentItem().text())

            self.menu_settings_btn_clicked()

    def create_backup_btn_clicked(self):
        saved_backup_name = ''

        while True:
            backup_name_input_dialog = QtWidgets.QInputDialog()
            backup_name_input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            backup_name_input_dialog.setWindowTitle('Create Backup')
            backup_name_input_dialog.setLabelText('Name of backup:')
            backup_name_input_dialog.setTextValue(saved_backup_name)
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

            # Checks for invalid character.
            invalid_char = False
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                if char in backup_name and ok:
                    no_name_msg = QMessageBox()
                    no_name_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                    no_name_msg.setWindowTitle('Invalid Character')
                    no_name_msg.setText('Due to the way Windows stores folders your backup name cannot contain: \ / : * ? " < > |')
                    no_name_msg.exec_()
                    invalid_char = True
                    break

            if invalid_char:
                continue

            if ok:
                not_duplicate = backups.create_back_up(backup_name)
                if not not_duplicate:
                    duplicate_backup = QMessageBox()
                    duplicate_backup.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                    duplicate_backup.setWindowTitle('Duplicate Name')
                    duplicate_backup.setText('A backup with that name already exists, please choose another.')
                    duplicate_backup.exec_()
                    saved_backup_name = backup_name
                    continue

            break

        self.menu_settings_btn_clicked()

    def settings_save(self):
        settings.set_font_size(self.font_size_selector.value())
        settings.set_target_retention_rate(self.target_retention_rate_selector.value())

        self.clear_layout(self.root_grid_layout)
        self.setup_ui(check_for_update=False, maximize=False)
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
            self.stats_retention_label.setText(f'Retention rate: {round(stats.get_retention_1440())}%')
        else:
            self.stats_retention_label.setText(f'Retention rate: N/A')
        self.stats_retention_label.setMinimumHeight(60)
        self.main_frame_grid_layout.addWidget(self.stats_retention_label, 1, 0, 1, 1)

        self.stats_retention_30_label = QtWidgets.QLabel()
        self.stats_retention_30_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        if type(stats.get_retention_1440()) == float:
            self.stats_retention_30_label.setText(f'Retention rate (previous 30 days): {round(stats.get_retention_1440(30))}%')
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
        self.search_line_edit.setObjectName('search_line_edit')
        self.search_line_edit.setStyleSheet('''
                                            #search_line_edit{
                                                background-color: rgba(255, 255, 255, 0.1);
                                                border: none;
                                                color: white;
                                            }
        ''')
        # Line edit needs font to be 3 bigger to match other items.
        self.search_line_edit.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 3))
        self.main_frame_grid_layout.addWidget(self.search_line_edit, 0, 0, 1, 1)

        self.search_btn = QtWidgets.QPushButton()
        self.search_btn.setObjectName('search_btn')
        self.search_btn.setStyleSheet('''
                                    #search_btn{
                                        color: white;
                                    }
        ''')
        self.search_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.search_btn.setText('Search')
        self.search_btn.clicked.connect(lambda: self.search_btn_clicked(self.search_line_edit.text()))
        self.main_frame_grid_layout.addWidget(self.search_btn, 0, 1, 1, 1)

        search_lower_left_spacer =QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(search_lower_left_spacer, 1, 0, 1, 1)

        search_lower_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_frame_grid_layout.addItem(search_lower_right_spacer, 1, 1, 1, 1)

    def search_btn_clicked(self, query):
        self.search_up_to = 0
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
            for deck in deck_names:
                self.search_deck_selector.addItem(deck)
            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_deck_selector.currentTextChanged.connect(self.search_save)
            self.main_frame_grid_layout.addWidget(self.search_deck_selector, 1, 0, 1, 2)

            self.search_qst_text = QtWidgets.QTextEdit()
            self.search_qst_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_qst_text.setPlainText(self.searched_cards[self.search_up_to]['Question'])
            self.search_qst_text.setTabChangesFocus(True)
            self.search_qst_text.textChanged.connect(self.search_save)
            self.main_frame_grid_layout.addWidget(self.search_qst_text, 2, 0, 1, 2)

            self.search_ans_text = QtWidgets.QTextEdit()
            self.search_ans_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_ans_text.setPlainText(self.searched_cards[self.search_up_to]['Answer'])
            self.search_ans_text.setTabChangesFocus(True)
            self.search_ans_text.textChanged.connect(self.search_save)
            self.main_frame_grid_layout.addWidget(self.search_ans_text, 3, 0, 1, 2)

            self.search_lower_frame = QtWidgets.QFrame()
            self.search_lower_frame_grid_layout = QtWidgets.QGridLayout(self.search_lower_frame)

            self.search_del_btn = QtWidgets.QPushButton()
            self.search_del_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_del_btn.setText('Delete')
            self.search_del_btn.clicked.connect(self.search_del_btn_clicked)
            self.search_lower_frame_grid_layout.addWidget(self.search_del_btn, 0, 0, 1, 1)

            search_lower_frame_center_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.search_lower_frame_grid_layout.addItem(search_lower_frame_center_spacer, 0, 1, 1, 1)

            self.search_previous_btn = QtWidgets.QPushButton()
            self.search_previous_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_previous_btn.setText('<')
            self.search_previous_btn.clicked.connect(self.search_previous_btn_clicked)
            self.search_lower_frame_grid_layout.addWidget(self.search_previous_btn, 0, 2, 1, 1)

            self.search_next_btn = QtWidgets.QPushButton()
            self.search_next_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.search_next_btn.setText('>')
            self.search_next_btn.clicked.connect(self.search_next_btn_clicked)
            self.search_lower_frame_grid_layout.addWidget(self.search_next_btn, 0, 3, 1, 1)

            self.adjust_search_nav_btns()

            self.main_frame_grid_layout.addWidget(self.search_lower_frame, 4, 0, 1, 2)

            self.search_next_btn.setFocus()
        else:
            query_not_found_msg = QMessageBox()
            query_not_found_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            query_not_found_msg.setWindowTitle('Query not found')
            query_not_found_msg.setText('There were no cards that contained that query.')
            query_not_found_msg.exec_()

    def search_save(self):
        search_qst = self.search_qst_text.toPlainText().strip()
        search_ans = self.search_ans_text.toPlainText().strip()

        if search_qst == '':
            enter_qst_msg = QMessageBox()
            enter_qst_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            enter_qst_msg.setWindowTitle('Enter Question')
            enter_qst_msg.setText('Please enter a question')
            enter_qst_msg.exec_()
            return

        if search_qst == self.searched_cards[self.search_up_to]['Question']:
            cards.write_card_edit_save(self.searched_cards[self.search_up_to], search_qst, search_ans)
        # Makes sure an edited question does not already exist.
        else:
            if cards.check_qst_exists(search_qst):
                duplicate_qst_msg = QMessageBox()
                duplicate_qst_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                duplicate_qst_msg.setWindowTitle('Duplicate Question')
                duplicate_qst_msg.setText('That question already exists, please enter a different question.')
                duplicate_qst_msg.exec_()
                return
            else:
                cards.write_card_edit_save(self.searched_cards[self.search_up_to], search_qst, search_ans)

        cards.change_deck(self.searched_cards[self.search_up_to]['Deck'], self.search_deck_selector.currentText(), search_qst)

        self.searched_cards[self.search_up_to]['Question'] = search_qst
        self.searched_cards[self.search_up_to]['Answer'] = search_ans
        self.searched_cards[self.search_up_to]['Deck'] = self.search_deck_selector.currentText()

    def search_del_btn_clicked(self):
        cards.del_card(self.searched_cards[self.search_up_to])
        self.searched_cards.pop(self.search_up_to)

        # Sets textChanged events to nothing (to avoid unnecessarily saving when changing cards).
        self.search_deck_selector.currentTextChanged.disconnect()
        self.search_qst_text.textChanged.disconnect()
        self.search_ans_text.textChanged.disconnect()

        if len(self.searched_cards) == 0:
            self.menu_search_btn_clicked()
        elif len(self.searched_cards) == self.search_up_to:
            self.search_up_to = self.search_up_to - 1

            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setPlainText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setPlainText(self.searched_cards[self.search_up_to]['Answer'])
        else:
            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setPlainText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setPlainText(self.searched_cards[self.search_up_to]['Answer'])

        self.search_deck_selector.currentTextChanged.connect(self.search_save)
        self.search_qst_text.textChanged.connect(self.search_save)
        self.search_ans_text.textChanged.connect(self.search_save)

        self.adjust_search_nav_btns()

        self.menu_study_btn.setText(f'Study {cards.get_num_to_study()}')

    def search_previous_btn_clicked(self):
        if self.search_up_to > 0:
            self.search_up_to = self.search_up_to - 1

            # Sets textChanged events to nothing (to avoid unnecessarily saving when changing cards).
            self.search_deck_selector.currentTextChanged.disconnect()
            self.search_qst_text.textChanged.disconnect()
            self.search_ans_text.textChanged.disconnect()

            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setPlainText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setPlainText(self.searched_cards[self.search_up_to]['Answer'])

            self.search_deck_selector.currentTextChanged.connect(self.search_save)
            self.search_qst_text.textChanged.connect(self.search_save)
            self.search_ans_text.textChanged.connect(self.search_save)

            self.adjust_search_nav_btns()

    def search_next_btn_clicked(self):
        if self.search_up_to < len(self.searched_cards) - 1:

            # Sets textChanged events to nothing (to avoid unnecessarily saving when changing cards).
            self.search_deck_selector.currentTextChanged.disconnect()
            self.search_qst_text.textChanged.disconnect()
            self.search_ans_text.textChanged.disconnect()

            self.search_up_to = self.search_up_to + 1

            self.search_deck_selector.setCurrentText(self.searched_cards[self.search_up_to]['Deck'])
            self.search_qst_text.setPlainText(self.searched_cards[self.search_up_to]['Question'])
            self.search_ans_text.setPlainText(self.searched_cards[self.search_up_to]['Answer'])

            self.search_deck_selector.currentTextChanged.connect(self.search_save)
            self.search_qst_text.textChanged.connect(self.search_save)
            self.search_ans_text.textChanged.connect(self.search_save)

            self.adjust_search_nav_btns()

    def adjust_search_nav_btns(self):
        if self.search_up_to == 0:
            self.search_previous_btn.setEnabled(False)
            self.setFocus()
        else:
            self.search_previous_btn.setEnabled(True)

        if (self.search_up_to + 1) == len(self.searched_cards):
            self.search_next_btn.setEnabled(False)
            self.setFocus()
        else:
            self.search_next_btn.setEnabled(True)

    def menu_study_btn_clicked(self, deck=False):
        self.clear_layout(self.main_frame_grid_layout)

        self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")

        self.current_card = cards.get_card(deck)

        if self.current_card:
            self.study_qst_text = QtWidgets.QTextEdit(self.main_frame)
            self.study_qst_text.setTabChangesFocus(True)
            self.study_qst_text.setObjectName("study_qst_text")
            self.study_qst_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_qst_text.setPlainText(self.current_card['Question'])
            self.study_qst_text.setReadOnly(True)
            self.study_qst_text.setStyleSheet('''
                                            #study_qst_text{
                                                background-color: transparent;
                                                border: none;
                                                color: white;
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
                                                    color: white;
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
            self.study_ans_btn.setStyleSheet('''#study_ans_btn{color: white;}''')
            self.study_ans_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_ans_btn.setText("Answer")
            self.study_ans_btn.setFocus()
            self.study_ans_btn.clicked.connect(self.study_ans_btn_clicked)
            self.study_lower_btns_frame_grid_layout.addWidget(self.study_ans_btn, 0, 1, 1, 1)

            study_lower_btns_frame_right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_right_spacer, 0, 2, 1, 1)

            study_lower_btns_frame_left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_left_spacer, 0, 0, 1, 1)

            self.main_frame_grid_layout.addWidget(self.study_lower_btns_frame, 2, 0, 1, 1)

            self.study_ans_btn.setFocus()
        else:
            self.study_completed_label = QtWidgets.QLabel()
            self.study_completed_label.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.study_completed_label.setText('Study completed.')
            self.study_completed_label.setObjectName('study_completed_label')
            self.study_completed_label.setStyleSheet('''#study_completed_label{color: white;}''')
            self.study_completed_label.setMinimumHeight(60)
            self.main_frame_grid_layout.addWidget(self.study_completed_label, 0, 0, 1, 1)

            completed_lower_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.main_frame_grid_layout.addItem(completed_lower_spacer, 1, 0, 1, 1)

    def study_ans_btn_clicked(self):
        self.study_ans_text.setPlainText(self.current_card["Answer"])

        # Done to change focus off of self.study_ans_btn before it is cleared.
        self.menu_study_btn.setFocus()

        self.clear_layout(self.study_lower_btns_frame_grid_layout)

        study_lower_btns_frame_left_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_left_spacer, 0, 0, 1, 1)

        self.study_correct_btn = QtWidgets.QPushButton()
        self.study_correct_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.study_correct_btn.setText('Correct')
        self.study_correct_btn.setObjectName('study_correct_btn')
        self.study_correct_btn.setStyleSheet('''#study_correct_btn{color: white;}''')
        self.study_correct_btn.clicked.connect(self.study_correct_btn_clicked)
        self.study_lower_btns_frame_grid_layout.addWidget(self.study_correct_btn, 0, 1, 1, 1)
        self.study_correct_btn.setFocus()

        study_lower_btns_frame_center_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.study_lower_btns_frame_grid_layout.addItem(study_lower_btns_frame_center_spacer, 0, 2, 1, 1)

        self.study_again_btn = QtWidgets.QPushButton()
        self.study_again_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.study_again_btn.setText('Again')
        self.study_again_btn.setObjectName('study_again_btn')
        self.study_again_btn.setStyleSheet('''#study_again_btn{color: white;}''')
        self.study_again_btn.clicked.connect(self.study_again_btn_clicked)
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
            self.add_cards_deck_selector.setMinimumHeight(60)
            self.add_cards_deck_selector.setObjectName('add_cards_deck_selector')
            self.add_cards_deck_selector.setStyleSheet('''
                                                        #add_cards_deck_selector{
                                                            background-color: rgba(255, 255, 255, 0.1);
                                                            border: none;
                                                            color: white;
                                                        }
                                                        QAbstractItemView{
                                                            background-color: #447777;
                                                            color: white;
                                                        }
            ''')
            deck_lines = decks.get_deck_lines()
            for deck in deck_lines:
                self.add_cards_deck_selector.addItem(deck)
            self.add_cards_deck_selector.setCurrentIndex(-1)
            self.add_cards_upper_frame_grid_layout.addWidget(self.add_cards_deck_selector, 0, 0, 1, 1)

            self.add_cards_qst_text = QtWidgets.QTextEdit()
            self.add_cards_qst_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.add_cards_qst_text.setObjectName('add_cards_qst_text')
            self.add_cards_qst_text.setStyleSheet('''
                                                    #add_cards_qst_text{
                                                        margin-right: 10px;
                                                        margin-left: 10px;
                                                        margin-bottom: 10px;
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                        border: none;
                                                        color: white;
                                                    }
                                                    QScrollBar{
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                    }
            ''')
            self.add_cards_qst_text.setTabChangesFocus(True)
            self.main_frame_grid_layout.addWidget(self.add_cards_qst_text, 1, 0, 1, 1)

            self.add_cards_ans_text = QtWidgets.QTextEdit()
            self.add_cards_ans_text.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.add_cards_ans_text.setObjectName('add_cards_ans_text')
            self.add_cards_ans_text.setStyleSheet('''
                                                    #add_cards_ans_text{
                                                        margin-right: 10px;
                                                        margin-left: 10px;
                                                        background-color: rgba(255, 255, 255, 0.1);
                                                        border: none;
                                                        color: white;
                                                    }
                                                    QScrollBar{
                                                       background-color: rgba(255, 255, 255, 0.1);
                                                    }
                        ''')
            self.add_cards_ans_text.setTabChangesFocus(True)
            self.main_frame_grid_layout.addWidget(self.add_cards_ans_text, 2, 0, 1, 1)

            self.add_cards_lower_frame = QtWidgets.QFrame()
            self.add_cards_lower_frame_grid_layout = QtWidgets.QGridLayout(self.add_cards_lower_frame)
            self.main_frame_grid_layout.addWidget(self.add_cards_lower_frame, 3, 0, 1, 1)

            self.add_card_btn = QtWidgets.QPushButton()
            self.add_card_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            self.add_card_btn.setText('Add Card')
            self.add_card_btn.setObjectName('add_card_btn')
            self.add_card_btn.setStyleSheet('''#add_card_btn{color: white;}''')
            self.add_card_btn.clicked.connect(self.add_card_btn_clicked)
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
        add_qst = self.add_cards_qst_text.toPlainText().strip()
        add_ans = self.add_cards_ans_text.toPlainText().strip()

        if self.add_cards_deck_selector.currentIndex() == -1:
            select_deck_msg = QMessageBox()
            select_deck_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            select_deck_msg.setWindowTitle('Select Deck')
            select_deck_msg.setText('Please select a deck')
            select_deck_msg.exec_()
            self.add_cards_deck_selector.setFocus()
            return

        if add_qst == '':
            enter_qst_msg = QMessageBox()
            enter_qst_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            enter_qst_msg.setWindowTitle('Enter Question')
            enter_qst_msg.setText('Please enter a question')
            enter_qst_msg.exec_()
            return

        if not cards.add_card(self.add_cards_deck_selector.currentText(), add_qst, add_ans):
            duplicate_qst_msg = QMessageBox()
            duplicate_qst_msg.setWindowTitle('Duplicate')
            duplicate_qst_msg.setText('A card with that question already exists, card not added.')
            duplicate_qst_msg.exec_()
        else:
            self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")
            self.add_cards_qst_text.clear()
            self.add_cards_ans_text.clear()
            self.add_cards_qst_text.setFocus()

    def menu_decks_btn_clicked(self):
        self.clear_layout(self.main_frame_grid_layout)

        self.add_deck_line_edit = QtWidgets.QLineEdit()
        self.add_deck_line_edit.setObjectName('add_deck_line_edit')
        self.add_deck_line_edit.setStyleSheet('''
                                                #add_deck_line_edit{
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                    border: none;
                                                    color: white;
                                                }
        ''')
        # Line edit needs font to be 3 bigger to match other items.
        self.add_deck_line_edit.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 3))
        self.main_frame_grid_layout.addWidget(self.add_deck_line_edit, 0, 0, 1, 1)

        self.add_deck_btn = QtWidgets.QPushButton()
        self.add_deck_btn.setObjectName('add_deck_btn')
        self.add_deck_btn.setStyleSheet('''
                                        #add_deck_btn{
                                            color: white;
                                        }
        ''')
        self.add_deck_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.add_deck_btn.setText('Add Deck')
        self.add_deck_btn.clicked.connect(self.add_deck_btn_clicked)
        self.main_frame_grid_layout.addWidget(self.add_deck_btn, 0, 1, 1, 1)

        self.deck_list_widget = QtWidgets.QListWidget()
        self.deck_list_widget.setObjectName('deck_list_widget')
        self.deck_list_widget.setStyleSheet('''
                                            #deck_list_widget{
                                                background-color: rgba(255, 255, 255, 0.1);
                                                border: none;
                                                color: white;
                                            }
        ''')
        deck_lines = decks.get_deck_lines()
        for deck in deck_lines:
            self.deck_list_widget.addItem(deck)
        self.deck_list_widget.setFont(QFont('MS Shell Dlg 2', settings.get_font_size() + 2))
        self.main_frame_grid_layout.addWidget(self.deck_list_widget, 1, 0, 3, 1)

        self.del_deck_btn = QtWidgets.QPushButton()
        self.del_deck_btn.setObjectName('del_deck_btn')
        self.del_deck_btn.setStyleSheet('''
                                        #del_deck_btn{
                                            color: white;
                                        }
        ''')
        self.del_deck_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.del_deck_btn.setText('Delete')
        self.del_deck_btn.clicked.connect(self.del_deck_btn_clicked)
        self.main_frame_grid_layout.addWidget(self.del_deck_btn, 1, 1, 1, 1)

        self.rename_deck_btn = QtWidgets.QPushButton()
        self.rename_deck_btn.setObjectName('rename_deck_btn')
        self.rename_deck_btn.setStyleSheet('''
                                                #rename_deck_btn{
                                                    color: white;
                                                }
                ''')
        self.rename_deck_btn.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        self.rename_deck_btn.setText('Rename')
        self.rename_deck_btn.clicked.connect(self.rename_deck_btn_clicked)
        self.main_frame_grid_layout.addWidget(self.rename_deck_btn, 2, 1, 1, 1)

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

        # Will only work if focus set to self before line edit.
        self.setFocus()
        self.add_deck_line_edit.setFocus()

    def del_deck_btn_clicked(self):
        # Returns if nothing is selected.
        if not self.deck_list_widget.selectedIndexes():
            return

        selected_deck_del = self.deck_list_widget.currentItem().text().strip()

        confirm_del_deck_msg = QMessageBox()
        confirm_del_deck_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
        confirm_del_deck_msg.setWindowTitle('Confirm')
        confirm_del_deck_msg.setText(f'Are you sure you want to delete the selected deck and all cards in the deck?')
        confirm_del_deck_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_del_deck_msg.setDefaultButton(QMessageBox.Cancel)
        confirm_del_deck_msg.exec_()
        if confirm_del_deck_msg.clickedButton().text() == 'OK':
            decks.del_deck(selected_deck_del)
            self.menu_study_btn.setText(f"Study {cards.get_num_to_study()}")
            self.menu_decks_btn_clicked()

    def rename_deck_btn_clicked(self):
        # Returns if nothing selected.
        if not self.deck_list_widget.selectedIndexes():
            return

        selected_deck_rename = self.deck_list_widget.currentItem().text().strip()

        saved_deck_name = ''

        while True:
            deck_name_input_dialog = QtWidgets.QInputDialog()
            deck_name_input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            deck_name_input_dialog.setWindowTitle('Rename Deck')
            deck_name_input_dialog.setLabelText('Enter the new name for deck:')
            deck_name_input_dialog.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
            deck_name_input_dialog.setTextValue(saved_deck_name)
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
                not_duplicate = decks.rename_deck(selected_deck_rename, new_deck_name)
                if not not_duplicate:
                    duplicate_deck_msg = QMessageBox()
                    duplicate_deck_msg.setFont(QFont('MS Shell Dlg 2', settings.get_font_size()))
                    duplicate_deck_msg.setWindowTitle('Duplicate')
                    duplicate_deck_msg.setText('Deck already exists.')
                    duplicate_deck_msg.exec_()
                    saved_deck_name = new_deck_name
                    continue

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


# If MemoryGain.exe running True, else False.
def app_already_running():
    command_output = ''
    pipe = Popen('powershell -c "get-process | select-object path"', stdout=PIPE, stderr=PIPE)
    for line in pipe.stdout.readlines():
        command_output += line.decode()

    if 'C:\\Program Files\\MemoryGain\\MemoryGain.exe' in command_output:
        return True

    return False


if __name__ == "__main__":
    # Does not allow multiple instances.
    if app_already_running():
        sys.exit()

    decks.decks_on_device()
    cards.cards_on_device()
    stats.stats_on_device()
    settings.settings_on_device()
    backups.backups_on_device()
    backups.create_back_up()
    backups.delete_old_backups()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
