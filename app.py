from flask import Flask, request, render_template
import gspread
import pandas as pd


app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # SHEET_ID = ''
    SHEET_NAME = 'Student Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    p_row=-1
    p_col=-1
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        findin= request.form['find']
        
        print(f"here is ldap id {LDAP_ID}")
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        
        # print(rows[:5])

        # print('==============================')
        
        df = pd.DataFrame(rows)
        print(df.head())
        for i in range(len(df)):
          if str(df.iloc[i, 0])==str(LDAP_ID):
              p_row=i
        print(f"This is value of p_row{p_row}")
        if p_row!=-1:
            for col in range(df.shape[1]):
               if str(df.iloc[p_row, col])=='1':
                   p_col=col
        print(f"This is value of p_col{p_col}")           
        
        if p_col!=-1:
            if str(findin)=='PI of Student':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID], 'PI of Student': [df.iloc[1, p_col]]})
            if str(findin)=='Lab Name':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID],'Lab Name': [df.columns.tolist()[p_col]]})
            
           
            data1=df.to_html(index=False,sparsify=False)
            print(data1)
            table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 15px;"')
            return render_template('home.html', data2=table_with_styles,flag=True)
        df_json = df.to_json(orient='records')
        if p_col==-1:
            df = pd.DataFrame({'Student Status': ['Student Record Not Found'] })
            return render_template('home.html', data=df.to_html(),flag=False)
            

    return render_template('home.html', data=df.to_html(),flag=1)


@app.route("/faculty", methods = ['GET', 'POST'])
def faculty():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # SHEET_ID = ''
    SHEET_NAME = 'Faculty Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        findin = request.form['find']
        
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        print("This is Faculty information")
        print(df.head())
        p_row=-1
        for i in range(len(df)):
          if str(df.iloc[i, 0])==str(LDAP_ID):
              p_row=i
        print(f"This is value of p_row{p_row}")
        df_json = df.to_json(orient='records')
        if p_row!=-1:
            if str(findin)=='No of Student':
                df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]],'No of Student': [df.iloc[p_row, 3]]})
            if str(findin)=='No of Labs':
                df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]], 'No of Labs': [df.iloc[p_row, 1]]})
            if str(findin)=='Lab Name':
                df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]], 'Lab Name': [df.iloc[p_row, 2]]})
            
            data1=df.to_html(index=False,sparsify=False)
            print(data1)
            table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
            return render_template('Faculty.html', data2=table_with_styles,flag=True)
            # return render_template('home.html', data2=df.to_html(),flag=True)
    return render_template('Faculty.html', data=df.to_html(),flag=1)

@app.route("/lab", methods = ['GET', 'POST'])
def lab():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # SHEET_ID = ''
    SHEET_NAME = 'Student Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        print(df.head())
        df_json = df.to_json(orient='records')
        # p_col=-1
        # for col in range(df.shape[1]):
        #        if str(df.iloc[0, col])==str(LDAP_ID):
        #            p_col=col
        # print(f"This is value of p_row{p_col}")
        # if p_col!=-1:
        
        df = pd.DataFrame({'Custodian Name': [df[LDAP_ID][0]], 'No of PIs': [df[LDAP_ID][2]], 'PI Name': [df[LDAP_ID][1]],
                           'No of Student': [df[LDAP_ID][3]],'M.Tech Student': [df[LDAP_ID][4]],'MS Student': [df[LDAP_ID][8]],
                           'B.Tech Student': [df[LDAP_ID][12]],'Phd Student': [df[LDAP_ID][13]]})
        data1=df.to_html(index=False,sparsify=False)
        print(data1)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
        return render_template('Lab.html', data2=table_with_styles,flag=True)
        return render_template('Lab.html', data2=df.to_html(),flag=True)
            
    return render_template('Lab.html', data=df.to_html(),Flag=1)
@app.route("/custodian", methods = ['GET', 'POST'])
def custodian():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # SHEET_ID = ''
    SHEET_NAME = 'Student Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        
        print(df.head())
        df_json = df.to_json(orient='records')

    return render_template('Custodian.html', data=df.to_html())
@app.route("/status", methods = ['GET', 'POST'])
def status():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # SHEET_ID = ''
    SHEET_NAME = 'Student Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    if request.method == "POST":
        
        
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        start_row = 17
        end_row = 500

# Filter the DataFrame to include only the rows in the specified range with sum of second column onwards >= 1
        filtered_df = df.iloc[start_row:end_row+1][(df.iloc[start_row:end_row+1].iloc[:,1:].sum(axis=1)) >= 1]

# Output the values of the first column for each row in the filtered DataFrame
        list=[]
        for index, row in filtered_df.iterrows():
          list.append(row[0])
        df = pd.DataFrame({'Student Status': list })
        data1=df.to_html(index=False,sparsify=False)
        print(data1)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 15px;"')
        return render_template('status.html', data2=table_with_styles,flag=True)
        df_json = df.to_json(orient='records')
        if p_col==-1:
            df = pd.DataFrame({'Student Status': ['Student Record Not Found'] })
            return render_template('home.html', data=df.to_html(),flag=False)
         
        

# select first column if sum of values from second column to last column is greater than 0, starting from start_row
#         selected_col = []
#         for index, row in df.iterrows():
#           if index >= start_row and row.iloc[1:].sum() > 0:
#             selected_col.append(row.iloc[0])

# # add selected column as a new column to the dataframe
#         df['selected_col'] = selected_col
#         print(selected_col)
            # return render_template('home.html', data2=df.to_html(),flag=True)
    return render_template('Status.html', data2=df.to_html(),flag=1)
@app.route("/room", methods = ['GET', 'POST'])
def room():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # SHEET_ID = ''
    SHEET_NAME = 'Room Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        
        print(df.head())
        df_json = df.to_json(orient='records')
        rows = df[(df.iloc[:, 2] == str(LDAP_ID)) & (df.iloc[:, 4].isin(['N/A', 'Vacant']))]

        # row = df[df.iloc[:, 2] == ]
        # if not row.empty and row.iloc[0, 4] in ['N/A', 'Vacant']:
        #     print(row.iloc[0, 0])
        list=[]
        for i, row in rows.iterrows():
          list.append(row.iloc[0])
        print(list)
        df = pd.DataFrame({f'Vacant {LDAP_ID} ': list});
        print("piyush")
        data1=df.to_html(index=False,sparsify=False)
        print(data1)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
        return render_template('Room.html', data2=table_with_styles,flag=True)
        return render_template('Room.html', data2=df.to_html(),flag=True);
        
        # column=df['Space Type']
        # list=[]
        # for col in len(column):
        #     if str(column[col])==str(LDAP_ID) and (str(df.iloc[col, 4])=="NA" or str(df.iloc[col, 4])=="vacant") :
        #         list.append(df.iloc[col, 4])
        # print(list)       
        print("piyush")     
        

    return render_template('Room.html', data2=df.to_html(),flag=True)
if __name__ == '__main__':
    app.run(host='localhost', port=8000)