import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5 import uic
import pymysql
import random
#from utils_for_sql import *

## python실행파일 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from_class = uic.loadUiType(BASE_DIR + r'\window.ui')[0]


# MainWindow Class 선언
class WindowClass(QWidget, from_class):
    def __init__(self):
        super().__init__()
        '''object name define'''
        bussiness_obj_name = 'BusID,BusName,Busaddress,Bustel,StartDate,EndDate,Ower'
        bussiness_search_combo = {'사업장아이디':'BusID','사업장이름':'BusName','사업장전화번호':'Bustel','계약시작일':'StartDate','계약종료일':'EndDate','대표자명':'ower'}

        vendor_obj_name = 'VendorID,VendorName,Vendoraddress,VendorTel,VendorFax'
        vendor_search_combo = {'거래처아이디':'VendorID','거래처명':'VendorName','전화번호':'VendorTel','팩스번호':'VendorFax'}

        machine_obj_name = 'MachineID, invoiceID, productID'
        machine_search_combo = {'기기번호':'machineID','송장번호':'invoiceID','상품번호':'productID' }

        tech_obj_name = 'TechnicianID, TechnicianName'

        order_obj_name = 'OrderID, MachineID_2, Orderdate_2, Inst_BusID, Rem_BusID, TechnicianID_2'

        product_temp_obj_name = 'ProductID,ProductName,ManufacName,Quantity,UnitPrice'

        self.setupUi(self)

        ##Business_location
        self.View_Table(self.view_busnesslocation_input,"Bus_Loca")
        self.combobox_additem(self.search_bussiness_comboBox,bussiness_search_combo)
        self.bussiness_input_btn.clicked.connect(lambda :  self.Insert_Table(self.view_busnesslocation_input,bussiness_obj_name,"Bus_Loca"))
        self.view_busnesslocation_input.clicked.connect(lambda: self.Get_RowData(self.view_busnesslocation_input,bussiness_obj_name))
        # self.bussiness_modify_btn.clicked.connect(lambda: self.Modify_Table(self.view_busnesslocation_input,bussiness_obj_name,"BusID","Bus_Loca"))
        self.bussiness_delete_btn.clicked.connect(lambda: self.Delete_Row("BusID",self.view_busnesslocation_input,"Bus_Loca"))

        ##Vendor
        self.View_Table(self.view_vendor_input, "vendor")
        self.combobox_additem(self.search_vendor_comboBox, vendor_search_combo)
        self.vendor_input_btn.clicked.connect(
            lambda: self.Insert_Table(self.view_vendor_input, vendor_obj_name, "vendor"))
        self.view_vendor_input.clicked.connect(
            lambda: self.Get_RowData(self.view_vendor_input, vendor_obj_name))
        # self.vendor_modify_btn.clicked.connect(
            # lambda: self.Modify_Table(self.view_vendor_input, vendor_obj_name, "VendorID", "vendor"))
        self.vendor_delete_btn.clicked.connect(
            lambda: self.Delete_Row("VendorID", self.view_vendor_input, "vendor"))

        ##구매기기현황
        self.View_Table(self.view_machine_input, "machine")
        self.combobox_additem(self.search_machine_comboBox, machine_search_combo)
        self.machine_input_btn.clicked.connect(lambda: self.Insert_Table(self.view_machine_input, machine_obj_name, "machine"))
        self.view_machine_input.clicked.connect(lambda: self.Get_RowData(self.view_machine_input, machine_obj_name))
        # self.machine_modify_btn.clicked.connect(
            # lambda: self.Modify_Table(self.view_machine_input, machine_obj_name, "MachineID", "machine"))
        self.machine_delete_btn.clicked.connect(
            lambda: self.Delete_Row("MachineID", self.view_machine_input, "machine"))
        
        ##담당자현황
        self.View_Table(self.view_tech_input, "technician")
        self.tech_input_btn.clicked.connect(lambda: self.Insert_Table(self.view_tech_input, tech_obj_name, "technician"))
        self.view_tech_input.clicked.connect(lambda: self.Get_RowData(self.view_tech_input, tech_obj_name))
        # self.tech_modify_btn.clicked.connect(
            # lambda: self.Modify_Table(self.view_tech_input, tech_obj_name, "TechnicianID", "TechnicianName"))
        self.tech_delete_btn.clicked.connect(
            lambda: self.Delete_Row("TechnicianID", self.view_tech_input, "technician"))

         ##설치관리
        self.View_Table(self.view_order_input, "order_t")
        self.combobox_additem(self.search_order_comboBox_3, self.Comb_List_1('machine'))
        self.combobox_additem(self.search_order_comboBox_4, self.Comb_List_2('bus_loca'))
        self.combobox_additem(self.search_order_comboBox_5, self.Comb_List_2('bus_loca'))
        self.combobox_additem(self.search_order_comboBox_6, self.Comb_List_2('technician'))
        self.order_input_btn.clicked.connect(lambda: self.Insert_Table_order(self.view_order_input, "order_t"))
        self.view_order_input.clicked.connect(lambda: self.Get_RowData(self.view_order_input, order_obj_name))
        self.order_delete_btn.clicked.connect(lambda: self.Delete_Row("OrderID", self.view_order_input, "order_t"))        

        ##PurchaseOrder
        ##기기구매주문리스트
        self.View_Table(self.view_PurchaseOrder_input, "pur_order")
        self.product_temp_input_btn.clicked.connect(lambda: self.Insert_temp_table(self.view_Product_input,product_temp_obj_name))
       
        ##발주기기정보등록
        self.View_Table(self.view_Product_input, "product")

        ##거래처조회
        self.View_Table(self.view_vendor_PurOrder, "vendor")
        self.combobox_additem(self.search_vendor_PurOrder_comboBox, bussiness_search_combo)
        self.view_vendor_PurOrder.clicked.connect(
            lambda: self.VendorID_PurOrder.setText(self.view_vendor_PurOrder.selectedItems()[0].text()))


        self.purchaseOrder_input_btn.clicked.connect(lambda: self.Insert_from_table(self.view_Product_input,'product'))


    def connectiondb(self):
        db_info = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "1q2w3e4r",
            "db": "grouppjt",
            "charset": "utf8",
        }
        self.db_connect = pymysql.connect(**db_info)

        return self.db_connect

    def combobox_additem(self,obj_name,items):
        for item in items:
            obj_name.addItem(item)

    def Insert_from_table(self,obj_name,table):
        row_num = obj_name.rowCount()
        col_num = obj_name.columnCount()
        for i in range(row_num):
            insert_sql = f"INSERT INTO {table} values("
            for j in range(col_num):
                insert_sql+= "'"+obj_name.item(i,j).text()+"'"
                if j != col_num-1:
                    insert_sql += ','
                else:
                    insert_sql += ')'

            with self.connectiondb() as db_connect:
                with db_connect.cursor() as cur:
                    cur.execute(insert_sql)
                    db_connect.commit()

    def Insert_temp_table(self,obj_name,insert_obj_names):
        row_num = obj_name.rowCount()
        obj_name.insertRow(row_num)

        num = random.randrange(1,10000)

        insert_obj_name_list = insert_obj_names.split(',')
        insert_sql_list = []

        obj_name.setItem(row_num, 0, QTableWidgetItem(str(num)))
        insert_sql_list.append(str(num))
        for j in range(len(insert_obj_name_list) - 1):
            text = eval('self.' + insert_obj_name_list[j + 1] + '.text()')
            obj_name.setItem(row_num, j + 1, QTableWidgetItem(text))
            insert_sql_list.append(text)

        return insert_sql_list

    def Insert_temp_table_order(self,obj_name):
        row_num = obj_name.rowCount()
        obj_name.insertRow(row_num)

        insert_sql_list = []

        num = random.randrange(1,10000)

        obj_name.setItem(row_num, 0, QTableWidgetItem(str(num)))
        insert_sql_list.append(str(num))

        insert_sql_list_order = [self.search_order_comboBox_3.currentText(), self.Orderdate.text(), self.search_order_comboBox_4.currentText().split()[0],self.search_order_comboBox_5.currentText().split()[0], self.search_order_comboBox_6.currentText().split()[0]]
        insert_sql_list.extend(insert_sql_list_order)

        for j in range(len(insert_sql_list) - 1):
            obj_name.setItem(row_num, j + 1, QTableWidgetItem(insert_sql_list[j+1]))
        # print(insert_sql_list)
        return insert_sql_list

    
    def Insert_Table(self,obj_name,insert_obj_names,table):

        insert_sql_list = self.Insert_temp_table(obj_name,insert_obj_names)

        insert_sql = f"INSERT into {table} values ("

        for i in range(len(insert_sql_list)):
            insert_sql += "'"+insert_sql_list[i]+"'"
            if i != len(insert_sql_list)-1:
                insert_sql += ','
            else:
                insert_sql += ")"

        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(insert_sql)
                db_connect.commit()

    def Insert_Table_order(self,obj_name,table):

        insert_sql_list = self.Insert_temp_table_order(obj_name)
        print(insert_sql_list)
        
        insert_sql = f"INSERT into {table} values ("

        for i in range(len(insert_sql_list)):
            if insert_sql_list[i] == 'null':
                insert_sql += insert_sql_list[i]
                if i != len(insert_sql_list)-1:
                    insert_sql += ','
                else:
                    insert_sql += ")"
            else:
                insert_sql += "'"+insert_sql_list[i]+"'"
                if i != len(insert_sql_list)-1:
                    insert_sql += ','
                else:
                    insert_sql += ")"

        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(insert_sql)
                db_connect.commit()    

    def View_Table(self,obj_name,table):

        obj_name.setRowCount(0)
        row_num = 0
        select_sql = f"SELECT * from {table}"
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    obj_name.insertRow(row_num)
                    for i in range(len(data)):
                        obj_name.setItem(row_num,i,QTableWidgetItem(str(data[i])))
                    row_num += 1

    def Modify_Table(self,obj_name,modify_obj_names,key,table):
        modify_obj_name_list = modify_obj_names.split(',')
        key_num= eval('self.'+modify_obj_name_list[0]+'.text()')
        modify_sql = f"UPDATE {table} SET "
        for i in range(len(modify_obj_name_list)-1):
            modify_sql += f"{modify_obj_name_list[i+1]} = '{eval('self.'+modify_obj_name_list[i+1]+'.text()')}'"
            if i != len(modify_obj_name_list)-2:
                modify_sql += ','
            else:
                modify_sql += ' '
        modify_sql+=f"WHERE {key} = {key_num}"

        print(modify_sql)

        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(modify_sql)
                db_connect.commit()

        self.View_Table(obj_name,table)

    def Delete_Row(self,obj_name,view_obj_name,table):
        ## delete key 가져오는걸로 바꿔야함
        key_num = eval('self.'+obj_name+'.text()')
        delete_sql = f"DELETE FROM {table} WHERE {obj_name} = '{key_num}'"

        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(delete_sql)
                db_connect.commit()

        self.View_Table(view_obj_name, table)

    def Get_RowData(self,obj_name,input_opj_name):
        items=obj_name.selectedItems()
        input_opj_name_list = input_opj_name.split(',')
        for i in range(len(items)):
            input_opj = eval(f"self.{input_opj_name_list[i]}")
            if type(input_opj) == QLineEdit:
                input_opj.setText(f'{items[i].text()}')
            elif type(input_opj) == QLabel:
                input_opj.setHidden(True)
                input_opj.setText(f'{items[i].text()}')
            elif type(input_opj) == QDateEdit:
                date=items[i].text().split('-')
                input_opj.setDate(QDate(int(date[0]),int(date[1]),int(date[2])))

    def Comb_List_1(self, table):
        select_sql = f"SELECT * from {table}"
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
            comb_list = []
            for data in res:
                comb_list.append(str(data[0]))
        return comb_list
    
    def Comb_List_2(self, table):
        select_sql = f"SELECT * from {table}"
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
            comb_list = ['null']
            for data in res:
                comb_list.append(str(data[0])+" "+str(data[1]))
        return comb_list    
    

# 실행
if __name__ == '__main__':


    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()

    app.exec_()
    