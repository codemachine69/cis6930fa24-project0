import argparse
import sys
import utils

def main(incidents):
    # Download data
    try:
        incident_data = utils.fetch_incidents(incidents)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit()

    # Extract data
    incidents = utils.extract_incidents(incident_data)
	
    # Create new database
    conn = utils.create_db()
	
    # Insert data
    utils.populate_db(conn, incidents)
	
    # Print incident counts
    utils.status(conn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
    else:
        parser.print_help(sys.stderr)