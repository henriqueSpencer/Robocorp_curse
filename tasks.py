import time

from robocorp import browser
from robocorp.tasks import task
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from RPA.PDF import PDF


@task
def minimal_task():
    """ This is a minimal task. """
    # Slow down the browser to make it easier to see what's happening.
    # browser.configure(
    #     slowmo=1000,
    # )
    open_the_intranet_website()
    login_into_the_intranet()
    # fill_and_submit_the_sales_form()
    download_the_sales_report()
    fill_the_sales_report_with_excel_data()
    collet_results()
    export_as_pdf()
    log_out()

def open_the_intranet_website():
    """ Opens the intranet website. """
    print("Opening the intranet website.")
    browser.goto("https://robotsparebinindustries.com/")

def login_into_the_intranet():
    """ Logs into the intranet portal filling the form and click in login. """
    print("Logging into the intranet.")
    
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")
    #time.sleep(5000)

def fill_and_submit_the_sales_form(row):
    """ Fills the form. """
    print("Filling the form.")
    page = browser.page()
    page.fill("id=firstname", row['First Name'])
    page.fill("id=lastname", row['Last Name'])
   
    page.select_option("id=salestarget", str(row['Sales Target']))
    page.fill("id=salesresult", str(row['Sales']))
    page.click("button:text('Submit')")


def download_the_sales_report():
    """ Downloads the sales report. """
    print("Downloading the sales report.")
    # page = browser.page()
    # page.click("button:text('Download report')")
    # time.sleep(5000)
    http = HTTP()
    http.download("https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)

def fill_the_sales_report_with_excel_data():
    """ Fills the sales report. """
    print("Filling the sales report.")
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet = excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()
    
    for row in worksheet:
        fill_and_submit_the_sales_form(row)

def collet_results():
    """ Take a scrin shot of the results. """
    page = browser.page()
    page.screenshot(path="output/sales_summary.png")

def log_out():
    """ Logs out from the intranet. """
    print("Logging out.")
    page = browser.page()
    page.click("button:text('Log out')")

def export_as_pdf():
    """ Export the sales report as PDF. """
    print("Exporting the sales report as PDF.")
    page = browser.page()
    sales_results_html = page.locator("#sales-results").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")






