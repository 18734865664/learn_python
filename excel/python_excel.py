#! /usr/local/python3/bin/python3
# encode:utf8

import xlwt

title_list = ["姓名", "年龄"] 


def add_line(line_num, excel_name, a_list):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet("sheet1", cell_overwrite_ok = True)
    for i in range(0, len(a_list)):
        worksheet.write(line_num, i, a_list[i])
    workbook.save(excel_name)
    

add_line(0, 'test.xls', title_list)
