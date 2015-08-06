# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import doc_to_database, make_readable_csv, csv_to_database
from word import wipe_db_tables, change_extension
from word import get_raw_csv_filename, get_labelled_csv_filename
from word import yield_row_with_labels, yield_csv_rows
from word import load_spec, dump_iter_to_csv

import os

src_doc = ["../data/1-07/1-07.doc", "../data/ind06/tab.doc", "../data/minitab/minitab.doc"] 

def batch1():
    print("\n### Trial 1")
    p = os.path.abspath("../data/1-07/1-07.doc")
    #c = dump_doc_to_single_csv_file(p)
    #label_dict, sec_label_dict, reader_dict = load_spec(p)
    #t = make_labelled_csv(c, label_dict, sec_label_dict)
    #csv_to_database(t)
    doc_to_database(p)    

def batch2():
    print("\n### Trial 2")
    p = os.path.abspath("../data/minitab/minitab.doc")
    c = change_extension(p, ".csv")
    r = make_readable_csv(c)
    #r = change_extension(p, ".txt")
    #csv_to_database(r)
    
def batch3():
    print("\n### Trial 3")
    c = os.path.abspath("../data/ind06/all_tab.csv") #all_tab got.csv
    r = make_readable_csv(c)
    csv_to_database(r)
    
def batch4():
    
    from word import dump_labelled_rows_to_csv, check_vars_not_in_labelled_csv, csv_to_database
    import os    
    
        
    f = os.path.abspath("../data/ind06/all_tab.csv") #all_tab got.csv
    r = dump_labelled_rows_to_csv(f)
    print("Written to:   \n", r)
    check_vars_not_in_labelled_csv(f)
    csv_to_database(r)
    
    
if __name__ == "__main__":
    wipe_db_tables()   
    batch4()
    import query
    