from project0.utils import extract_incidents
from pypdf import PdfReader
import os
import sqlite3
import pytest

def test_empty():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources', 'incidents.pdf')
    
    with open(file_path, 'rb') as file:
        incidents = extract_incidents(file)
        print(incidents)
        
    assert len(incidents) > 0, "No incidents extracted from the PDF"
    
 
def test_rowlen():  
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources', 'incidents.pdf')
    
    with open(file_path, 'rb') as file:
        incidents = extract_incidents(file)
    
    for incident in incidents:
        print(incidents)
        assert len(incident) == 5, "Each incident should have 5 fields"
        
        
def test_db_creation():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(curr_dir, '..', 'resources', 'incidents.db')
    
    assert os.path.exists(db_path) == True, "Database file is missing"
    
def test_db_data():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(curr_dir, '..', 'resources', 'incidents.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
                '''
                SELECT nature, COUNT(*) 
                FROM incidents
                GROUP BY nature 
                ORDER BY nature ASC;
                ''')
    
    rows = cursor.fetchall()
    
    assert len(rows) > 0, "Database is empty"
    
    