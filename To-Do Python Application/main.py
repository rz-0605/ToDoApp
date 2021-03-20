from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import date, datetime
import datetime as datetime2
from CustomWidgets import DisplayEventSection, EventDescriptionViewer, AddEventDialog, DeleteEventDialog, \
    EditEventDialog, TodoEvent, WeekViewEventSection, CustomStackedLayout, TodoCalendar, MinuteTimer
from CustomWidgets import toDoEvents
from win10toast import ToastNotifier
import pickle
import sys
import time

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
stylesheet = """
        QWidget{
            background-color: white;
        }

        QWidget#sideMenuBackground{
            background-color: #f7f7f7;
        }

        QVBoxLayout#sideMenuLayout{
            background-color: grey;
        }


        QPushButton#sideMenuButton{
            text-align: left;
            border: none;
            background-color: #f7f7f7;
            max-width: 10em;
            font: 16px; 
            padding: 6px;
        }

        QPushButton#sideMenuButton:hover{
            font: 18px;
        }

        QLabel#today_label{
            font: 25px;
            max-width: 70px;
        }

        QLabel#todays_date_label{
            font: 11px;
            color: grey;
        }

        QPushButton#addTodoEventButton{
            border: none;
            max-width: 130px;
        }
        
        QPushButton#DeleteButton{
            background-color: white;
        }
        
        QLabel#doubleTitleLabel {
            color: red;
        }
        
        QLabel#next_week_label {
            font: 25px;
            text-align: left;
            margin-bottom: 5px;
            border-bottom: 2px solid grey;
        }
        
        QLabel#day_label {
            margin-bottom: 5px;
            border-bottom: 1px solid black;
            text-align: left;
        }
        
        QLabel#click_label {
            color: grey;
        }
        
        QLabel#calendar_label {
            font: 25px;
            text-align: left;
            margin-bottom: 5px;
            border-bottom: 2px solid grey;
        }
        
        QCalendarWidget QWidget {
            background-color: grey;
        }
        
        QCalendarWidget QAbstractItemView:enabled{
            background-color: white;
            color: black;
        }
        
        QLabel#calendar_click_dialog_label{
            margin-bottom: 5px;
            border-bottom: 1px solid black;
            text-align: left;
            font: 25px;
        }

    """


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do Application")
        self.setGeometry(200, 200, 1100, 700)
        self.setFixedSize(1100, 700)
        # self.loadEventData()
        self.initUI()

    # def loadEventData(self):
    #     # loads all data into one dict, toDoEvents
    #     infile = open('ToDoEvents', 'rb')
    #     tempToDoEvents = pickle.load(infile)
    #     global toDoEvents
    #     toDoEvents = tempToDoEvents
    #     infile.close()

    def initUI(self):
        backgroundWidget = QtWidgets.QWidget()
        backgroundWidget.setObjectName("sideMenuBackground")
        backgroundWidget.setFixedWidth(150)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(backgroundWidget)
        sideMenuLayout = QtWidgets.QVBoxLayout()
        sideMenuLayout.setObjectName("sideMenuLayout")
        self.taskLayout = CustomStackedLayout()

        backgroundWidget.setLayout(sideMenuLayout)
        layout.addLayout(self.taskLayout)

        self.setSideMenu(sideMenuLayout)
        sideMenuLayout.addStretch(0)

        self.setMainLayout(self.taskLayout)

        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(layout)

        self.setCentralWidget(mainWidget)

    def setSideMenu(self, layout):
        self.todayButton = QtWidgets.QPushButton(" Today")
        self.nextWeekButton = QtWidgets.QPushButton("Next 7 Days")
        self.calendarButton = QtWidgets.QPushButton("Calendar")

        sideMenuButtons = [self.todayButton, self.nextWeekButton, self.calendarButton]
        for button in sideMenuButtons:
            button.setObjectName("sideMenuButton")
            layout.addWidget(button)

        sideMenuButtons[0].setIcon(QtGui.QIcon("today icon.png"))
        sideMenuButtons[1].setIcon(QtGui.QIcon("week icon.png"))
        sideMenuButtons[2].setIcon(QtGui.QIcon("calendar icon.png"))

        sideMenuButtons[0].pressed.connect(self.todayButtonPress)
        sideMenuButtons[1].pressed.connect(self.nextWeekButtonPress)
        sideMenuButtons[2].pressed.connect(self.calendarButtonPress)

    def setMainLayout(self, layout):
        today = self.todayWidget()
        self.next_week_widget = self.nextWeekWidget()
        calendar_widget = self.calendarWidget()

        layout.addWidget(today)
        layout.addWidget(self.next_week_widget)
        layout.addWidget(calendar_widget)

    def todayWidget(self):
        widget = QtWidgets.QWidget(self)
        self.todayMainLayout = QVBoxLayout(widget)
        self.todayMainLayout.setAlignment(Qt.AlignTop)

        today_label_widget = QtWidgets.QWidget()
        topLayout = QtWidgets.QHBoxLayout()

        eventLayoutWidget = QtWidgets.QWidget()
        self.eventLayout = QtWidgets.QVBoxLayout(self)
        eventLayoutWidget.setLayout(self.eventLayout)

        self.todayMainLayout.addWidget(today_label_widget)
        today_label_widget.setLayout(topLayout)
        self.todayMainLayout.addWidget(eventLayoutWidget)

        month = date.today().month
        day = date.today().day
        today = f"{months[month - 1]} {day}"
        self.todays_date = QtWidgets.QLabel(today)
        self.todays_date.setObjectName("todays_date_label")
        self.today_label = QtWidgets.QLabel("Today")
        self.today_label.setObjectName("today_label")

        self.addTodoEventButton = QtWidgets.QPushButton()
        self.addTodoEventButton.setObjectName("addTodoEventButton")
        self.addTodoEventButton.setIcon(QtGui.QIcon("add event button.png"))
        self.addTodoEventButton.setToolTip("Add To Do Event")
        self.addTodoEventButton.pressed.connect(self.addTodoEvent)

        topLayout.addWidget(self.today_label)
        topLayout.addWidget(self.todays_date)
        topLayout.addWidget(self.addTodoEventButton)
        self.updateTodayWidget()
        return widget

    def updateTodayWidget(self):
        for i in reversed(range(self.eventLayout.count())):
            self.eventLayout.itemAt(i).widget().setParent(None)

        global toDoEvents
        for event in toDoEvents.values():
            display_new_event = DisplayEventSection(event)
            self.eventLayout.addWidget(display_new_event)

    def nextWeekWidget(self):
        widget = QtWidgets.QWidget(self)
        self.nextWeekLayout = QVBoxLayout(self)
        widget.setLayout(self.nextWeekLayout)
        title_widget = QtWidgets.QWidget(self)
        self.nextWeekLayout.addWidget(title_widget)
        title_layout = QtWidgets.QHBoxLayout(self)
        title_widget.setLayout(title_layout)
        next_week_label = QtWidgets.QLabel("Next Week")
        next_week_label.setObjectName("next_week_label")
        title_layout.addWidget(next_week_label)

        week_view_widget = QtWidgets.QWidget(self)
        self.week_view_layout = QtWidgets.QHBoxLayout(self)
        week_view_widget.setLayout(self.week_view_layout)
        self.nextWeekLayout.addWidget(week_view_widget)

        return widget

    def updateNextWeekWidget(self):
        for index in reversed(range(self.week_view_layout.count())):
            self.week_view_layout.itemAt(index).widget().setParent(None)

        for i in range(7):
            day_widget = QtWidgets.QWidget(self)
            day_layout = QtWidgets.QVBoxLayout(self)
            day_widget.setLayout(day_layout)
            self.week_view_layout.addWidget(day_widget)

            day_title_widget = QtWidgets.QWidget(self)
            self.week_day_title_layout = QtWidgets.QVBoxLayout(self)
            day_title_widget.setLayout(self.week_day_title_layout)

            for index in reversed(range(self.week_day_title_layout.count())):
                self.week_day_title_layout.itemAt(index).widget().setParent(None)

            event_widget = QtWidgets.QWidget(self)
            self.week_event_layout = QtWidgets.QVBoxLayout(self)
            event_widget.setLayout(self.week_event_layout)

            day_layout.addWidget(day_title_widget)
            day_layout.addWidget(event_widget)

            day_name = datetime2.date.today() + datetime2.timedelta(days=i)
            self.day_name_display = day_name.strftime("%A")
            self.day_date_display = day_name.strftime("%m/%d")
            day_label = QtWidgets.QLabel(f"{self.day_name_display} {self.day_date_display}")
            day_label.setMinimumWidth(100)
            day_label.setMinimumWidth(100)
            day_label.setObjectName("day_label")
            self.week_day_title_layout.addWidget(day_label)

            for index in reversed(range(self.week_event_layout.count())):
                self.week_event_layout.itemAt(index).widget().setParent(None)

            global toDoEvents
            for event in toDoEvents.values():
                if event.due_time.strftime("%m/%d") == self.day_date_display:
                    week_view_event_section = WeekViewEventSection(event)
                    self.week_event_layout.addWidget(week_view_event_section)

            day_layout.addStretch(0)

    def calendarWidget(self):
        widget = QtWidgets.QWidget(self)
        layout = QVBoxLayout(widget)

        calendar_label = QtWidgets.QLabel(self)
        calendar_label.setText("Calendar")
        calendar_label.setObjectName("calendar_label")
        layout.addWidget(calendar_label)
        global toDoEvents
        mainCalendar = TodoCalendar(toDoEvents)
        layout.addWidget(mainCalendar)

        return widget

    def todayButtonPress(self):
        self.taskLayout.setCurrentIndex(0)
        self.updateTodayWidget()

    def nextWeekButtonPress(self):
        self.taskLayout.setCurrentIndex(1)
        self.updateNextWeekWidget()

    def calendarButtonPress(self):
        self.taskLayout.setCurrentIndex(2)

    def addTodoEvent(self):
        self.addEventDialog = AddEventDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.addEventDialog.exec_()
        self.updateTodayWidget()

    def closeEvent(self, event):
        # Loads all data from toDoEvents dict back into file
        outfile = open("ToDoEvents", 'wb')
        global toDoEvents
        pickle.dump(toDoEvents, outfile)
        outfile.close()
        event.accept()

def minuteEvent():
    for event in toDoEvents.values():
        if event.remind_time.strftime("%m/%d/%Y, %I:%M") == datetime.now().strftime("%m/%d/%Y, %I:%M"):
            toaster = ToastNotifier()
            toaster.show_toast(event.title, event.description, threaded=True, icon_path=None, duration=8)
            while toaster.notification_active():
                time.sleep(0.1)
def main():
    app = QtWidgets.QApplication(sys.argv)
    minuteTimer = MinuteTimer()
    minuteTimer.timeout.connect(minuteEvent)
    minuteTimer.start()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
