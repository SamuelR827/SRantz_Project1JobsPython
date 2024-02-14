from openpyxl import load_workbook


def load_job_workbook():
    job_workbook = load_workbook('Sprint3Data.xlsx')
    job_worksheet = job_workbook.active
    return job_worksheet


def get_job_data(job_worksheet):
    row_count = job_worksheet.max_row
    for row in range(2, row_count):
        company_name = job_worksheet.cell(row=row, column=1).value
        posted_ago = job_worksheet.cell(row=row, column=2).value
        location = job_worksheet.cell(row=row, column=5).value
        salary_min = job_worksheet.cell(row=row, column=7).value
        salary_max = job_worksheet.cell(row=row, column=8).value
        salary_type = job_worksheet.cell(row=row, column=9).value
        salary = parse_salary(salary_min, salary_max, salary_type)
        job_name = job_worksheet.cell(row=row, column=10).value
        print(company_name, posted_ago, location, salary, job_name)


def parse_salary(salary_min, salary_max, salary_type):
    if salary_type == 'N/A':
        return 'no salary specified'
    else:
        salary = str(salary_min) + ' - ' + str(salary_max) + ' ' + salary_type
        return salary




