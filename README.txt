Author: Crystalina Opaczewski
Last updated: 3/4/2026

Files Included

Artisan Portal GUI.py
artisan_portal_data.csv
README.txt
User Manual.txt


Artisan Portal Vendor Management System

Program Description

    Artisan Portal with the purpose to help coordinators manange vendor applications for craft
    fairs and artisan markets. It allows vendors to submit their applications and review their 
    application status. Coordinators are able to view, approve or decline applications, assign 
    booth locations, and leave notes for other coordinators. The program also allows coordinators
    to save their database as a csv file so that they can upload to the program of their choice
    easily. 

All vendor information is stored in a CSV file so the data can be easily viewed and edited if needed.

Main Features

Vendor Application Submission

    Vendors can enter their name, email address, and type of craft. The system checks that all fields 
    are filled out and that the email is valid.

Application Status Lookup

    Vendors can check their application status by entering their Vendor ID or email address.

Coordinator Review Panel
    Coordinators can view all vendor applications and perform several actions including:

        -Approving vendors
        -Declining vendors
        -Assigning booth numbers
        -Adding coordinator notes

CSV Data Storage

    All vendor data is saved to a CSV file named artisan_portal_data.csv. This allows the information 
    to persist between program runs.

Export Feature

    The system allows the user to export all vendor records to a new CSV file that can be saved anywhere on 
    the computer.

Program Requirements

    Python 3 must be installed on the computer.
    The program uses built-in Python libraries including:

csv
os
re
tkinter

No additional installations are required.

How to Run the Program

1. Open the Python file named “Artisan Portal GUI.py”.
2. Run the program using Python.
3. The Artisan Portal main menu window will open.
4. Use the buttons in the main menu to navigate through the system.




