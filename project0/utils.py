import urllib.request
from pypdf import PdfReader
import os
import sqlite3
import re
import io

# Fetches the PDF data from the given URL and returns it as a byte stream.
def fetch_incidents(url):
    headers = {'User-Agent': "Mozilla/5.0"}
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read() 
    data = io.BytesIO(data)
    return data

# Extracts and parses incidents from the PDF data using pypdf. 
def extract_incidents(incident_data):
    incidents = []
    pdfreader = PdfReader(incident_data)
    
    for page in pdfreader.pages:
        text = page.extract_text(extraction_mode="layout")
        rows = text.split('\n')
        
        for row in rows:
            row = row.strip() # Strippping any excess spaces.
            
            if 'Date / Time' in row or 'Daily Incident' in row or 'NORMAN POLICE DEPARTMENT'in row: # Skipping over headers
                continue
            
            if len(row) == 0:  # Removing blank rows
                continue
            
            columns = re.split(r'\s{2,}', row) # Split columns if separated by 2 or more spaces.
            
            # Incomplete record, ignore it
            if len(columns) != 5:
                # print(f"Record doesn't have 5 columns:\n{row}\nParsed columns: {columns}\n")
                continue
            incidents.append(tuple(columns))
    # for incident in incidents:
    #     print(incident)
    return incidents

# Creates a new SQLite database and 'incidents' table.
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

# Establishes and returns a connection to the SQLite database.
def get_db_conn():
    curr_path = os.getcwd()
    db_path = os.path.join(curr_path, 'resources', 'normanpd.db')
    conn = sqlite3.connect(db_path)
    return conn

# Inserts extracted incident data into the 'incidents' table in the database.
def populate_db(conn, incidents):
    cursor = conn.cursor()
    
    cursor.executemany(
                    '''
                    INSERT INTO incidents
                    (incident_time, incident_number, incident_location, nature, incident_ori) 
                    VALUES (?, ?, ?, ?, ?);
                    ''', incidents)

    conn.commit()
    
# Queries and prints the count of incidents grouped by their nature.    
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