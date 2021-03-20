from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import date
import pickle




class DisplayEventSection(QtWidgets.QPushButton):

    def __init__(self, toDoEvent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toDoEvent = toDoEvent
        self.initUI()

    def initUI(self):
        self.setMinimumHeight(50)
        displayEventLayout = QtWidgets.QHBoxLayout(self)
        remindWidget = QtWidgets.QWidget(self)
        dueWidget = QtWidgets.QWidget(self)
        remindLayout = QtWidgets.QVBoxLayout()
        remindWidget.setLayout(remindLayout)
        dueLayout = QtWidgets.QVBoxLayout()
        dueWidget.setLayout(dueLayout)

        titleLabel = QtWidgets.QLabel(self)
        titleLabel.setText(self.toDoEvent.title)

        remindLabel = QtWidgets.QLabel(self)
        remindLabel.setText("Remind on:")
        remind_date_label = QtWidgets.QLabel(self)
        remind_date_label.setText(f"{self.toDoEvent.due_time.strftime('%m/%d/%Y, %I:%M')}")
        remindLayout.addWidget(remindLabel)
        remindLayout.addWidget(remind_date_label)

        dueLabel = QtWidgets.QLabel(self)
        dueLabel.setText("Due on:")
        due_date_label = QtWidgets.QLabel(self)
        due_date_label.setText(f"{self.toDoEvent.remind_time.strftime('%m/%d/%Y, %I:%M')}")
        dueLayout.addWidget(dueLabel)
        dueLayout.addWidget(due_date_label)

        deleteButton = QtWidgets.QPushButton(self)
        deleteButton.setObjectName("DeleteButton")
        deleteButton.setIcon(QtGui.QIcon("delete icon.png"))
        deleteButton.clicked.connect(self.handleDeleteButton)

        editButton = QtWidgets.QPushButton(self)
        editButton.setIcon(QtGui.QIcon("edit icon.png"))
        editButton.clicked.connect(self.handleEditButton)

        displayEventLayout.setContentsMargins(1, 5, 5, 1)
        displayEventLayout.addWidget(titleLabel)
        displayEventLayout.addWidget(remindWidget)
        displayEventLayout.addWidget(dueWidget)
        displayEventLayout.addWidget(deleteButton)
        displayEventLayout.addWidget(editButton)
        self.clicked.connect(self.handleSectionClick)

    def handleSectionClick(self):
        self.eventViewer = EventDescriptionViewer(self.toDoEvent, None,
                                                  QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.eventViewer.exec_()

    def handleDeleteButton(self):
        deleteDialog = DeleteEventDialog(self.toDoEvent, None,
                                         QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        deleteDialog.exec_()
        try:
            self.nativeParentWidget().updateTodayWidget()
        except Exception:
            self.nativeParentWidget().handleEventUpdate()

    def handleEditButton(self):
        editEventDialog = EditEventDialog(self.toDoEvent, None,
                                          QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        editEventDialog.exec_()
        try:
            self.nativeParentWidget().updateTodayWidget()
        except Exception:
            self.nativeParentWidget().handleEventUpdate()


class EventDescriptionViewer(QtWidgets.QDialog):

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

        self.setWindowTitle(self.event.title)
        self.setGeometry(250, 250, 400, 200)
        self.setMaximumWidth(400)
        mainLayout = QtWidgets.QVBoxLayout(self)

        Btn = QDialogButtonBox.Ok
        okBtn = QDialogButtonBox(Btn)
        okBtn.accepted.connect(self.accept)

        title_label = QtWidgets.QLabel(self)
        title_label.setText("Title: ")
        display_title = QtWidgets.QLabel(self)
        display_title.setText(self.event.title)
        display_title.setWordWrap(True)

        remind_label = QtWidgets.QLabel(self)
        remind_label.setText("Remind on: ")
        display_remind = QtWidgets.QLabel(self)
        display_remind.setText(self.event.remind_time.strftime("%m/%d/%Y, %H:%M:%S"))

        due_label = QtWidgets.QLabel(self)
        due_label.setText("Due on: ")
        display_due = QtWidgets.QLabel(self)
        display_due.setText(self.event.due_time.strftime("%m/%d/%Y, %H:%M:%S"))

        description_label = QtWidgets.QLabel(self)
        description_label.setText("Description: ")
        display_description = QtWidgets.QLabel(self)
        display_description.setMaximumWidth(400)
        display_description.setWordWrap(True)
        display_description.setMargin(5)
        display_description.setText(self.event.description)

        mainLayout.addWidget(title_label)
        mainLayout.addWidget(display_title)
        mainLayout.addWidget(remind_label)
        mainLayout.addWidget(display_remind)
        mainLayout.addWidget(due_label)
        mainLayout.addWidget(display_due)
        mainLayout.addWidget(description_label)
        mainLayout.addWidget(display_description)
        mainLayout.addWidget(okBtn)
        mainLayout.addStretch(0)
        self.setLayout(mainLayout)


class AddEventDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Add Event")
        self.setGeometry(250, 250, 400, 200)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addStretch(0)
        self.setLayout(self.mainLayout)

        # ---------------------------------------------------------------
        # Setting up labels and edit
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText("Event Title: ")
        self.titleLine = QtWidgets.QLineEdit(self)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.titleLine)

        self.dueDateLabel = QtWidgets.QLabel(self)
        self.dueDateLabel.setText("Due Date: ")
        self.dueDateEdit = QtWidgets.QDateTimeEdit(self)
        self.dueDateEdit.setCalendarPopup(True)
        self.dueDateEdit.setMinimumDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))

        self.remindDateLabel = QtWidgets.QLabel(self)
        self.remindDateLabel.setText("Remind Date: ")
        self.remindDateEdit = QtWidgets.QDateTimeEdit(self)
        self.remindDateEdit.setCalendarPopup(True)
        self.remindDateEdit.setMinimumDate(QtCore.QDate(date.today().year, date.today().month, date.today().day))

        self.descriptionLabel = QtWidgets.QLabel(self)
        self.descriptionLabel.setText("Description: ")
        self.descriptionEdit = QtWidgets.QPlainTextEdit(self)

        # -----------------------------------------------------------------------------
        # adding to main layout
        self.mainLayout.addWidget(self.dueDateLabel)
        self.mainLayout.addWidget(self.dueDateEdit)

        self.mainLayout.addWidget(self.remindDateLabel)
        self.mainLayout.addWidget(self.remindDateEdit)

        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.descriptionEdit)

        self.mainLayout.addWidget(self.buttonBox)

    def accept(self):
        #  checking if duplicate titles exist
        global toDoEvents
        if self.titleLine.text() in toDoEvents:
            doubleTitleLabel = QtWidgets.QLabel(self)
            doubleTitleLabel.setObjectName("doubleTitleLabel")
            doubleTitleLabel.setText(f"Error: There is already an event with name {self.titleLine.text()}.")
            self.mainLayout.addWidget(doubleTitleLabel)

        else:
            eventTitle = self.titleLine.text()
            dueDate = self.dueDateEdit.dateTime().toPyDateTime()
            remindDate = self.remindDateEdit.dateTime().toPyDateTime()
            description = self.descriptionEdit.toPlainText()
            newEvent = TodoEvent(eventTitle, dueDate, remindDate, description)
            super().accept()

    def reject(self):
        super().reject()


class DeleteEventDialog(QtWidgets.QDialog):

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event = event
        self.setWindowTitle("Delete Event")
        self.setGeometry(250, 250, 400, 200)
        self.setFixedSize(400, 200)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addStretch(0)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dialog_buttons = QDialogButtonBox(QBtn)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)

        deleteQuestion = QtWidgets.QLabel(self)
        deleteQuestion.setMinimumWidth(400)
        deleteQuestion.setAlignment(QtCore.Qt.AlignCenter)
        deleteQuestion.setText(f"Are you sure you want to delete \n\t{self.event.title}?")

        mainLayout.addWidget(dialog_buttons)

    def accept(self):
        global toDoEvents
        del toDoEvents[self.event.title]
        super().accept()


class EditEventDialog(QtWidgets.QDialog):

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        self.setWindowTitle("Edit Event")
        self.setGeometry(250, 250, 400, 200)
        self.initUI()

    def initUI(self):
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addStretch(0)
        self.setLayout(self.mainLayout)

        # ---------------------------------------------------------------
        # Setting up labels and edit
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText("Event Title: ")
        self.titleLine = QtWidgets.QLineEdit(self)
        self.titleLine.setText(self.event.title)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.titleLine)

        self.dueDateLabel = QtWidgets.QLabel(self)
        self.dueDateLabel.setText("Due Date: ")
        self.dueDateEdit = QtWidgets.QDateTimeEdit(self)
        self.dueDateEdit.setCalendarPopup(True)
        self.dueDateEdit.setDateTime(self.event.due_time)

        self.remindDateLabel = QtWidgets.QLabel(self)
        self.remindDateLabel.setText("Remind Date: ")
        self.remindDateEdit = QtWidgets.QDateTimeEdit(self)
        self.remindDateEdit.setCalendarPopup(True)
        self.remindDateEdit.setDateTime(self.event.remind_time)

        self.descriptionLabel = QtWidgets.QLabel(self)
        self.descriptionLabel.setText("Description: ")
        self.descriptionEdit = QtWidgets.QPlainTextEdit(self)
        self.descriptionEdit.setPlainText(self.event.description)

        # -----------------------------------------------------------------------------
        # adding to main layout
        self.mainLayout.addWidget(self.dueDateLabel)
        self.mainLayout.addWidget(self.dueDateEdit)

        self.mainLayout.addWidget(self.remindDateLabel)
        self.mainLayout.addWidget(self.remindDateEdit)

        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.descriptionEdit)

        self.mainLayout.addWidget(self.buttonBox)

    def accept(self):
        changedTitle = self.titleLine.text()
        changed_due_time = self.dueDateEdit.dateTime().toPyDateTime()
        changed_remind_time = self.remindDateEdit.dateTime().toPyDateTime()
        changed_description = self.descriptionEdit.toPlainText()
        global toDoEvents
        del toDoEvents[self.event.title]
        newEvent = TodoEvent(changedTitle, changed_due_time, changed_remind_time, changed_description)
        super().accept()


class WeekViewEventSection(QtWidgets.QPushButton):

    def __init__(self, toDoEvent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toDoEvent = toDoEvent
        self.initUI()

    def initUI(self):
        self.setMinimumSize(100, 50)
        main_layout = QtWidgets.QVBoxLayout(self)
        title_label = QtWidgets.QLabel(self)
        title_label.setText(self.toDoEvent.title)
        click_label = QtWidgets.QLabel(self)
        click_label.setText("Click for more...")
        click_label.setWordWrap(True)
        click_label.setObjectName("click_label")

        main_layout.addWidget(title_label)
        main_layout.addWidget(click_label)
        self.clicked.connect(self.handleEventClick)

    def handleEventClick(self):
        self.eventViewer = EventDescriptionViewer(self.toDoEvent, None,
                                                  QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.eventViewer.exec_()


class CustomStackedLayout(QtWidgets.QStackedLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TodoCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, list_of_events, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_of_events = list_of_events

        self.table = self.findChild(QtWidgets.QTableView)
        self.table.viewport().installEventFilter(self)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        for event in self.list_of_events.values():
            if event.due_time == date:
                painter.setBrush(QtCore.Qt.red)
                painter.drawEllipse(rect.topLeft() + QtCore.QPoint(12, 7), 3, 3)

    def eventFilter(self, source, event):
        if (
                event.type() == QtCore.QEvent.MouseButtonDblClick
                and source is self.table.viewport()
        ):
            index = self.table.indexAt(event.pos())
            date = self.dateForCell(index.row(), index.column())
            today_events = [ev for ev in self.list_of_events.values() if ev.due_time == date]
            if today_events:
                self.handleDateClick(today_events)
        return super().eventFilter(source, event)

    def referenceDate(self):
        refDay = 1
        while refDay <= 31:
            refDate = QtCore.QDate(self.yearShown(), self.monthShown(), refDay)
            if refDate.isValid():
                return refDate
            refDay += 1
        return QtCore.QDate()

    @property
    def firstColumn(self):
        return (
            1
            if self.verticalHeaderFormat() == QtWidgets.QCalendarWidget.ISOWeekNumbers
            else 0
        )

    @property
    def firstRow(self):
        return (
            0
            if self.horizontalHeaderFormat()
               == QtWidgets.QCalendarWidget.NoHorizontalHeader
            else 1
        )

    def columnForDayOfWeek(self, day):
        if day < 1 or day > 7:
            return -1
        column = day - self.firstDayOfWeek()
        if column < 0:
            column += 7
        return column + self.firstColumn

    def columnForFirstOfMonth(self, date):
        return (self.columnForDayOfWeek(date.dayOfWeek()) - (date.day() % 7) + 8) % 7

    def dateForCell(self, row, column):
        if (
                row < self.firstRow
                or row > (self.firstRow + 6 - 1)
                or column < self.firstColumn
                or column > (self.firstColumn + 7 - 1)
        ):
            return QtCore.QDate()
        refDate = self.referenceDate()
        if not refDate.isValid():
            return QtCore.QDate()
        columnForFirstOfShownMonth = self.columnForFirstOfMonth(refDate)
        if columnForFirstOfShownMonth - self.firstColumn < 1:
            row -= 1
        requestedDay = (
                7 * (row - self.firstRow)
                + column
                - columnForFirstOfShownMonth
                - refDate.day()
                + 1
        )
        return refDate.addDays(requestedDay)

    def handleDateClick(self, days_events):
        date_click_dialog = CalendarClickDialog(days_events, None,
                                                QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        date_click_dialog.exec_()


class CalendarClickDialog(QtWidgets.QDialog):

    def __init__(self, events, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events = events
        self.setWindowTitle("Edit Event")
        self.setGeometry(250, 250, 400, 200)
        self.setFixedWidth(650)
        self.setMaximumHeight(1)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.initUI()

    def initUI(self):
        event_label = QtWidgets.QLabel(self)
        event_label.setText("Events")
        event_label.setObjectName("calendar_click_dialog_label")

        self.mainLayout.addWidget(event_label)

        for event in self.events:
            new_section = DisplayEventSection(event)
            self.mainLayout.addWidget(new_section)

        Btn = QDialogButtonBox.Ok
        okBtn = QDialogButtonBox(Btn)
        okBtn.accepted.connect(self.accept)
        self.mainLayout.addWidget(okBtn)
        self.mainLayout.addStretch(0)

    def handleEventUpdate(self):
        for i in reversed(range(self.mainLayout.count() - 1)):
            self.mainLayout.itemAt(i).widget().setParent(None)
        self.initUI()


class MinuteTimer(QTimer):
    customTimeout = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSingleShot(True)
        # default timer is CoarseTimer, which *could* fire up before, making it
        # possible that the timeout is called twice
        self.setTimerType(Qt.PreciseTimer)
        # to avoid unintentional disconnection (as disconnect() without arguments
        # disconnects the signal from *all* slots it's connected to), we
        # "overwrite" the internal timeout signal attribute name by switching it
        # with a custom signal instead
        self._internalTimeout = self.timeout
        self._internalTimeout.connect(self.startAdjusted)
        self._internalTimeout.connect(self.customTimeout)
        self.timeout = self.customTimeout

    def start(self):
        now = QTime.currentTime()
        nextMinute = QTime(now.hour(), now.minute()).addSecs(60)
        QTimer.start(self, now.msecsTo(nextMinute) % 86400000)

    def startAdjusted(self):
        now = QTime.currentTime()
        # even when using a PreciseTimer, it is possible that the timeout is
        # called before the minute change; if that's the case, add 2 minutes
        addSecs = 120 if now.second() > 50 else 60
        nextMinute = QTime(now.hour(), now.minute()).addSecs(addSecs)
        QTimer.start(self, now.msecsTo(nextMinute) % 86400000)


class TodoEvent:

    def __init__(self, title, due_time, remind_time, description):
        self.title = title
        self.due_time = due_time
        self.remind_time = remind_time
        self.description = description
        toDoEvents[self.title] = self

    def change_title(self, new_title):
        self.title = new_title

    def change_due_time(self, new_due_time):
        self.due_time = new_due_time

    def change_remind_time(self, new_remind_time):
        self.remind_time = new_remind_time

    def change_description(self, new_description):
        self.description = new_description


infile = open('ToDoEvents', 'rb')
toDoEvents = pickle.load(infile)
infile.close()
