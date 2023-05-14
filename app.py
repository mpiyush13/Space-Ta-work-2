from flask import Flask, request, render_template
import gspread
import re
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
        # findin= request.form['find']
        PIs='off'
        Lab='off'
        print(f'Before the value of PIS is {PIs}')
        print(f'Before the value of Lab is {Lab}')
        if 'PIs' in request.form:
            PIs = request.form.get('PIs')
            print(f'the value of PIS is: {PIs}')
        
        if 'Lab' in request.form:
            Lab= request.form.get('Lab')
            print(f'the value of Lab is: {Lab}')
        print(f'After the value of PIS is {PIs}')
        print(f'After the value of Lab is {Lab}')
        print(f"here is ldap id {LDAP_ID}")
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        
        # print(rows[:5])

        # print('==============================')
        
        df = pd.DataFrame(rows)
        # print(df.head())
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
            # if str(findin)=='PI of Student':
            #     df = pd.DataFrame({'LDAP ID': [LDAP_ID], 'PI of Student': [df.iloc[1, p_col]]})
            # if str(findin)=='Lab Name':
            #     df = pd.DataFrame({'LDAP ID': [LDAP_ID],'Lab Name': [df.columns.tolist()[p_col]]})
            if PIs!='off' and Lab!='off':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID], 'PI of Student': [df.iloc[1, p_col]],'Lab Name': [df.columns.tolist()[p_col]]})
            elif PIs!='off':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID], 'PI of Student': [df.iloc[1, p_col]]})
            elif Lab!='off':
                df = pd.DataFrame({'LDAP ID': [LDAP_ID],'Lab Name': [df.columns.tolist()[p_col]]})
            
            else:
                df = pd.DataFrame({'Student Status': ['Select Something'] })
            data1=df.to_html(index=False,sparsify=False)
            # print(data1)
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
    print('Control come into faculty')
    df = pd.DataFrame([])
    if request.method == "POST":
        LDAP_ID = request.form['ldap_id']
        # findin = request.form['find']
        # StudentType=''
        # if str(findin)=='No of Student':
        #     StudentType= request.form['StudentType']
        
        
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        print("This is Faculty information")
        # print(df.head())
        p_row=-1
        df1 = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]]})
        for i in range(len(df)):
          if str(df.iloc[i, 0])==str(LDAP_ID):
              p_row=i
        print(f"This is value of p_row {p_row}")
        df_json = df.to_json(orient='records')
        if p_row!=-1:
            if 'Noflab' in request.form:
                # PIs = request.form.get('Noflab')
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
                
            # if str(findin)=='No of Student':
            #     if str(StudentType)=="M.tech":
            #         df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]],'No of M.Tech Student': [df.iloc[p_row, 4]]})
            #     if str(StudentType)=="B.Tech":
            #         df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]],'No of B.tech Student': [df.iloc[p_row, 9]]}) 
            #     if str(StudentType)=="MS":
            #         df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]],'No of MS Student': [df.iloc[p_row, 10]]})   
            #     if str(StudentType)=="Phd":
            #         df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]],'No of Phd Student': [df.iloc[p_row, 8]]})
            #     if str(StudentType)=="Total No of Students":
            #         df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]],'Total No of Student': [df.iloc[p_row, 3]]})   
            # if str(findin)=='No of Labs':
            #     print("This is for test purpose")
            #     df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]], 'No of Labs': [df.iloc[p_row, 1]]})
            #     print(df)
            # if str(findin)=='Lab Name':
            #     df = pd.DataFrame({'Faculty Name': [df.iloc[p_row, 0]], 'Lab Name': [df.iloc[p_row, 2]]})
            
            data1=df1.to_html(index=False,sparsify=False)
            print("Here data will print ")
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
    SHEET_NAME2='Room Data'
    df_json=''
    print('HELLO')
    df = pd.DataFrame([])
    if request.method == "POST":
        # LDAP_ID = request.form['ldap_id']
        # findoption = request.form['find']
        gc = gspread.service_account('keys.json')
        spreadsheet = gc.open_by_key(SHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME)
        rows = worksheet.get_all_records()
        worksheet = spreadsheet.worksheet(SHEET_NAME2)
        rows2 = worksheet.get_all_records()
        # print(rows[:5])

        # print('==============================')
        df = pd.DataFrame(rows)
        df2 = pd.DataFrame(rows2)
        print(df.head())
        df_json = df.to_json(orient='records')
        # p_col=-1
        # for col in range(df.shape[1]):
        #        if str(df.iloc[0, col])==str(LDAP_ID):
        #            p_col=col
        # print(f"This is value of p_row{p_col}")
        # if p_col!=-1:
        
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
        df3=pd.DataFrame()   
        for LDAP_ID in Lablist:
            new_column = pd.DataFrame({f'Custodian Name': [df[LDAP_ID][0]]})
            new_column2 = pd.DataFrame({f'Lab Name': [LDAP_ID]})
            df1=pd.DataFrame()
            

            # concatenate the new DataFrame with the empty DataFrame
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
   
            
         
        # if str(findoption)=="No of PI":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]], 'No of PIs': [df[LDAP_ID][2]]})
        # if str(findoption)=="PI Name":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]], 'PI Name': [df[LDAP_ID][1]]})
       
        # if str(findoption)=="No of Total Student":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]],
        #                    'No of Total Student': [df[LDAP_ID][3]]})
        # if str(findoption)=="No of M.Tech Student":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]],'M.Tech Student': [df[LDAP_ID][4]]})
        # if str(findoption)=="No of B.Tech Student":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]],
        #                    'B.Tech Student': [df[LDAP_ID][12]]})
        # if str(findoption)=="No of MS Student":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]],'MS Student': [df[LDAP_ID][8]]})
        # if str(findoption)=="No of Phd Student":
        #     df = pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]],'Phd Student': [df[LDAP_ID][13]]})
            
        # if str(findoption)=="Available Capacity of Lab":
        #     print("xkjvbffkj")
        #     search_result = df2.loc[df2['Room No.'] == str(LDAP_ID)]
        #     difference = search_result.iloc[0][6] - search_result.iloc[0][5]
        #     df=pd.DataFrame({f'Custodian Name of {LDAP_ID}': [df[LDAP_ID][0]],f'Available Capacity ': [difference]})
            
        
        data1=df3.to_html(index=False,sparsify=False)
        # print(data1)
        table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
    .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
    .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
        return render_template('Lab.html', data2=table_with_styles,flag=True)
       
            
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
        end_row = 761

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
        Floor = request.form['floor']
        Bgd = request.form['bgd']
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
        if str(Bgd)=="New CSE":
            newlist=[]
            for l in list:
                if "CC" in l and Floor==str(re.search(r'\d', l).group()):
                    newlist.append(l)
            list=newlist       
            df = pd.DataFrame({f'Vacant {LDAP_ID} ': list});
            print("piyush")
            data1=df.to_html(index=False,sparsify=False)
            print(data1)
            table_with_styles = data1.replace('<table', '<table style="border: 2px solid black;padding: 15px;"') \
            .replace('<th', '<th style="text-align: center;border-collapse: collapse;"') \
           .replace('<td', '<td style="border: 2px solid black;padding: 30px;"')
            return render_template('Room.html', data2=table_with_styles,flag=True)
            return render_template('Room.html', data2=df.to_html(),flag=True);
        if str(Bgd)=="Kresit":
            newlist=[]
            for l in list:
                if "CC" not in l and Floor==str(re.search(r'\d', l).group()):
                    newlist.append(l)
            list=newlist
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