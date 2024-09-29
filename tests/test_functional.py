from project0.utils import extract_incidents
from pypdf import PdfReader
import os

def test_empty():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources', 'incidents.pdf')
    
    with open(file_path, 'rb') as file:
        # reader = PdfReader(file)
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
        
        
