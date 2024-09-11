""" 
 This is the second level of the curse
 
 Problema a ser resolvido:
    - Pega os dados em um csv https://robotsparebinindustries.com/orders.csv
    - Faz a ordem aqui: https://robotsparebinindustries.com/#/robot-order
    - save each order HTML receipt as a PDF file
    - save a screenshot of each of the ordered robots
    - embed the screenshot of the robot to the PDF receipt
    - create a ZIP archive of the PDF receipts 
    - complete all the orders even when there are technical failures
    - be available in public GitHub repository
    - possible to get the robot from the public GitHub repository and run it without manual setup
"""
import csv
import os
import time
import zipfile

from robocorp import browser
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from RPA.PDF import PDF


def curse_level_II_tasks():
    """ This gets the data from a csv and create a order for each row and generete a report in the end."""
    # Slow down the browser to make it easier to see what's happening.
    browser.configure(
        slowmo=1000,
    )
    list_robots_datas = get_input_data_from_csv()
    # print(list_robots_datas)
    open_the_intranet_website()
    files = []
    for robot_data in list_robots_datas:
        try:
            create_order(robot_data)
        except Exception as e:
            print(f"Error: {e}")
        else:
            files.append(save_order_receipt_as_pdf(robot_data))
            handle_order_new_robot()
            handle_pop_up()
    make_zip_with_pdfs(files)

def handle_order_new_robot():
    page = browser.page()
    page.click("button:text('Order another robot')")

def handle_pop_up():
    page = browser.page()
    page.click("button:text('OK')")

def open_the_intranet_website():
    """ Opens the intranet website. """
    print("Opening the intranet website.")
    browser.goto("https://robotsparebinindustries.com")
    time.sleep(5)
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    handle_pop_up()

def get_input_data_from_csv():
    """ download the csv and get the data from it """
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)
    excel = Files()
    
    with open("orders.csv", newline='', encoding='utf-8') as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        
        # Convert the CSV into a list of dictionaries
        data_list = [row for row in csv_dict_reader]
    return data_list

def create_order(robot_data):
    """ Creates a order with the data """
    #Order number,Head,Body,Legs,Address
    page = browser.page()
    #Head
    page.select_option("id=head", str(robot_data["Head"]))
    #Body
    page.check(f"id=id-body-{str(robot_data['Body'])}")
    #Legs
    page.fill('input[placeholder="Enter the part number for the legs"]', robot_data["Legs"])
    #Address
    page.fill('id=address', robot_data["Address"])

    page.click("button:text('Order')")
    # Check if the div exists
    div = page.query_selector('div.alert.alert-danger[role="alert"]')
    if div:
        raise Exception("Error creating the order")
    #     open_the_intranet_website(retry=False)
    #     create_order(robot_data)
    


def save_order_receipt_as_pdf(robot_data):
    """ Save the order receipt as a PDF """
    pdf_file_name = f"output/robot_receipt_{robot_data['Order number']}.pdf"
    robot_preview_data = get_order_preview_data()
    get_robot_screenshot()
    pdf = PDF()
    pdf.html_to_pdf(robot_preview_data, pdf_file_name)
    # Add the image to the PDF
    # pdf.add_files_to_pdf(files=["output/robot.png:align=center, width=20, height=20"],
    #                       target_document=f"output/robot_preview{robot_data['Order number']}.pdf")

    return pdf_file_name
    

def get_order_preview_data():
    page = browser.page()
    sales_results_html = page.locator("#order-completion").inner_html()
    return sales_results_html
    

def get_robot_screenshot():
    #<div id="robot-preview-image"><img src="/heads/1.png" alt="Head"><img src="/bodies/2.png" alt="Body"><img src="/legs/2.png" alt="Legs"></div>
    page = browser.page()
    robot_img = page.locator("id=robot-preview-image")
    #robot_img.is_visible()
    robot_img.screenshot(path="output/robot.png")

def make_zip_with_pdfs(files):
    """ Make a zip with the pdfs """
    output_zip_path = "output/robot_receipts.zip"
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the source folder
        for file in files:
            # Add the file to the ZIP archive, preserving the folder structure
            try:
                zipf.write(file)
            except Exception as e:
                continue


if __name__ == "__main__":
    curse_level_II_tasks()
  
