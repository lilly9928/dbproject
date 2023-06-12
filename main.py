import datetime
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5 import uic
import pymysql
import random
import datetime as dt
from utils_for_sql import DBApi

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
        machine_search_combo = {'기기번호':'MachineID','송장번호':'invoiceID','상품번호':'ProductID' }

        order_search_combo = {'사업장아이디':'BusID','사업장이름':'BusName'}

        tech_obj_name = 'TechnicianID, TechnicianName'

        product_temp_obj_name = 'ProductID,ProductName,ManufacName,Quantity,UnitPrice'

        order_obj_name = 'machine_number,order_date,Bus_number,Bus_number_2,search_order_comboBox_6,MoveDate,none'

        self.setupUi(self)

        self.none.setHidden(True)
        ##Business_location
        self.View_Table(self.view_busnesslocation_input,"Bus_Loca")
        self.contract_search_btn_11.clicked.connect(lambda: self.View_Table(self.view_busnesslocation_input,"Bus_Loca",'*',
                                                                            f'{bussiness_search_combo[self.search_bussiness_comboBox.currentText()]} Like "%{self.search_bussiness_id.text()}%"'))
        self.combobox_additem(self.search_bussiness_comboBox,bussiness_search_combo)
        self.bussiness_input_btn.clicked.connect(lambda :  self.Insert_Table(self.view_busnesslocation_input,bussiness_obj_name,"Bus_Loca"))
        self.view_busnesslocation_input.clicked.connect(lambda: self.Get_RowData(self.view_busnesslocation_input,bussiness_obj_name))
        self.bussiness_modify_btn.clicked.connect(lambda: self.Modify_Table(self.view_busnesslocation_input,bussiness_obj_name,"BusID","Bus_Loca"))
        self.bussiness_delete_btn.clicked.connect(lambda: self.Delete_Row("BusID",self.view_busnesslocation_input,"Bus_Loca"))

        ##Vendor
        self.View_Table(self.view_vendor_input, "vendor")
        self.vendor_search_btn.clicked.connect(lambda : self.View_Table(self.view_vendor_input, "vendor",'*',f'{vendor_search_combo[self.search_vendor_comboBox.currentText()]}  Like "%{self.lineEdit_49.text()}%"'))
        self.combobox_additem(self.search_vendor_comboBox, vendor_search_combo)
        self.vendor_input_btn.clicked.connect(
            lambda: self.Insert_Table(self.view_vendor_input, vendor_obj_name, "vendor"))
        self.view_vendor_input.clicked.connect(
            lambda: self.Get_RowData(self.view_vendor_input, vendor_obj_name))
        self.vendor_modify_btn.clicked.connect(
            lambda: self.Modify_Table(self.view_vendor_input, vendor_obj_name, "VendorID", "vendor"))
        self.vendor_delete_btn.clicked.connect(
            lambda: self.Delete_Row("VendorID", self.view_vendor_input, "vendor"))

        ##구매기기현황
        self.View_Table(self.view_machine_input, "machine,product","MachineID,ProductName,ManufacName,Realquantity,Totalquantity","product.ProductID = machine.ProductID")
        self.machine_search_btn_2.clicked.connect(lambda:self.View_Table(self.view_machine_input, "machine,product","MachineID,ProductName,ManufacName,Realquantity,Totalquantity",
                                                                         f'product.ProductID = machine.ProductID and {machine_search_combo[self.search_machine_comboBox.currentText()]} like "%{self.lineEdit_50.text()}%"') )
        self.combobox_additem(self.search_machine_comboBox, machine_search_combo)
        # self.machine_modify_btn.clicked.connect(
            # lambda: self.Modify_Table(self.view_machine_input, machine_obj_name, "MachineID", "machine"))
        self.machine_delete_btn.clicked.connect(
            lambda: self.Delete_Row("MachineID", self.view_machine_input, "machine"))

        ##담당자현황
        self.View_Table(self.view_tech_input, "technician")
        self.tech_search_btn_23.clicked.connect(lambda: self.View_Table(self.view_tech_input, "technician",'*',f'TechnicianID Like "%{self.lineEdit_67.text()}%"'))
        self.tech_input_btn.clicked.connect(lambda: self.Insert_Table(self.view_tech_input, tech_obj_name, "technician"))
        self.view_tech_input.clicked.connect(lambda: self.Get_RowData(self.view_tech_input, tech_obj_name))
        self.tech_modify_btn.clicked.connect(
             lambda: self.Modify_Table(self.view_tech_input, tech_obj_name, "TechnicianID", "technician"))
        self.tech_delete_btn.clicked.connect(
            lambda: self.Delete_Row("TechnicianID", self.view_tech_input, "technician"))

         ##설치관리
        self.View_Table(self.view_order_input, "order_t")
        self.View_Table(self.view_req_input,"purreq_product as a,pur_req as b,bus_loca AS c", "a.PRID,a.ProductName,b.orderDate,b.BusID,c.BusName","a.PRID = b.PRID AND b.BusID = c.BusID")
        self.combobox_additem(self.search_order_comboBox_2,order_search_combo)
        self.contract_search_btn_8.clicked.connect(lambda: self.View_Table(self.view_req_input,"purreq_product as a,pur_req as b,bus_loca AS c", "a.PRID,a.ProductName,b.orderDate,b.BusID,c.BusName",
                                                                           f"a.PRID = b.PRID AND b.BusID = c.BusID and c.{order_search_combo[self.search_order_comboBox_2.currentText()]}"
                                                                           f" Like '%{self.lineEdit_51.text()}%'"))
        self.view_req_input.clicked.connect(lambda: self.view_req_click())
        self.combobox_additem(self.search_order_comboBox_6, self.Comb_List_2('technician'))
        self.order_input_btn.clicked.connect(lambda: self.Insert_OTable(self.view_order_input,order_obj_name,'order_t'))
        self.view_product_input.clicked.connect(
            lambda: self.machine_number.setText(self.view_product_input.selectedItems()[0].text()))

        self.View_Table(self.view_removeorder_input ,"order_t",'*',"PickUpDate = '0000-00-00' ")
        self.view_removeorder_input.clicked.connect(lambda: self.Bus_number_2.setText(self.view_removeorder_input.selectedItems()[4].text()))
        self.order_update_btn.clicked.connect(lambda:self.UpdateOrderTable())

        ##PurchaseOrder
        ##기기구매주문리스트
        self.View_Table(self.view_PurchaseOrder_input, "pur_order")
        self.purchaseOrder_input_btn.clicked.connect(
            lambda: self.Insert_orderproduct_table(self.view_Product_input, 'product'))
        self.view_PurchaseOrder_input.clicked.connect(lambda : self.Get_Product_view(self.view_PurchaseOrder_input,"product"))

        ##발주기기정보등록
        self.product_temp_input_btn.clicked.connect(lambda: self.Insert_temp_table_product(self.view_Product_input,product_temp_obj_name))
        ##거래처조회
        self.View_Table(self.view_vendor_PurOrder, "vendor")
        self.vendor_PurOrder_search.clicked.connect(lambda : self.View_Table(self.view_vendor_PurOrder,"vendor","*",f"{vendor_search_combo[self.search_vendor_PurOrder_comboBox.currentText()]} Like "
                                                                                                                    f"'%{self.search_vendor_PurOrder.text()}%'"))
        self.combobox_additem(self.search_vendor_PurOrder_comboBox, vendor_search_combo)
        self.view_vendor_PurOrder.clicked.connect(
            lambda: self.VendorID_PurOrder.setText(self.view_vendor_PurOrder.selectedItems()[0].text()))
        self.PurchaseOrder_delete_btn.clicked.connect(lambda: self.Delete_purchaseOrder(self.view_PurchaseOrder_input))

        self.View_Table(self.view_Product_input_2,"purreq_product","ProductName,Quantity")
        self.view_Product_input_2.clicked.connect(lambda: self.ProductName.setText(self.view_Product_input_2.selectedItems()[0].text()))
    #invoice

        self.View_Table(self.view_invoice,"invoice")
        self.invoice_search_btn.clicked.connect(lambda: self.View_Table(self.view_invoice,"invoice","*",f"invoiceID Like '%{self.invoice_search.text()}%'"))
        self.view_invoice.clicked.connect(lambda : self.Get_invoice_view(self.view_invoice))
        self.view_invoice_product.clicked.connect(lambda: self.GetProductRow(self.view_invoice_product))
        self.invoice_date_input.clicked.connect(lambda: self.UpdateTable(self.view_invoice,"invoice"))
        self.machine_input.clicked.connect(lambda: self.InsertMachine(self.view_machine,"machine"))


        self.View_Table(self.view_pr_bussiness,"bus_loca","BusID,BusName")
        self.view_pr_bussiness.clicked.connect(lambda: self.bus_id.setText(self.view_pr_bussiness.selectedItems()[0].text()))
        self.purchaseRequestProduct_input_btn.clicked.connect(lambda: self.Insert_temp_table_product(self.view_purreq_product_2,"product_name,quantity"))
        self.purchaseRequest_input_btn.clicked.connect(lambda: self.purchaseRequest_insert())
        self.View_Table(self.view_purreq, "pur_req,bus_loca", "PRID,pur_req.BUSID,BusName,OrderDate", "pur_req.BUSID = bus_loca.BusID")
        self.view_purreq.clicked.connect(lambda: self.View_Table(self.view_purreq_product,"purreq_product","ProductName,Quantity",f"PRID={self.view_purreq.selectedItems()[0].text()}"))
        self.tabWidget.tabBarClicked.connect(lambda : self.handle_tab_clicked())
        self.tabWidget_2.tabBarClicked.connect(lambda: self.handle_tab_clicked())
        self.tabWidget_3.tabBarClicked.connect(lambda: self.handle_tab_clicked())
        self.purreq_search_btn.clicked.connect(lambda : self.View_Table(self.view_purreq, "pur_req,bus_loca", "PRID,pur_req.BUSID,BusName,OrderDate", f"pur_req.BUSID = bus_loca.BusID and PRID Like '%{self.search_order_id.text()}%'"))




    def connectiondb(self):
        db_info = {
            "host": "localhost",
            "port": 3307,
            "user": "root",
            "password": "1234",
            "db": "dbproject",
            "charset": "utf8",
        }
        self.db_connect = pymysql.connect(**db_info)

        return self.db_connect
    def commitdb(self,sql):
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(sql)
                db_connect.commit()



    def random_id(self):
        date = dt.datetime.now()
        rand = random.randrange(1,10000)
        return date.year+date.month+date.hour+date.microsecond-rand
    def combobox_additem(self,obj_name,items):
        for item in items:
            obj_name.addItem(item)
    def UpdateOrderTable(self):
        order_tid= self.view_removeorder_input.selectedItems()[0].text()
        mn = self.view_removeorder_input.selectedItems()[1].text()
        date = self.PickUpdate.text()

        sql = f'UPDATE order_t set PickUpDate = "{date}" where orderTID = {order_tid}'
        print(sql)
        self.commitdb(sql)

        sql = f"Update machine set Realquantity = Realquantity+1 where MachineID = {mn} "
        self.commitdb(sql)


        self.handle_tab_clicked()
    def handle_tab_clicked(self):
        self.View_Table(self.view_busnesslocation_input, "Bus_Loca")
        self.View_Table(self.view_vendor_input, "vendor")
        self.View_Table(self.view_machine_input, "machine")
        self.View_Table(self.view_tech_input, "technician")
        self.View_Table(self.view_order_input, "order_t")
        self.View_Table(self.view_req_input, "purreq_product as a,pur_req as b",
                        "a.PRID,a.ProductName,b.orderDate,b.BusID", "a.PRID = b.PRID")
        self.View_Table(self.view_PurchaseOrder_input, "pur_order")
        self.View_Table(self.view_Product_input_2, "purreq_product", "ProductName,Quantity")
        self.View_Table(self.view_vendor_PurOrder, "vendor")
        self.View_Table(self.view_invoice, "invoice")
        self.View_Table(self.view_pr_bussiness, "bus_loca", "BusID,BusName")
        self.View_Table(self.view_purreq, "pur_req,bus_loca", "PRID,pur_req.BUSID,BusName,OrderDate",
                        "pur_req.BUSID = bus_loca.BusID")
        self.combobox_additem(self.search_order_comboBox_6, self.Comb_List_2('technician'))
        self.View_Table(self.view_removeorder_input, "order_t", '*', "PickUpDate = '0000-00-00' ")


    def view_req_click(self):
        name =self.view_req_input.selectedItems()[1].text()
        bus_id = self.view_req_input.selectedItems()[3].text()
        order_date = self.view_req_input.selectedItems()[2].text()

        self.order_date.setText(order_date)
        self.Bus_number.setText(bus_id)
        self.Bus_number_2.setText(bus_id)
        self.View_Table(self.view_product_input, "machine,product", "MachineID,ProductName,ManufacName,Realquantity,Totalquantity",
                       f"machine.ProductID = product.ProductID and ProductName like '%{name}%'")

    def purchaseRequest_insert(self):
        PRID = self.random_id()
        BUSID = self.bus_id.text()
        orderDate = self.orderdate.text()
        row = self.view_purreq_product_2.rowCount()

        sql = f"INSERT INTO pur_req values ({PRID},{BUSID},'{orderDate}')"
        print(sql)
        self.commitdb(sql)

        for r in range(row):
            PRPID = self.random_id()
            product_name = self.view_purreq_product_2.item(r,0).text()
            quantity = self.view_purreq_product_2.item(r,1).text()
            sql = f"INSERT INTO purreq_product values ({PRPID},'{product_name}',{PRID},{quantity})"
            print(sql)
            self.commitdb(sql)

        self.view_purreq.setRowCount(0)
        self.view_purreq_product_2.setRowCount(0)

        self.View_Table(self.view_purreq, "pur_req,bus_loca", "PRID,pur_req.BUSID,BusName,OrderDate",
                        "pur_req.BUSID = bus_loca.BusID")




    def view_pur_req(self):
        row_num = 0
        select_sql = f"SELECT POID,BUSID,BusName,OrderDate from pur_req,bus_loca where BUSID = BusID"
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    self.view_purreq.insertRow(row_num)
                    for i in range(len(data)):
                        self.view_purreq.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1
    def InsertMachine(self,obj_name,table):
        machineid = self.random_id()
        invoiceid = self.m_invoiceID.text()
        productid = self.product_id.text()
        qunt = self.machine_Totalquantity.text()

        sql = f'INSERT into {table} values ({machineid},{invoiceid},{productid},{qunt},{qunt})'
        print(sql)

        self.commitdb(sql)

        obj_name.setRowCount(0)
        row_num = 0
        select_sql = f"SELECT * from {table} where machine.invoiceID = {invoiceid}"
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    obj_name.insertRow(row_num)
                    for i in range(len(data)):
                        obj_name.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1

        self.view_invoice_product.setRowCount(0)
        row_num = 0
        select_sql = f"SELECT product.ProductID,product_sid,ProductName,ManufacName,Quantity,UnitPrice,InVoiceNumber,PurOrderID FROM product" \
                     f" WHERE ProductID NOT IN (SELECT productID FROM machine) AND InvoiceNumber ={invoiceid}"
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    self.view_invoice_product.insertRow(row_num)
                    for i in range(len(data)):
                        self.view_invoice_product.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1

    def UpdateTable(self,obj_name,table):
        date = self.shipdate.text()
        invoice = self.m_invoiceID.text()
        sql = f'update {table} set shipdate = "{date}" where InvoiceID = {invoice}'
        print(sql)

        self.commitdb(sql)

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
                        obj_name.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1
    def GetProductRow(self,obj_name):
        product_num = obj_name.selectedItems()[0].text()
        product_qunt = obj_name.selectedItems()[4].text()
        self.product_id.setText(product_num)
        self.machine_Totalquantity.setText(product_qunt)

    def Get_invoice_view(self,obj_name):
        purorderid = obj_name.selectedItems()[1].text()
        invoiceid= obj_name.selectedItems()[0].text()
        vendorid = obj_name.selectedItems()[2].text()

        self.m_invoiceID.setText(invoiceid)
        self.m_VendorID.setText(vendorid)

        self.view_invoice_product.setRowCount(0)
        self.view_machine.setRowCount(0)


        row_num = 0
        select_sql = f"SELECT product.ProductID,product_sid,ProductName,ManufacName,Quantity,UnitPrice,InVoiceNumber,PurOrderID FROM product" \
                     f" WHERE ProductID NOT IN (SELECT productID FROM machine) AND InvoiceNumber ={invoiceid}"
        print(select_sql)
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    self.view_invoice_product.insertRow(row_num)
                    for i in range(len(data)):
                        self.view_invoice_product.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1

        row_num = 0
        select_sql = f"SELECT * from machine where InvoiceID = {invoiceid} "
        print(select_sql)
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    self.view_machine.insertRow(row_num)
                    for i in range(len(data)):
                        self.view_machine.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1



    def Delete_purchaseOrder(self,obj_name):
        key = obj_name.selectedItems()[0].text()

        delete_product_sql = f"DELETE FROM product Where PurOrderID = {key}"
        print(delete_product_sql)
        self.commitdb(delete_product_sql)

        delete_invoice_sql = f"DELETE FROM invoice Where POID = {key}"
        print(delete_invoice_sql)
        self.commitdb(delete_invoice_sql)

        delete_pruorder_sql = f"DELETE FROM pur_order Where POID = {key}"
        print(delete_pruorder_sql)
        self.commitdb(delete_pruorder_sql)

        self.View_Table(obj_name, "pur_order")
        self.view_order_product.setRowCount(0)


    def Get_Product_view(self,obj_name,table):
        self.view_order_product.setRowCount(0)
        items = obj_name.selectedItems()
        key = items[0].text()
        row_num = 0
        select_sql = f"SELECT * from {table} Where PurOrderID = {key}"
        print(select_sql)
        with self.connectiondb() as db_connect:
            with db_connect.cursor() as cur:
                cur.execute(select_sql)
                res = cur.fetchall()
                for data in res:
                    self.view_order_product.insertRow(row_num)
                    for i in range(len(data)):
                        self.view_order_product.setItem(row_num, i, QTableWidgetItem(str(data[i])))
                    row_num += 1



    def Insert_orderproduct_table(self,obj_name,table):
        row_num = obj_name.rowCount()
        col_num = obj_name.columnCount()
        order_id = self.random_id()
        invoice_id = self.random_id()
        today = dt.datetime.now()
        day_format = str(today.year)+'-'+str(today.month)+'-'+str(today.day)

        insert_order_sql = f'INSERT INTO {"pur_order"} values ({order_id},{self.VendorID_PurOrder.text()},"{day_format}")'
        print(insert_order_sql)
        self.commitdb(insert_order_sql)

        insert_invoice_sql = f'INSERT INTO invoice values ({invoice_id},{order_id},{self.VendorID_PurOrder.text()},"{day_format}",NULL,NULL)'
        print(insert_invoice_sql)
        self.commitdb(insert_invoice_sql)


        for i in range(row_num):
            pid = self.random_id()
            insert_sql = f"INSERT INTO {table} values({pid},"
            for j in range(col_num):
                insert_sql+= "'"+obj_name.item(i,j).text()+"'"
                if j != col_num-1:
                    insert_sql += ','
                else:
                    insert_sql+=f',{invoice_id},"{order_id}")'

            print(insert_sql)
            self.commitdb(insert_sql)

        self.view_Product_input.setRowCount(0)
        self.View_Table(self.view_PurchaseOrder_input,"pur_order")


    def Insert_temp_table(self,obj_name,insert_obj_names):
        row_num = obj_name.rowCount()
        obj_name.insertRow(row_num)

        num = self.random_id()

        insert_obj_name_list = insert_obj_names.split(',')
        insert_sql_list = []

        obj_name.setItem(row_num, 0, QTableWidgetItem(str(num)))
        insert_sql_list.append(str(num))
        for j in range(len(insert_obj_name_list) - 1):
            input_opj = eval(f"self.{insert_obj_name_list[j + 1]}")
            if type(input_opj) ==QComboBox:
                text = input_opj.currentText()
            else:
                text = input_opj.text()
            obj_name.setItem(row_num, j + 1, QTableWidgetItem(text))
            insert_sql_list.append(text)

        return insert_sql_list

    def Insert_order_table(self, obj_name, insert_obj_names):
        row_num = obj_name.rowCount()
        obj_name.insertRow(row_num)

        num = self.random_id()

        insert_obj_name_list = insert_obj_names.split(',')
        insert_sql_list = []

        obj_name.setItem(row_num, 0, QTableWidgetItem(str(num)))
        insert_sql_list.append(str(num))
        for j in range(len(insert_obj_name_list)):
            input_opj = eval(f"self.{insert_obj_name_list[j]}")
            if type(input_opj) == QComboBox:
                text = input_opj.currentText()
            else:
                text = input_opj.text()
            obj_name.setItem(row_num, j + 1, QTableWidgetItem(text))
            insert_sql_list.append(text)

        return insert_sql_list


    def Insert_temp_table_product(self,obj_name,insert_obj_names):
        row_num = obj_name.rowCount()
        obj_name.insertRow(row_num)

        insert_obj_name_list = insert_obj_names.split(',')
        insert_sql_list = []

        for j in range(len(insert_obj_name_list)):
            text = eval('self.' + insert_obj_name_list[j] + '.text()')
            obj_name.setItem(row_num, j, QTableWidgetItem(text))
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
        print(insert_sql_list)

        insert_sql = f"INSERT into {table} values ("

        for i in range(len(insert_sql_list)):
            insert_sql += "'"+insert_sql_list[i]+"'"
            if i != len(insert_sql_list)-1:
                insert_sql += ','
            else:
                insert_sql += ")"

        print(insert_sql)
        self.commitdb(insert_sql)

    def Insert_OTable(self, obj_name, insert_obj_names, table):
        mn= self.machine_number.text()
        insert_sql_list = self.Insert_order_table(obj_name, insert_obj_names)
        print(insert_sql_list)

        insert_sql = f"INSERT into {table} values ("

        for i in range(len(insert_sql_list)):
            insert_sql += "'" + insert_sql_list[i] + "'"
            if i != len(insert_sql_list) - 1:
                insert_sql += ','
            else:
                insert_sql += ")"

        print(insert_sql)
        self.commitdb(insert_sql)

        sql = f"Update machine set Realquantity = Realquantity-1 where MachineID = {mn} "
        self.commitdb(sql)

        self.handle_tab_clicked()


    def Insert_ProductOrder_Table(self,obj_name,insert_obj_names,table):

        insert_sql_list = self.Insert_temp_table(obj_name,insert_obj_names)

        insert_sql = f"INSERT into {table} values ("

        for i in range(len(insert_sql_list)):
            insert_sql += "'"+insert_sql_list[i]+"'"
            if i != len(insert_sql_list)-1:
                insert_sql += ','
            else:
                insert_sql += ")"

        self.commitdb(insert_sql)

    def get_all_item(self,obj_name):
        col=obj_name.columnCount()
        row = obj_name.rowCount()

        insert_sql_list=[]

        for r in range(row):
            list = []
            for c in range(col):
                list.append(obj_name.item(r,c).text())

            insert_sql_list.append(list)

        print(insert_sql_list)

        return insert_sql_list

    def View_Table(self,obj_name,table,select='*',where=''):

        obj_name.setRowCount(0)
        row_num = 0
        select_sql = f"SELECT {select} from {table}"
        if where != '':
            select_sql += f" WHERE {where}"
        print(select_sql)
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

        self.commitdb(modify_sql)

        self.View_Table(obj_name,table)

    def Delete_Row(self,obj_name,view_obj_name,table):

        key_num = eval('self.'+obj_name+'.text()')
        delete_sql = f"DELETE FROM {table} WHERE {obj_name} = '{key_num}'"

        self.commitdb(delete_sql)

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
            comb_list = []
            for data in res:
                comb_list.append(str(data[0]))
        return comb_list    
    

# 실행
if __name__ == '__main__':


    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()

    app.exec_()
    