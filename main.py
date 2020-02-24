import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui import *
from jwc import *


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('强智系统学生信息查询')
        self.setWindowIcon(QIcon('ui.ico'))
         if token == "":
            QtWidgets.QMessageBox.question(self, '错误', '从服务器获取数据失败，该软件目前不可用', QtWidgets.QMessageBox.Yes)
        self.list_url_school = list(url_school)
        self.comboBox_2.addItems(self.list_url_school)
        self.comboBox.addItems(date_list)
        self.comboBox_2.activated.connect(self.changeSchool)
        self.school_url = ""
        self.pushButton.clicked.connect(self.query)
        self.pushButton_2.clicked.connect(self.setXq)
        self.pushButton_3.clicked.connect(self.setJwcUrl)
        self.school_name = self.comboBox_2.currentText()

    def setXq(self):
        self.xq = self.lineEdit_2.text().strip()
        if self.xq == "":
            return
        self.comboBox.addItem(self.xq)
        self.comboBox.setCurrentIndex(self.comboBox.count()-1)

    def setJwcUrl(self):
        self.school_url = self.lineEdit_3.text().strip()
        if self.school_url == "":
            return
        self.comboBox_2.addItem(self.school_url)
        self.comboBox_2.setCurrentIndex(self.comboBox_2.count() - 1)

    def changeSchool(self):
        self.school_name = self.comboBox_2.currentText()

    def query(self):
        self.xh = self.lineEdit.text().strip()
        if self.xh == "":
            QtWidgets.QMessageBox.question(self, '警告', '请输入学号', QtWidgets.QMessageBox.Yes)
            return
        if self.school_name == "":
            QtWidgets.QMessageBox.question(self, '警告', '请选择学校', QtWidgets.QMessageBox.Yes)
            return
        if self.school_url!="":
            self.school = School(self.school_url, self.xh)
        else:
            self.school = School(url_school[self.school_name], self.xh)
        self.setUserTable()

        if self.comboBox.currentText() == '当前学期':
            date = self.school.getCurrentTime()['xnxqh']
            if date == None:
                QtWidgets.QMessageBox.question(self, '错误', '当前学期获取失败，请手动设置', QtWidgets.QMessageBox.Yes)
                return
            else:
                self.dataGrade = self.school.getGrade(date)
        elif self.comboBox.currentText() == '所有学期':
            self.dataGrade = []
            for xq in date_list[2:]:
                one_Grade = self.school.getGrade(xq)
                for i in one_Grade:
                    if i == None:
                        continue
                    self.dataGrade.append(i)
        else:
            self.dataGrade = self.school.getGrade(self.comboBox.currentText())
        if self.dataGrade == [None]:
            QtWidgets.QMessageBox.question(self, '警告', '没有查到成绩', QtWidgets.QMessageBox.Yes)
            return
        self.setGradeTable()

    def setGradeTable(self):
        # 表相关
        self.tableHead = ['课程名称', '成绩', '课程类别', '学分', '课程性质']
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # {'bz': None, 'cjbsmc': None, 'kclbmc': '必修', 'zcj': '49', 'xm': '娄景林', 'xqmc': '2019-2020-1', 'kcxzmc': '专业主干课',
        #  'kcywmc': None, 'ksxzmc': '正常考试', 'kcmc': '编译原理', 'xf': 3}
        self.model = QStandardItemModel(len(self.dataGrade), len(self.tableHead))
        # 设置横坐标每项的属性名
        self.model.setHorizontalHeaderLabels(self.tableHead)
        # 配置数据，注意！！！需要使用QStandardItem格式的文本
        for y in range(len(self.dataGrade)):
            self.model.setItem(y, 0, QStandardItem(self.dataGrade[y]['kcmc']))
            self.model.setItem(y, 1, QStandardItem(self.dataGrade[y]['zcj']))
            self.model.setItem(y, 2, QStandardItem(self.dataGrade[y]['kclbmc']))
            self.model.setItem(y, 3, QStandardItem(str(self.dataGrade[y]['xf'])))
            self.model.setItem(y, 4, QStandardItem(self.dataGrade[y]['kcxzmc']))
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)  # 禁止编辑

    def setUserTable(self):
        # 表相关
        self.dataUser = self.school.getUserInfo()
        if self.dataUser == {}:
            return
        self.tableHead = ['姓名', '性别', '专业名称', '年级', '班级', '院系名称', '入学年份', '学制',
                          '电话号码', '电子邮箱', 'qq', '高考考号']
        self.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model = QStandardItemModel(1, len(self.tableHead))
        # 设置横坐标每项的属性名
        self.model.setHorizontalHeaderLabels(self.tableHead)
        # 配置数据，注意！！！需要使用QStandardItem格式的文本
        self.model.setItem(0, 0, QStandardItem(self.dataUser['xm']))
        self.model.setItem(0, 1, QStandardItem(self.dataUser['xb']))
        self.model.setItem(0, 2, QStandardItem(self.dataUser['zymc']))
        self.model.setItem(0, 3, QStandardItem(self.dataUser['nj']))
        self.model.setItem(0, 4, QStandardItem(self.dataUser['bj']))
        self.model.setItem(0, 5, QStandardItem(self.dataUser['yxmc']))
        self.model.setItem(0, 6, QStandardItem(self.dataUser['rxnf']))
        self.model.setItem(0, 7, QStandardItem(str(self.dataUser['xz'])))
        self.model.setItem(0, 8, QStandardItem(self.dataUser['dh']))
        self.model.setItem(0, 9, QStandardItem(self.dataUser['email']))
        self.model.setItem(0, 10, QStandardItem(self.dataUser['qq']))
        self.model.setItem(0, 11, QStandardItem(self.dataUser['ksh']))
        self.tableView_2.setModel(self.model)

        # self.tableView_2.setEditTriggers(QTableView.NoEditTriggers)  # 禁止编辑


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
