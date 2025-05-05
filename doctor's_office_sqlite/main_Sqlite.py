
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent 
from PyQt5.QtGui import * 
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtCore
from datetime import date
#import ordonnance_sqlite_POO
# from PyQt5 import uic
# from instance_connection_access import get_sql_connection
import sqlite3

import sys
from os import path
#import pymsgbox
import ctypes
from sqliteDb import *
myFunc = SqliteDb("C:/allFiles/docteur.db")

today = date.today()

#import UI file
FORM_CLASS,_ =loadUiType(path.join(path.dirname(__file__),'C:/allFiles/Clinique.ui'))	

class MyProject(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MyProject, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.maFenetre()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.tableWidget.setColumnWidth(0, 250)
        # self.tableWidget.setColumnWidth(1, 100)
        # self.tableWidget.setColumnWidth(2, 350)
        # self.tableWidget.setHorizontalHeaderLabels(["City","Country","Subcountry"])

        self.tableVisites.setColumnWidth(0,0)
        self.tableVisites.setColumnWidth(1,30)
        self.tableVisites.setColumnWidth(2,80)
        self.tableVisites.setColumnWidth(3,473)
        self.afficher_client()
        text0=self.lineNo.text()
        self.tableClient.setColumnWidth(0,0)
        
        
        self.btn_save.clicked.connect(self.insert_client)
        self.closeButton.clicked.connect(lambda: self.close())
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())

        #self.btn_pdf.clicked.connect(self.show_ordonnance)
        self.btn_ShowPatients.clicked.connect(self.afficher_client)
        self.btn_delete.clicked.connect(self.delete_client)
        self.btn_update.clicked.connect(self.updateClient)
        self.btn_fill.clicked.connect(self.fill_From_tableClient_ToTextBox)

        self.btn_save_Observ.clicked.connect(self.insert_observ_client)
        self.btn_delete_visite.clicked.connect(self.delete_visite)
        self.btn_search.clicked.connect(self.recherche_client)
        self.tableClient.itemClicked.connect(self.selectRow_enregist)       
        self.tableClient.itemClicked.connect(self.selectRowVisites)
        self.tableVisites.itemPressed.connect (self.SelectRowV)
        self.tableClient.itemPressed.connect (self.SelectRowC)

            
#                                 ***********************
        

    def insert_client(self):     
        
        text1=self.lineEdit_1.text()
        text2=self.lineEdit_2.text()
        text3=self.lineEdit_3.text()
        text4=self.lineEdit_4.text()
        text5=self.lineEdit_5.text()
        text6=self.lineEdit_6.text()    
        if text1.strip(" ") != "" and text2.strip(" ") != "" :
        
            client =(text1,text2,text3,text4,text5,text6)
            myFunc.insert("INSERT INTO client(nom,prenom,datinscript,profession,adresse,telephone) VALUES (?,?,?,?,?,?)", client)
            self.refresh()
        else:
            show_message("Error")

        self.refresh()
        self.lineEdit_1.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        # rs.close()
        #         try:
            

#                                 ***********************
        
    def refresh(self):
        self.clearData()
        self.afficher_client()
        
#                                 ***********************
        
    def clearData(self):
        self.tableClient.clearSelection()
        while(self.tableClient.rowCount() > 0):
            self.tableClient.removeRow(0)
            self.tableClient.clearSelection()
        
#                                 ***********************
        
    def afficher_client(self):
        self.clearData()
        users = myFunc.select("SELECT * FROM client")
        
        for row_number, user in enumerate(users):
            self.tableClient.insertRow(row_number)
            for column_number, data in enumerate(user):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableClient.setItem(row_number,column_number,cell)
                
#                                 ***********************
                
    def fill_From_tableClient_ToTextBox(self):

        resultat = myFunc.select("SELECT * FROM client")
        # resultat = rs.execute(sql)
        for row in enumerate(resultat):
            if row[0] == self.tableClient.currentRow():
                data=row[1]
                # self.lineEditEnregist.setText(str(data[1])+" "+str(data[2]))
                self.lineNo.setText(str(data[0]))
                self.lineEdit_1.setText(str(data[1]))
                self.lineEdit_2.setText(str(data[2]))
                self.lineEdit_3.setText(str(data[3]))
                self.lineEdit_4.setText(str(data[4]))
                self.lineEdit_5.setText(str(data[5]))
                self.lineEdit_6.setText(str(data[6]))
                
 
        
#                       ***********************

                
    def updateClient(self):
        id_update = self.getSelectedClientId()
        text1=self.lineEdit_1.text()
        text2=self.lineEdit_2.text()
        text3=self.lineEdit_3.text()
        text4=self.lineEdit_4.text()
        text5=self.lineEdit_5.text()
        text6=self.lineEdit_6.text() 
        
        if text1.strip(" ") != "" and text2.strip(" ") != "" :
            
            client =(text1,text2,text3,text4,text5,text6)
            
            myFunc.update("UPDATE client SET nom = ?, prenom= ? , datinscript= ? , profession= ?, adresse= ?  ,telephone= ? WHERE id_c = "+id_update, client)
            self.refresh()
        else:
            show_message("Error")
            
        self.refresh()
        self.lineEdit_1.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
       
        
#                                 ***********************           
    
    def delete_client(self):
        message=QMessageBox.question(self, "u حذاري ", "هل تريد حذف هذا الزبون   ",
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            id_delete = self.getSelectedClientId()
            myFunc.delete("DELETE FROM client WHERE id_c = "+id_delete)
            self.refresh() 
        else:
            return              
                
    def getSelectedClientId(self):
        return self.tableClient.item(self.getSelectedRowIdClient(),0).text()             
                
                
    def getSelectedRowIdClient(self):
        return self.tableClient.currentRow()   


#                    *****************************  


    def recherche_client(self):        
        search=self.lineEdit_rech.text() 
 
        sql="select * from client Where nom LIKE ?"        
        result=myFunc.find2(sql, [search +"%"]) 
        self.tableClient.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableClient.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableClient.setItem(row_number, column_number, QTableWidgetItem(str(data)))
#        cnn.close()
                
                    
#******************************VISITES***********************************
          
    def SelectRowC(self):

        self.tableVisites.clearSelection()
        
#                       ***********************

    def selectRowVisites(self):
        
        self.tableVisites.clear()

        resultat = myFunc.select("SELECT * FROM client")
        for row in enumerate(resultat):
            if row[0] == self.tableClient.currentRow():
                data=row[1]               
                self.lineNo.setText(str(data[0]))
                sql=("select * from visites Where id_p_c ="+ str(data[0]))  #autoNo ,nomProf, date, detail
                
                 
                result=myFunc.select(sql)
                self.tableVisites.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.tableVisites.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableVisites.setItem(row_number, column_number, QTableWidgetItem(str(data)))

#                     ***********************
                                
    def selectRow_enregist(self):

        resultat = myFunc.select("SELECT * FROM client")
      
        for row in enumerate(resultat):
            if row[0] == self.tableClient.currentRow():
                data=row[1]
                self.lineNo.setText(str(data[0]))
                self.lineEditEnregist.setText(str(data[1])+" "+str(data[2])+"        profession: "+str(data[4])+"       habite  à : "+str(data[5]+"    tel:  "+str(data[6])))

        
#                     ***********************
    
    
    def insert_observ_client(self):

        textObserv = self.textEdit.toPlainText()
        textID=int(self.lineNo.text())
        try:
            data=(textID,today,textObserv)
            # user =(text1,text2,text3,text4,text5,text6)
            myFunc.insert("INSERT INTO visites(id_p_c,dateV,observation)VALUES(?,?,?)", data)
            # self.refresh()
            # QMessageBox.information(QMessageBox(),'Successful','client is added successfully to the database.')

        except Exception:
            # show_message("Error")
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add client to the database.')

        self.textEdit.setPlainText("")
        
#                      ***********************
  
    def SelectRowV(self):

        self.tableClient.clearSelection()
        
#                      *********************** 
        
    def delete_visite(self):
        self.tableClient.clearSelection()
        message=QMessageBox.question(self, "u حذاري ", "هل تريد حذف هذه الزيارة المسجلة  ",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
#            
            row=self.tableVisites.currentRow()
            self.tableVisites.removeRow(row)
            id_delete = self.getSelectedVisiteId()
            myFunc.delete("DELETE FROM visites WHERE id_order = "+id_delete)
           
        else:
            return
#                      ***********************        
        
    def getSelectedVisiteId(self):
        return self.tableVisites.item(self.getSelectedRowIdVisite(),0).text()             
                
#                      ***********************
                
    def getSelectedRowIdVisite(self):
        return self.tableVisites.currentRow() 
    
#                     ************************
        
    
  
    # def show_ordonnance(self): 

    #     self.open = ordonnance_sqlite_POO.My_ordonnance()
    #     self.open.show()
        
 #*************************************FIN****************************************  
        
    def maFenetre(self):            
        self.setFixedSize(1040,671)
        self.setWindowIcon(QIcon('chat.png'))     
# Execute app
# 
def main():            
    app = QApplication(sys.argv)
    window = MyProject()
    # window.ord_medic=uic.loadUi("ord_medic.ui")
    # connection=get_sql_connection()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
        

