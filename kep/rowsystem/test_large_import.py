import os
import io
import pandas as pd
from pandas.util.testing import assert_frame_equal   
from pprint import pprint

from spec_io import docstring_to_file, fcomp
from spec_io import load_spec, load_cfg
from rowsystem import init_rowsystem_from_folder, get_annual_df, get_qtr_df, get_monthly_df

def join_header_dicts(vars):
    """Join headers dict of variables listed in *vars*."""
    headers = {}
    for key in vars:
      headers.update(header_dicts[key])
    return headers  

# --------------------------------------------------------------------------------
#1. TEST IMPORT OF HEADERS AND UNITS DICTS FROM SPEC FILES
#

# ---- strings/docs ----
null_segment_definition = """# segment information
start line : null
end line : null
special reader: null

---\n"""

cpi_segment_definition = """# segment information
start line : 3.5. Индекс потребительских цен
end line : Из общего объема оборота розничной торговли
special reader: null

---\n"""

food_segment_definition = """# segment information
start line : Из общего объема оборота розничной торговли
end line : null
special reader: null

---\n"""


null_segment_dict = {'special reader': None, 'start line': None, 
                                             'end line':   None}
                                             
cpi_segment_dict  = {'special reader': None, 'start line': '3.5. Индекс потребительских цен', 
                                             'end line':   'Из общего объема оборота розничной торговли'}
                                             
food_segment_dict = {'special reader': None, 'start line': 'Из общего объема оборота розничной торговли',
                                             'end line':    None}

unit_definition = """в % к соответствующему периоду предыдущего года: yoy
в % к предыдущему периоду : rog
отчетный месяц в % к предыдущему месяцу : rog
отчетный месяц в % к соответствующему месяцу предыдущего года : yoy
период с начала отчетного года : ytd

---\n"""

spec_ip_doc = null_segment_definition + unit_definition + """
Индекс промышленного производства:
  - IND_PROD
  - yoy
"""

spec_ip_trans_inv_doc = null_segment_definition + unit_definition + """
Индекс промышленного производства:
  - IND_PROD
  - yoy

Производство транспортных средств и оборудования:
  - TRANS
  - Not specified
 
Инвестиции в основной капитал: 
  - INVESTMENT
  - bln_rub
"""

spec_cpi_block = cpi_segment_definition + unit_definition +  """
Индекс потребительских цен: 
  - CPI
  - rog

непродовольственные товары:
   - CPI_NONFOOD
   - rog  
""" 

spec_food_block = food_segment_definition + """bln rubles : bln_rub
---
пищевые продукты, включая напитки, и табачные изделия :
 - SALES_FOOD
 - bln_rub
 
непродовольственные товары :
 - SALES_NONFOOD
 - bln_rub
""" 

# ---- header and unit dicts ----

header_dicts = {
'ip'        :{'Индекс промышленного производства': ['IND_PROD', 'yoy']},
'trans'     :{'Производство транспортных средств и оборудования': ['TRANS', 'Not specified']},
'investment':{'Инвестиции в основной капитал': ['INVESTMENT', 'bln_rub']},
'cpi_block' :{'Индекс потребительских цен': ['CPI', 'rog'], 
              'непродовольственные товары': ['CPI_NONFOOD', 'rog']},  
'food_block':{'пищевые продукты, включая напитки, и табачные изделия': ['SALES_FOOD','bln_rub'],
              'непродовольственные товары': ['SALES_NONFOOD', 'bln_rub']}
}

common_unit_dict = {'в % к соответствующему периоду предыдущего года': 'yoy',
'в % к предыдущему периоду' : 'rog',
'отчетный месяц в % к предыдущему месяцу' : 'rog',
'отчетный месяц в % к соответствующему месяцу предыдущего года' : 'yoy',
'период с начала отчетного года' : 'ytd'}

unit_dicts = {
'ip'        : common_unit_dict,
'trans'     : common_unit_dict,
'investment': common_unit_dict,
'cpi_block' : common_unit_dict ,   
'food_block':{'bln rubles':'bln_rub'}
}

cpi_additional_spec_filename = "cpi_spec.txt"
food_additional_spec_filename = "retail_spec.txt"
cfg_txt = """- {0}
- {1}""".format(cpi_additional_spec_filename, food_additional_spec_filename)

cfg_list = [['3.5. Индекс потребительских цен', 
'Из общего объема оборота розничной торговли', 
({'Индекс потребительских цен': ['CPI', 'rog'], 'непродовольственные товары': ['CPI_NONFOOD', 'rog']}, 
{'период с начала отчетного года': 'ytd', 'в % к соответствующему периоду предыдущего года': 'yoy', 'отчетный месяц в % к предыдущему месяцу': 'rog', 'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 'в % к предыдущему периоду': 'rog'},
{'start line': '3.5. Индекс потребительских цен', 'end line': 'Из общего объема оборота розничной торговли', 'special reader': None})]
, ['Из общего объема оборота розничной торговли', None, 
({'пищевые продукты, включая напитки, и табачные изделия': ['SALES_FOOD', 'bln_rub'], 'непродовольственные товары': ['SALES_NONFOOD', 'bln_rub']}, 
{'bln rubles': 'bln_rub'}, 
{'start line': 'Из общего объема оборота розничной торговли', 'end line': None, 'special reader': None})]]

from rs_constants import full_raw_doc

def write_cfg():
    cfg = 'tab_cfg.txt'
    return docstring_to_file(cfg_txt, cfg)

def write_spec_files():
    spec = 'tab_spec.txt'
    docstring_to_file(spec_cpi_block,  cpi_additional_spec_filename)
    docstring_to_file(spec_food_block, food_additional_spec_filename)
    return docstring_to_file(spec_ip_trans_inv_doc, spec)

def write_csv():
   csv = 'tab.csv'   
   return docstring_to_file(full_raw_doc, csv)

def get_testable_files():
    # csv, spec, cfg = get_testable_files()
    return write_csv(), write_spec_files(), write_cfg()   

def remove_testable_files():
    for fn in get_testable_files():  
        os.remove(fn)
    os.remove(cpi_additional_spec_filename)
    os.remove(food_additional_spec_filename)

def test_cfg_import():
    spec = write_spec_files()
    cfg = write_cfg()    
    segments = load_cfg(cfg)
    assert segments == cfg_list

def cmp_spec(doc,var):
    return fcomp(doc, var, loader_func=load_spec)
            
def test_spec():
    cmp_spec(doc=spec_ip_doc, var=(header_dicts['ip'], unit_dicts['ip'], null_segment_dict))
    
    cmp_spec(doc=spec_ip_trans_inv_doc, 
             var=(join_header_dicts(['ip','trans','investment']),
                  common_unit_dict, null_segment_dict))
                  
    cmp_spec(doc=spec_cpi_block, 
             var=(header_dicts['cpi_block'], unit_dicts['cpi_block'], cpi_segment_dict))

    cmp_spec(doc=spec_food_block, 
             var=(header_dicts['food_block'], unit_dicts['food_block'], food_segment_dict))

dfa_csv = 'year,CPI_NONFOOD_rog,CPI_rog,IND_PROD_yoy,INVESTMENT_bln_rub,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub\n2014,108.1,111.4,101.7,13527.7,97.3,12380.9,13975.3\n'
dfq_csv = 'time_index,year,qtr,CPI_NONFOOD_rog,CPI_rog,IND_PROD_rog,IND_PROD_yoy,INVESTMENT_bln_rub,INVESTMENT_rog,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub\n2014-03-31,2014,1,101.4,102.3,87.6,101.1,1863.8,35.7,94.7,2729.6,3063.3\n2014-06-30,2014,2,101.5,102.4,103.6,101.8,2942.0,158.2,98.1,2966.3,3290.4\n2014-09-30,2014,3,101.4,101.4,102.7,101.5,3447.6,114.9,98.5,3140.1,3557.2\n2014-12-31,2014,4,103.6,104.8,109.6,102.1,5274.3,149.9,97.2,3544.9,4064.4\n'
dfm_csv = 'time_index,year,month,CPI_NONFOOD_rog,CPI_rog,IND_PROD_rog,IND_PROD_yoy,IND_PROD_ytd,INVESTMENT_bln_rub,INVESTMENT_rog,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub,TRANS_rog,TRANS_yoy,TRANS_ytd\n2014-01-31,2014,1,100.3,100.6,81.2,99.8,99.8,492.2,21.1,92.7,882.7,984.4,45.4,103.8,103.8\n2014-02-28,2014,2,100.4,100.7,101.6,102.1,100.9,643.2,129.6,95.5,884.5,986.8,131.8,113.2,108.9\n2014-03-31,2014,3,100.7,101.0,109.7,101.4,101.1,728.4,114.5,95.3,962.4,1092.1,123.9,114.2,111.0\n2014-04-30,2014,4,100.6,100.9,97.3,102.4,101.4,770.4,106.6,97.4,963.6,1079.3,102.3,119.6,113.4\n2014-05-31,2014,5,100.5,100.9,99.6,102.8,101.7,991.1,127.0,97.3,999.4,1095.6,88.8,118.3,114.8\n2014-06-30,2014,6,100.4,100.6,99.9,100.4,101.5,1180.5,119.0,99.3,1003.3,1115.5,116.3,111.7,114.2\n2014-07-31,2014,7,100.4,100.5,102.2,101.5,101.5,1075.1,90.5,99.1,1034.0,1158.2,98.4,122.0,114.8\n2014-08-31,2014,8,100.5,100.2,99.8,100.0,101.3,1168.5,107.1,98.4,1061.8,1202.0,84.0,90.9,111.8\n2014-09-30,2014,9,100.6,100.7,102.7,102.8,101.5,1204.0,103.3,98.1,1044.3,1197.0,123.4,111.4,111.8\n2014-10-31,2014,10,100.6,100.8,105.1,102.9,101.7,1468.5,121.6,99.2,1084.6,1226.3,100.7,109.8,111.6\n2014-11-30,2014,11,100.6,101.3,99.8,99.6,101.5,1372.5,92.7,92.2,1097.9,1245.7,112.3,95.5,110.1\n2014-12-31,2014,12,102.3,102.6,108.1,103.9,101.7,2433.3,173.8,98.9,1362.4,1592.4,141.6,91.0,108.5\n'

def test_folder_level_import_and_df_testing():
    get_testable_files()
    folder = os.path.dirname(os.path.realpath(__file__))
    rs = init_rowsystem_from_folder(folder)
    dfa = get_annual_df(rs)
    dfq = get_qtr_df(rs)
    dfm = get_monthly_df(rs)
    assert dfa_csv == dfa.to_csv()
    assert dfq_csv == dfq.to_csv()
    assert dfm_csv == dfm.to_csv()
    remove_testable_files()

from rowsystem import collect_head_labels
    
def test_full_import():
   #TODO: get labels from spec, used in import check =  all must be imported 
   #labels_in_spec,  = get_target_and_actual_varnames_by_file(spec_path, cfg_path)
   #assert labels_in_spec ==

   get_testable_files()
   folder = os.path.dirname(os.path.realpath(__file__))
   rs = init_rowsystem_from_folder(folder)
   
   labels_in_db = collect_head_labels(rs)
   assert labels_in_db == ['CPI', 'CPI_NONFOOD', 'IND_PROD', 'INVESTMENT', 'SALES_FOOD', 'SALES_NONFOOD', 'TRANS']
