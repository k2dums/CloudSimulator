import xlwt
from xlwt import Workbook



def write(dataset,filename="values.xls"):
    """
    writes the results in an excel sheet and saves it \n
    It takes dataset and filename as parameter\n
    By default filename= "values.xls"\n
    dataset should be a dictionary\n
    where dataset={key1:[x1,x2,x3],key2:[x1,x2,x3]}]\n
    """
    row=0
    col=0
    wb=Workbook()
    sheet1=wb.add_sheet("Sheet 1")
    for item in dataset.items():
        row=0
        name=item[0]
        values=item[1]
        print(name)
        print(values)
        sheet1.write(row,col,name)
        row+=1
        for value in values:
            sheet1.write(row,col,value)
            row+=1
        col+=1
    wb.save(filename)



        
