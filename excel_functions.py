from openpyxl import load_workbook

from database_functions import insert_worksheet_data_to_database


def load_job_workbook():
    job_workbook = load_workbook('Sprint3Data.xlsx')
    job_worksheet = job_workbook.active
    return job_worksheet


def add_excel_job_data(cursor, job_worksheet):
    row_count = job_worksheet.max_row
    for row in range(2, row_count):
        company_name = job_worksheet.cell(row=row, column=1).value
        posted_ago = job_worksheet.cell(row=row, column=2).value
        job_id = job_worksheet.cell(row=row, column=3).value
        location = job_worksheet.cell(row=row, column=5).value
        salary_min = job_worksheet.cell(row=row, column=8).value
        salary_max = job_worksheet.cell(row=row, column=7).value
        salary_rate = job_worksheet.cell(row=row, column=9).value
        job_name = job_worksheet.cell(row=row, column=10).value
        insert_worksheet_data_to_database(cursor, job_id, job_name, company_name, location, posted_ago, salary_min,
                                          salary_max, salary_rate)
