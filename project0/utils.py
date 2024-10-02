import urllib.request
from pypdf import PdfReader
import os
import sqlite3
import re
import io

def fetch_incidents(url):
    headers = {'User-Agent': "Mozilla/5.0"}
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read() 
    data = io.BytesIO(data)
    return data

    
def extract_incidents(incident_data):
    incidents = []
    pdfreader = PdfReader(incident_data)
    
    for page in pdfreader.pages:
        text = page.extract_text()
        rows = text.split('\n')
        overflow = ''
        for row in rows:
            #print("LINE: "+row)
            if row.startswith('Date / Time'):
                continue
            
            if row[0].isdigit() and not (row.endswith('EMSSTAT') or row.endswith('OK0140200') or row.endswith('14005') or row.endswith('COMMAND') or row.endswith('14009')):
                overflow = row
                continue
                
            row = overflow + row
            
            # pattern = r'^(\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2})\s+(\d{4}-\d{8})\s+((?:\d+\s+)?[A-Z0-9 /\-;.,]+?)(?:\s+(?=911\s)|(?=\sMVA)|(?=\s[A-Z][a-z])|(?=\sCOP))\s*([A-Za-z0-9/\s]+)\s+([A-Z0-9]+)$' working
            
            pattern = r'^(\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2})\s+(\d{4}-\d{8})\s+((?:\d+\s+)?[A-Z0-9 /\-;.,]+?)(?:\s+(?=911\s)|(?=\sMVA)|(?=[A-Z][a-z])|(?=\sCOP))\s*([A-Za-z0-9/\s]+)\s+([A-Z0-9]+)$'
            
            # Separating incident number and location
            row = re.sub(r'(\d{4}-\d{8})(?=\S)', r'\1 ', row)
            
            # Inserting a space before any uppercase letter followed by lowercase letters if the previous character is uppercase or a symbol
            row = re.sub(r'(?<=[A-Z0-9/])(?=[A-Z][a-z])', ' ', row)
            row = row.replace("NORMAN POLICE DEPARTMENT Daily Incident Summary (Public)", "")
         
            match = re.search(pattern, row.strip())
            if match:
                incidents.append((match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)))
            # else:
            #     print('RPLOG : ' + row)
                
            # Resetting extra line variable    
            overflow = ''
    
    return incidents

def create_db():    
    curr_path = os.getcwd()
    db_path = os.path.join(curr_path, 'resources', 'normanpd.db')
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
                '''
                CREATE TABLE incidents (
                    incident_time TEXT,
                    incident_number TEXT,
                    incident_location TEXT,
                    nature TEXT,
                    incident_ori TEXT
                );
                ''')
    
    conn.commit()
    
    return conn

def get_db_conn():
    curr_path = os.getcwd()
    db_path = os.path.join(curr_path, 'resources', 'normanpd.db')
    
    conn = sqlite3.connect(db_path)
    return conn


def populate_db(conn, incidents):
    cursor = conn.cursor()
    
    cursor.executemany(
                    '''
                    INSERT INTO incidents
                    (incident_time, incident_number, incident_location, nature, incident_ori) 
                    VALUES (?, ?, ?, ?, ?);
                    ''', incidents)

    conn.commit()
    
def status(conn):
    cursor = conn.cursor()
    
    cursor.execute(
                '''
                SELECT nature, COUNT(*) 
                FROM incidents
                GROUP BY nature 
                ORDER BY nature ASC;
                ''')
    
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}|{row[1]}")