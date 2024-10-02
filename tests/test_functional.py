from project0.utils import extract_incidents, create_db, get_db_conn
from pypdf import PdfReader
import os
import sqlite3
import pytest

# Tests if any incidents are extracted from the PDF.
def test_empty():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources', 'incidents.pdf')
    
    with open(file_path, 'rb') as file:
        incidents = extract_incidents(file)
        print(incidents)
        
    assert len(incidents) > 0, "No incidents extracted from the PDF"
    
# Tests that each extracted incident has exactly 5 fields. 
def test_extract_rowlen():  
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources', 'incidents.pdf')
    
    with open(file_path, 'rb') as file:
        incidents = extract_incidents(file)
    
    for incident in incidents:
        print(incidents)
        assert len(incident) == 5, "Each incident should have 5 fields"
        
        
# Tests if the 'incidents' table is successfully created in the database.    
def test_db_creation():
    conn = create_db()
    cursor = conn.cursor()
    
    cursor.execute('''
                   SELECT * 
                   FROM incidents;
                   ''')
    rows = cursor.fetchall()
    assert rows is not None, "DB fetch failed (table incidents not created)"
    
# Tests if demo data is inserted correctly into the 'incidents' table.
def test_db_population():
    demo_data = [
        ('9/29/2024 0:01', '2024-00070988', '597 S FLOOD AVE', 'Traffic Stop', 'OK0140200'),
        ('9/29/2024 0:04', '2024-00070989', '400 BUCHANAN AVE', 'Foot Patrol', 'OK0140200')
    ]
    
    conn = get_db_conn()
    cursor = conn.cursor()
    
    cursor.executemany(
                    '''
                    INSERT INTO incidents
                    (incident_time, incident_number, incident_location, nature, incident_ori) 
                    VALUES (?, ?, ?, ?, ?);
                    ''', demo_data)
    
    conn.commit()
    
    cursor.execute('''
                   SELECT * 
                   FROM incidents;
                   ''')
    rows = cursor.fetchall()
    
    assert len(rows) == 2, "Demo data not inserted successfully"
    
        