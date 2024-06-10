import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import time
import threading


json_content = {
    "type": "service_account",
    "project_id": "alpha-424216",
    "private_key_id": "d8615e606fc149c3f4f28c187e3f5f8ea414cbf2",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDLJfsbTGKRhBIi\nYBLM1KOrEHXvtY1BkSrJTQANdkt7WdLWL2AoHTuhXNrlDRbnZM5Qpg4ucmj23kmO\ncI1uuXjiHr4xPC421gDJiwFbvpo0Yfg+GUn7d1XpoFKAeKfSCOTuEyHbMGPueCH+\nEu3M57c5YeErAi3s73nfy75lMuUh3gmHgLfWpMzGUG9bzHKXBq6J18EDzoBFWbXC\nB7/d7Uwf7KK2LMZX/23pKr3pedspTRUC3Ymlh3nPXGpJGzv2gTATZWHblNp0ikAu\nqSAfMdqOvFdE1jqHUcxc+9S1dmztPilCt1sevDOOdCQCPhdPMUWbyFdruZCFRcpX\n0ok7MCuzAgMBAAECggEAXDwQ4CqUwEPqJeBf+M78xpDxMxZHncLm3cHPqc0RZV55\nixS0gFIRfmiV3BRO112eDODwJGd+v8NaO0lf9atRNr1Flj4gL3aHofoycjC+e9UV\nbEB4Jive/nVzr+/YJlUyd+OI5id43898g4qdnICCYJPPs4LITkDGoXU0q2bpwK9q\ndAbMG5dn/wR0aNFUSbcKpY9AfpgeVUw+ii7MnGxbOcBpvOfeyZm8yZArIXSl5xtQ\nfqNKHzrnEBFqQPOmARL6K75Y2CbqNE9RjxR/zyHecWEB0oRlr9fyd+3VoShfzqIj\nIMeIBNT0FloW890/o6nunt3iobgWnMN1EHn7e1tcZQKBgQD9/ZIZvkUVG5A9TISr\npJtP+DxThxt3tRZfeMknCeYF2NEt7JHYVFi1DB+1gtxbb1G82Mw6XwvdC3hqWUGk\nD0tvvZ8viYXLJFS7/le6e9LWG83xp1nqtEJitOmWY81dSKL1UsyImusTlOZRwH/9\njCKs8ksWjgS46Hi8GvkBEevgVQKBgQDMwW9jeOVZjNmScjSCQJeCtx56svOlYAOj\ndJTce95/R2yki/2a+VgXgwEJygr82COsFTKPTVKIXMP6r4bwvZCrpFChMF2QMOsI\nee236FSh4rvH9gWWM/Ji5Bcz6/nmQYrUCQQ3luUxciAjOWrBMchnEtElSWpZx5pC\nDXPybZjD5wKBgFwTJnmqnkSOn3V5XccTfzI4XTYyjmSRAzFNCi7aycZo2Tv6vMxd\nl2LaqEwWymdjLZB2T2MBvb0+QULcZI1i9gfmB+Ulx5ji7MzR4V+7L61qmvf1oQUS\nn9ZEm0FnoLUmddzVTUxgTMPmgLA2Rq/Vs2Ra2ZmtlkyqCcq3RHl807OZAoGBAJTD\nKWmtCX0hf2YOAaZsxWecIdHluG17r8kPR6RVftccjouShiQVavJSJOv21jrT0j8R\ne5VwCTm3pE+7PaAlKjn6fPZPjHrZf7m91H/clbi0YdgrH+38Oeutako39W1cS0A4\neM7mnAhrsXvGGJDa2Y5BtqCPkWw/QA0jdw04oVgbAoGAFbBkLgl/qCEHcWxDfhy8\n0yzR2k8IVZJiTYalIvXJzHVN/mv6a6B+Xzmswboh62Lnisam2INUKUZOSuIrodmv\n2xArzcHn/H6WFhTi+IJ0TKAlalalY0waLZQxtY5sx9RsobhTFimiClTrpE4zCFuB\n55pP+aML9WCUEpnTgFKTdvc=\n-----END PRIVATE KEY-----\n",
    "client_email": "alphabot@alpha-424216.iam.gserviceaccount.com",
    "client_id": "100039873888133124879",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/alphabot%40alpha-424216.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Replace 'path/to/credentials.json' with your actual credentials file path
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_content, scope)
client = gspread.authorize(creds)

# Open the Google Sheet by name
sheet = client.open('PenPencil Data').sheet1

def generate_unique_id(existing_ids):
    """Generate a unique ID starting with 'ALPHA' followed by a 10-digit number."""
    while True:
        unique_number = 'ALPHA' + ''.join(random.choices('0123456789', k=10))
        if unique_number not in existing_ids:
            return unique_number

def check_and_update_sheet():
    rows = sheet.get_all_values()
    if len(rows) < 1:
        print("No data in sheet.")
        return

    headers = rows[0]
    if 'Access_Token' not in headers or 'Batch_Id' not in headers or 'Batch Name' not in headers or 'Unique Id' not in headers:
        print("Required columns are missing.")
        return

    access_token_idx = headers.index('Access_Token')
    batch_id_idx = headers.index('Batch_Id')
    batch_name_idx = headers.index('Batch Name')
    unique_id_idx = headers.index('Unique Id')

    existing_ids = {row[unique_id_idx] for row in rows[1:] if len(row) > unique_id_idx and row[unique_id_idx]}

    for idx, row in enumerate(rows[1:], start=2):
        if len(row) > max(access_token_idx, batch_id_idx, batch_name_idx):
            access_token = row[access_token_idx]
            batch_id = row[batch_id_idx]
            batch_name = row[batch_name_idx]
            if access_token and batch_id and batch_name:
                if len(row) <= unique_id_idx or not row[unique_id_idx]:  # Check if the Unique Id column is empty or not present
                    unique_id = generate_unique_id(existing_ids)
                    sheet.update_cell(idx, unique_id_idx + 1, unique_id)  # Update the Unique Id column
                    existing_ids.add(unique_id)  # Add the new ID to the set of existing IDs
                    print(f"Row {idx}: Generated and stored unique ID {unique_id}")
                # else:
                #     print(f"Row {idx}: Unique ID already exists")

def clear_unique_id_column():
    while True:
        try:
            rows = sheet.get_all_values()
            headers = rows[0]
            if 'Unique Id' in headers:
                unique_id_idx = headers.index('Unique Id')
                for idx in range(2, len(rows) + 1):
                    sheet.update_cell(idx, unique_id_idx + 1, '')
                print("Cleared all Unique Ids")
            else:
                print("Unique Id column is missing.")
        except Exception as e:
            print(f"An error occurred while clearing Unique Id column: {e}")
        time.sleep(6 * 60 * 60)  # Sleep for 6 hours

def main_loop(interval=2):
    while True:
        try:
            check_and_update_sheet()
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    # Start the thread to clear Unique Id column every 6 hours
    clear_thread = threading.Thread(target=clear_unique_id_column)
    clear_thread.daemon = True
    clear_thread.start()

    # Run the main loop
    main_loop()
