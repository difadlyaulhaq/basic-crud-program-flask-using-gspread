from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import HttpAccessTokenRefreshError
import sys

app = Flask(__name__, template_folder="templates")

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

creds = ServiceAccountCredentials.from_json_keyfile_name("sigma-cairn-405214-700ce76cf826.json", scope)
client = gspread.authorize(creds)

sheet = client.open("test_flask").sheet1

# sheets = client.open("test_flask").sheet1

@app.route('/')
def index():
    try:
        data = sheet.get_all_records()
        mapped_data = []

        for row in data:
            mapped_row = {
                'ID': row.get('ID', ''),  
                'Name': row.get('Name', ''),  
                'Age': row.get('Age', '')  
            }
            mapped_data.append(mapped_row)
    
        # print(mapped_data, file=sys.stderr)

        
        return render_template("test.html", data=mapped_data)
    except HttpAccessTokenRefreshError as e:
        return f"Access Token Refresh Error: {e}", 500

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        new_row = [request.form['ID'], 
        request.form['Name'], 
        request.form['Age']]  # Adjust according to your columns
        sheet.append_row(new_row)
        return redirect(url_for('index'))

@app.route('/delete/<int:ID>', methods=['POST'])
def delete(ID):
    sheet.delete_row(ID+1)
    return redirect(url_for('index'))

@app.route('/update/<int:row_id>', methods=['POST'])
def update(row_id):
    if request.method == 'POST':
        updated_row = [request.form['col1'], request.form['col2'], request.form['col3']]  # Adjust according to your columns
        sheet.update_row(row_id, updated_row)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
