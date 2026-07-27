from openpyxl import *
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table,TableStyleInfo
import os
path = r'Excel\Data.xlsx'
workbook = Workbook()
if  os.path.exists(path):
    print("Path already exist !")
    workbook = load_workbook(path)
else:
    workbook[workbook.sheetnames[0]].title = 'Data1'
    worksheet = workbook.active
    table = Table(displayName = 'Employee_Table', ref = 'A1:D1')
    table.tableStyleInfo = TableStyleInfo(name = 'TableStyleMedium2', showFirstColumn=False, showLastColumn=False, showColumnStripes=True, showRowStripes=True )
    worksheet.add_table(table)

# worksheet['A1'] = 'Sri'
# worksheet['A2'] = 'Renga'
# worksheet['A3'] = 'Sarathy'
# worksheet.append(['R','Sri','Rengasarathy'])
# worksheet.append(['R','Yuvaraj','Kannan'])
# worksheet.append(['R','Naveen','Raja'])
# worksheet.append(['P S','Kiruba','Nidhi'])
# worksheet.append(['Y','Nikish','Daniel'])
# worksheet.append(['J S','Prawin','Kumar'])
# worksheet.append(['M','Sethu','Raj'])
# table.ref = f'A1:{get_column_letter(worksheet.max_column)}{worksheet.max_row}'
# workbook.create_sheet('Data2')
# worksheet.delete_rows(1,3)
# worksheet.delete_rows(1)
# worksheet.delete_cols(1,3)
# worksheet.delete_cols(1)


# if 'Employee_Table' not in workbook.tables:
#     workbook.append(['Id','Name','Age','Languages Known'])
    
# else:
#     table = workbook.tables['Employee_Table']


workbook.save(path)