# Load packages
import os 
import itertools
import pandas as pd

from  datetime import date

# Directory
path = "C:/Users/Yatma Sarr/Desktop/Linh TP/Docs"

# Keep only files ending up with ".xlsx"
files = list(itertools.compress(os.listdir(path), ['.xlsx' in x for x in os.listdir(path)]))

# Import countries name
countries = pd.read_csv(path+"/countries.csv")[["CODE", "NAME"]]

# Remove the space after the code name e.g from 'AT ' to 'AT'
countries.CODE = [x.split(" ")[0] for x in countries.CODE]

# Function to get country name from country code
def getcountryname(code):
    try:
        return countries.query("CODE == @code").NAME.values[0][:-1]
    except:
        return "Unknown"

# Function to import data
def import_tabs(path, filename, submission_type:str):
    ''' Retrieve all sheets name except the ones beginning with "Temp"'''
    reading = pd.ExcelFile(path + "/" + filename)
    sheets = reading.sheet_names
    ''' Exclude Temp into the sheets names '''
    mysheets = list(itertools.compress(sheets, ["Temp" not in x for x in sheets]))
    
    ''' Append all tables in a list '''
    df = []
    for xx in mysheets:
        ''' read each tabs by keeping only Documents and Note columns'''
        onecountry = pd.read_excel(reading, xx, skiprows=2, usecols=lambda x: 'Unnamed' not in x)[["Documents ", "Note"]]
        # Replace the "Documents " column by "Documents"
        onecountry.rename(columns=lambda x: x.strip(), inplace=True) 


        ''' Add all the other columns into each table '''
        onecountry = onecountry.assign(Code = xx.split(" ")[0], # Choose only the country code by split with space
                                       Country = getcountryname(xx.split(" ")[0]), # provide the country name from the country code
                                       Study = 'Pre-Market' if xx.split(" ")[1] == "Pre" else 'Post-Market', # Add study type depending on the second part of the sheetname
                                       Tag = "1.0", 
                                       Created =str(date.today()), 
                                       Submission=submission_type)
        df.append(onecountry)

    ''' Concatenate all list of tables in one single table '''
    data = pd.concat(df)
    
    return data


# Run the import function
datalist = [import_tabs(path=path, filename=files[0], submission_type="Competent Authority"),
            import_tabs(path=path, filename=files[1], submission_type="Ethics Committee")]

# Concatenate all list of tables in one single table
data = pd.concat(datalist)

# Reorder columns
mydata = data[['Code', 'Country', 'Study', 'Tag', 'Created', 'Submission', 'Documents', 'Note']]

# Save data in csv format
mydata.to_csv(path + "/../global_tab.csv", index=False)