from flask import Flask, request, render_template
import gspread
import re
import pandas as pd


app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
    # This is master sheet id
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    SHEET_NAME = 'Student Data'
    # Here we are accessing the Sutudent Data sheet which is present in master sheet.
    df_json=''
    # make the dataframe as df
    df = pd.DataFrame([])
    # make these two variable to check some condition.
    p_row=-1
    p_col=-1
    if request.method == "POST":
        # Here i am taking the value from frontend whose input tag name is ldap_id
        LDAP_ID = request.form['ldap_id']
        # Making the variable to check ,checkbox is selected or not
        PIs='off'
        Lab='off'
        # Here we are checking home.html file
        if 'PIs' in request.form:
            PIs = request.form.get('PIs')
        if 'Lab' in request.form:
            Lab= request.form.get('Lab')
        gc = gspread.service_account('keys.json')
        # Here we are taking data from dpreadsheet
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # make all the selected rows to dataframe
        df = pd.DataFrame(rows)
        # Here we are searching row number of particular Ldap id
        for i in range(len(df)):
          if str(df.iloc[i, 0])==str(LDAP_ID):
              p_row=i
        if p_row!=-1:
            # Here we are finding the column value where that row contain 1
            for col in range(df.shape[1]):
               if str(df.iloc[p_row, col])=='1':
                   p_col=col         
        if p_col!=-1:
            if PIs!='off' and Lab!='off':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID], 'PI of Student': [df.iloc[1, p_col]],'Lab Name': [df.columns.tolist()[p_col]]})
            elif PIs!='off':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID], 'PI of Student': [df.iloc[1, p_col]]})
            elif Lab!='off':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID],'Lab Name': [df.columns.tolist()[p_col]]})
            
            else:
                df = pd.DataFrame({'Student Status': ['Select Something'] })
            # Make the dataframe to html table
            data1=df.to_html(index=False,sparsify=False)
            # Give some style to table
            table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 15px;"')
            # Flag variable is used by frontend to show to show the data.
            return render_template('home.html', data2=table_with_styles,flag=True)
        df_json = df.to_json(orient='records')
        if p_col==-1:
            df = pd.DataFrame({'Student Status': ['Student Record Not Found'] })
            return render_template('home.html', data=df.to_html(),flag=False)
            
    
    return render_template('home.html', data=df.to_html(),flag=1)


@app.route("/faculty", methods = ['GET', 'POST'])
def faculty():
    # This is master sheet id
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    SHEET_NAME = 'Faculty Data'
    # Here we are accessing the Faculty sheet which is present in master sheet.
    df_json=''
    df = pd.DataFrame([])
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        df = pd.DataFrame(rows)
        p_row=-1
        # df1 is dataframe 
        df1 = pd.DataFrame({'Faculty Name': [LDAP_ID]})
        # we are finding the row for particular faculty name. 
        for i in range(len(df)):
          if str(df.iloc[i, 0])==str(LDAP_ID):
              p_row=i
        df_json = df.to_json(orient='records')
        if p_row!=-1:
            # Check if that particular name checkbox is selected or not.
            # Here we are checking in Faculty.html file
            if 'Noflab' in request.form:
                   newdf=pd.DataFrame({ 'No of Labs': [df.iloc[p_row, 1]]})
                   df1 = pd.concat([df1, newdf], axis=1)
            if 'labname' in request.form:
                   newdf=pd.DataFrame({'Lab Name': [df.iloc[p_row, 2]]})
                   df1 = pd.concat([df1, newdf], axis=1)
            if 'NofStudent' in request.form:
                   if 'M.tech' in request.form:
                       newdf=pd.DataFrame({'No of M.Tech Student': [df.iloc[p_row, 4]]})
                       df1 = pd.concat([df1, newdf], axis=1)
                       
                   if 'B.Tech' in request.form:
                       newdf=pd.DataFrame({ 'No of B.tech Student': [df.iloc[p_row, 9]]})
                       df1 = pd.concat([df1, newdf], axis=1)
                   if 'MS' in request.form:
                       newdf=pd.DataFrame({ 'No of MS Student': [df.iloc[p_row, 10]]})
                       df1 = pd.concat([df1, newdf], axis=1)
                   if 'Phd' in request.form:
                       newdf=pd.DataFrame({ 'No of Phd Student': [df.iloc[p_row, 8]]})
                       df1 = pd.concat([df1, newdf], axis=1)
                   if 'TotalStudent' in request.form:
                       newdf=pd.DataFrame({ 'Total No of Student': [df.iloc[p_row, 3]]})
                       df1 = pd.concat([df1, newdf], axis=1)
            # Make the dataframe to html table
            data1=df1.to_html(index=False,sparsify=False)
            # Give some style to table
            table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
            return render_template('Faculty.html', data2=table_with_styles,flag=True)
            # return render_template('home.html', data2=df.to_html(),flag=True)
    return render_template('Faculty.html', data=df.to_html(),flag=1)

@app.route("/lab", methods = ['GET', 'POST'])
def lab():
    # This is master sheet id
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    # Here we are accessing two sheet data which is present in master sheet.
    SHEET_NAME = 'Student Data'
    SHEET_NAME2='Room Data'
    df_json=''
    df = pd.DataFrame([])
    if request.method == "POST":
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        worksheet = spreadsheet.worksheet(SHEET_NAME2)
        rows2 = worksheet.get_all_records()
        
        df = pd.DataFrame(rows)
        df2 = pd.DataFrame(rows2)
        # The df3 dataframe will use in between the code
        df3=pd.DataFrame()
       
        df_json = df.to_json(orient='records')
        # Make the list of all lab which are selected 
        Lablist=[]
        if 'CC 402' in request.form:
            Lablist.append('CC 402')
        if 'CC 117' in request.form:
            Lablist.append('CC 117')
        if 'CC 301' in request.form:
            Lablist.append('CC 301')
        if 'CC 316' in request.form:
            Lablist.append('CC 316')   
        if 'CC 218' in request.form:
            Lablist.append('CC 218')   
        if 'CC 405' in request.form:
            Lablist.append('CC 405')
        if 'CFILT' in request.form:
            Lablist.append('CFILT')  
        if 'SIA 20' in request.form:
            Lablist.append('SIA 20') 
        if 'SIB 401' in request.form:
            Lablist.append('SIB 401')
        if 'SIA 20' in request.form:
            Lablist.append('SIA 20')
        if 'SIC101/SIC102' in request.form:
            Lablist.append('SIC101/SIC102') 
        if 'SIC 210' in request.form:
            Lablist.append('SIC 210')
        if 'SIC 204' in request.form:
            Lablist.append('SIC 204')
        if 'SIC 212' in request.form:
            Lablist.append('SIC 212')
        if 'SIC 312' in request.form:
            Lablist.append('SIC 312')
        if 'SIC 209' in request.form:
            Lablist.append('SIC 209')
        if 'SIC 309' in request.form:
            Lablist.append('SIC 309')
        if 'SIC 310' in request.form:
            Lablist.append('SIC 310')
        if 'SIC 313' in request.form:
            Lablist.append('SIC 313')    
        
        # Itereate all the selected lab    
        for LDAP_ID in Lablist:
            new_column = pd.DataFrame({f'Custodian Name': [df[LDAP_ID][0]]})
            new_column2 = pd.DataFrame({f'Lab Name': [LDAP_ID]})
            df1=pd.DataFrame()
            # concatenate one DataFrame to other DataFrame
            df1 = pd.concat([df1, new_column], axis=1)
            df1 = pd.concat([df1, new_column2], axis=1)
            if 'No of PI' in request.form:
                new_column = pd.DataFrame({'No of PIs': [df[LDAP_ID][2]]})
                df1 = pd.concat([df1, new_column], axis=1)
            if 'PI Name' in request.form:
                new_column = pd.DataFrame({'PI Name': [df[LDAP_ID][1]]})
                df1 = pd.concat([df1, new_column], axis=1)
                
            if 'No of Total Student' in request.form:
                new_column = pd.DataFrame({'No of Total Student': [df[LDAP_ID][3]]})
                df1 = pd.concat([df1, new_column], axis=1)
            if 'No of M.Tech Student' in request.form:
                new_column = pd.DataFrame({'M.Tech Student': [df[LDAP_ID][4]]})
                df1 = pd.concat([df1, new_column], axis=1)
            if 'No of B.Tech Student' in request.form:
                new_column = pd.DataFrame({'B.Tech Student': [df[LDAP_ID][12]]})
                df1 = pd.concat([df1, new_column], axis=1)
            if 'No of MS Student' in request.form:
                new_column = pd.DataFrame({'MS Student': [df[LDAP_ID][8]]})
                df1 = pd.concat([df1, new_column], axis=1)
            if 'No of Phd Student' in request.form:
                new_column = pd.DataFrame({'Phd Student': [df[LDAP_ID][13]]})
                df1 = pd.concat([df1, new_column], axis=1)
            if 'Available Capacity of Lab' in request.form:
                search_result = df2.loc[df2['Room No.'] == str(LDAP_ID)]
                difference = search_result.iloc[0][6] - search_result.iloc[0][5]
                new_column = pd.DataFrame({f'Available Capacity ': [difference]})
                df1 = pd.concat([df1, new_column], axis=1)
            df3 = pd.concat([df1, df3], axis=0, ignore_index=True)
        
        data1=df3.to_html(index=False,sparsify=False)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
        return render_template('Lab.html', data2=table_with_styles,flag=True)
       
            
    return render_template('Lab.html', data=df.to_html(),Flag=1)
@app.route("/status", methods = ['GET', 'POST'])
def status():
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    SHEET_NAME = 'Student Data'
    df_json=''
    df = pd.DataFrame([])
    if request.method == "POST": 
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        df = pd.DataFrame(rows)
        # We are just go through the student data sheet data from row 17 to row 761 to find in which row the entire value is zero,that means that student did not feel the form
        start_row = 17
        end_row = 761
        filtered_df = df.iloc[start_row:end_row+1][(df.iloc[start_row:end_row+1].iloc[:,1:].sum(axis=1)) >= 1]
        list=[]
        for index, row in filtered_df.iterrows():
          list.append(row[0])
        df = pd.DataFrame({'Student Status': list })
        data1=df.to_html(index=False,sparsify=False)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 15px;"')
        return render_template('status.html', data2=table_with_styles,flag=True)
    return render_template('Status.html', data2=df.to_html(),flag=1)
@app.route("/room", methods = ['GET', 'POST'])
def room():
    # Accessing the Room Data sheet from master sheet
    SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
    SHEET_NAME = 'Room Data'
    df_json=''
    df = pd.DataFrame([])
    if request.method == "POST":
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        df = pd.DataFrame(rows)
        # Make empty dataframe which is used in between the code
        finaldf = pd.DataFrame([])
        finaldf2 = pd.DataFrame([])
        finaldf3 = pd.DataFrame([])
        df_json = df.to_json(orient='records')
        # Here we are checking which room type is selected ,if selected take all room from sheet. 
        if 'Seminar Hall' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Seminar Hall":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)        
        if 'Teaching Lab' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Teaching Lab":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Seminar Room' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Seminar Room":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Classroom' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Classroom":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)    
        if 'PG first year Lab' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "PG first year Lab":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Faculty room' in request.form:
            print("Enter in Faculty hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Faculty Room":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'RS Room' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "RS Room":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Meeting room' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Meeting room":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Storage' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Storage":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Research lab' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Seminar Hall":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Department Office' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Department Office":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        if 'Lecture Hall' in request.form:
            print("Enter in seminar hall")
            classifications = {
                "seminar": []
            }
            for index, row in df.iterrows():
               value = row.iloc[1]  # Value in the second column
               if str(value) == "Lecture Hall":
                   classifications["seminar"].append(row)  
            seminar_df = pd.DataFrame(classifications["seminar"])
            finaldf = finaldf.append(seminar_df, ignore_index=True)
        # Here we are just replacing the df to finaldf
        df=finaldf
        # Here we are checking which building is selected
        if 'New CSE' in request.form:
            # We are filtering data from df by just checking if room number start with 'CC' then that room belong into new cse otherwise belong to kresit.
            new_df = df[df.iloc[:, 0].str.contains('CC')]
            finaldf2 = finaldf2.append(new_df, ignore_index=True)
        if 'Kresit' in request.form:
            new_df = df[~df.iloc[:, 0].str.contains('CC')]
            finaldf2 = finaldf2.append(new_df, ignore_index=True)
        # Here we are just replacing the df to finaldf2
        df=finaldf2
        # If df is empty the return 
        if df.empty:
            return render_template('Room.html', data2=df.to_html(),flag=True)
        # Here we are finding which floor is selected
        if 'floorB' in request.form:
            # Here we just check if room ending of room number string is 'B' then that room is selected.
            selected_rows = df[df.iloc[:, 0].astype(str).str.extract(r'(\D)(\d*)$')[0] == 'B']
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
        if 'floorG' in request.form:
            # Here we just check if room ending of room number string is 'G' then that room is selected.
            selected_rows = df[df.iloc[:, 0].astype(str).str.extract(r'(\D)(\d*)$')[0] == 'G']
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
        if 'floor1' in request.form:
             # Here we just checking, starting number digit is 1,then that room will select.
            selected_rows = df[df.iloc[:, 0].astype(str).apply(lambda x: re.search(r'\b1', x) is not None)]
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
        if 'floor2' in request.form:
            # Here we just checking, starting number digit is 2,then that room will select.
            selected_rows = df[df.iloc[:, 0].astype(str).apply(lambda x: re.search(r'\b2', x) is not None)]
            print("selected row:::")
            print(selected_rows)
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
            print(finaldf3)
        if 'floor3' in request.form:
            # Here we just checking, starting number digit is 3,then that room will select.
            selected_rows = df[df.iloc[:, 0].astype(str).apply(lambda x: re.search(r'\b3', x) is not None)]
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
        if 'floor4' in request.form:
            # Here we just checking, starting number digit is 4,then that room will select.
            selected_rows = df[df.iloc[:, 0].astype(str).apply(lambda x: re.search(r'\b4', x) is not None)]
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
        if 'floor5' in request.form:
            # Here we just checking, starting number digit is 5,then that room will select.
            selected_rows = df[df.iloc[:, 0].astype(str).apply(lambda x: re.search(r'\b5', x) is not None)]
            finaldf3 = finaldf3.append(selected_rows, ignore_index=True)
        df=finaldf3
        if df.empty:
            return render_template('Room.html', data2="<h1> Data Not found </h1>",flag=True)
        # Here we are filering if selected room till now is either "vacant" or "N/A" then only that type of room will select
        selected_rows = df[(df.iloc[:, 4] == "vacant") | (df.iloc[:, 4] == "N/A")]
        df=selected_rows
        # Select particular column from dataframe df
        selected_columns = df[['Room No.', 'Common Name']]
        df=selected_columns
        # Convert dataframe to html table
        data1=df.to_html(index=False,sparsify=False)
        # print(data1)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
            .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
           .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
        return render_template('Room.html', data2=table_with_styles,flag=True)
        

    return render_template('Room.html', data2=df.to_html(),flag=True)
if __name__ == '__main__':
    app.run(host='localhost', port=8000)