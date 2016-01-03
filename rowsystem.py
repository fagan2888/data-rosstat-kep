"""Tests for development of CSV file reader with user-defined specification for variable names and location.   

The reader must produce a pandas dataframe from CSV file based on user-defined specification. The reader attempts 
to label data rows in CSV file with variable names (method *label_rowsystem()*), read qualified rows to database 
(omitted in this example, will store in memory) and create resulting dataframe (method get_dfa()).

Output: 
    GDP_DF - pandas dataframe fron reference data
    
Input:
    DOC - a string mimicing CSV file contents
    header_dict, unit_dict - a tuple of dictionaries used to parse table headers in CSV file to obtain variable names for each data row.

Methods:
    doc_to_rowsystem(doc)	
    label_rowsystem(rs, dicts)
    get_dfa(rs)    

Assumptions/steps: 
- data row starts with year, e.g  '2014'
- data rows are preceded with text rows containing variable text description and units of measurement 
- variable text description is linked to variable headname
- text containing unit of measurement is parsed to variable units
- in CSV file each variable is usually presented in several units of measurement: levels and different kinds of rates of growth

Naming convention:
- variable headname is written in CAPITAL letters (e.g. 'GDP', 'SOC_WAGE')
- variable unit is written in lowercase letters (e.g. 'bln_rub', 'yoy', 'rog')
- time series label is a combination of variable headname and unit (e.g. 'GDP_bln_rub')

The file contains following sections:
# --- hardcoded constrants ---
# --- methods --- 
# --- testing ---
"""

import pandas as pd

# --- hardcoded constrants ---
# input csv
predoc = ["1. Gross domestic product at current prices", "billion ruble",
          "YEAR\tVALUE", "2013\t61500", "2014\t64000",
          "percent change from previous year - annual basis", "2013\t1.013", "2014\t1.028"]
CSV_DOC = "\n".join(predoc)

# rowsystem corresponding to DOC string contents 
RS_FROM_FILE = [
       {'string':"1. Gross domestic product at current prices",
          'list':["1. Gross domestic product at current prices"],
		  'head':"1. Gross domestic product at current prices",
		  'is_data_row':False,
		  'header_label':None,
		  'unit_label':None},
		
		{'string':"billion ruble",
          'list':["billion ruble"],
		  'head':"billion ruble",
		  'is_data_row':False,
		  'header_label':None,
		  'unit_label':None},		  
		
		{'string':"YEAR\tVALUE",
          'list':["YEAR", "VALUE"],
		  'head':"YEAR",
		  'is_data_row':False,
		  'header_label':None,
		  'unit_label':None},
		  
		{'string':"2013\t61500",
          'list':["2013", "61500"],
		  'head':"2013",
		  'is_data_row':True,
		  'header_label':None,
		  'unit_label':None},

		{'string':"2014\t64000",
          'list':["2014", "64000"],
		  'head':"2014",
		  'is_data_row':True,
		  'header_label':None,
		  'unit_label':None},
          
 		{'string':"percent change from previous year - annual basis",
          'list':["percent change from previous year - annual basis"],
		  'head':"percent change from previous year - annual basis",
		  'is_data_row':False,
		  'header_label':None,
		  'unit_label':None},
		  
		{'string':"2013\t1.013",
          'list':["2013", "1.013"],
		  'head':"2013",
		  'is_data_row':True,
		  'header_label':None,
		  'unit_label':None},

		{'string':"2014\t1.028",
          'list':["2014", "1.028"],
		  'head':"2014",
		  'is_data_row':True,
		  'header_label':None,
		  'unit_label':None}         
]

# init LABELLED_RS - labelled rowsystem
LABELLED_RS = RS_FROM_FILE
for i in [3,4]:
    LABELLED_RS[i]['header_label'] = "GDP"
    LABELLED_RS[i]['unit_label'] = "bln_rub"	
for i in [6,7]:
    LABELLED_RS[i]['header_label'] = "GDP"
    LABELLED_RS[i]['unit_label'] = "yoy"
    
# init markup dictionaries 
header_dict = {"Gross domestic product": ["GDP", "bln_rub"]}
unit_dict = {'percent change to previous year': 'yoy'}
DICTS = header_dict, unit_dict 

# resulting dataframe
GDP_DF = pd.DataFrame.from_items([
                                 ('GDP_bln_rub', [61500, 64000])
                                ,('GDP_yoy', [1.013, 1.028])
				                 ])			 
GDP_DF.index = [2013,2014]								 


# --- methods --- 	
def doc_to_rowsystem(doc):
    """Import CSV file contents from *doc* and return corresponding rowsystem,
       where each line(row) from *doc* is presented as a dictionary containing 
       raw data and supplementary information.
       Working on a rowsystem facilitates parsing data rows and makes parser 
       code more organised."""
    return RS_FROM_FILE 

def label_rowsystem(rs, dicts):
    """Label data rows in rowsystems *rs* using *dicts* as markup.
       Returns *rs* with labels added in 'header_label' and 'unit_label'. 
    """
    return LABELLED_RS

def get_dfa(rs):
    """Returns pandas dataframe with ANNUAL data from labelled rowsystem *rs*."""
    # NOTE: will also need get_dfq(), get_dfm() as well as rowsystem_to_database(rs).
    return GDP_DF
	
# --- testing ---
rs1 = doc_to_rowsystem(CSV_DOC)
assert rs1 == RS_FROM_FILE 

rs2 = label_rowsystem(rs1, DICTS)
assert rs2 == LABELLED_RS 

df = get_dfa(rs2)
assert (df == GDP_DF).all().all()