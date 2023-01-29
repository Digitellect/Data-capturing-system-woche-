import pandas as pd
import streamlit as st
import plotly.express as xp
import plotly.graph_objects as go
import sqlite3


st.title("APP for SMSE")
conn = sqlite3.connect("user.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, password TEXT)''')
conn.commit()
account = st.selectbox("Create Account or Log in",["Log in","Create Account"])
if account == "Log in" :
    username = st.text_input("Input Username", "Name")
    password = st.text_input("Input password", "password")
    cursor.execute('''SELECT * FROM user WHERE username = ? and password = ?''',(username,password))
    auth = cursor.fetchone()
    if auth :
        usernamedb = f"{username}.db"
        conn = sqlite3.connect(usernamedb)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        result = cursor.fetchall()
        if result :
            tabs = st.selectbox("Select prefered Table",[x[0] for x in result])
            data_op = st.selectbox("Select Data Operation",["Create Table","Add Values"])
            process = st.selectbox("Select operation to perform",["Convert column","Arithmetic Operations"])
            cols_opp = st.button("Submit for ops")
            if cols_opp :
                if process == "Convert column":
                        data = pd.read_sql_query(f'SELECT * FROM {tabs}', conn, index_col= None)
                        column = st.selectbox("Select Column here",[i for i in data.columns])
                        dtypes = st.selectbox("Select data types here",["int","float","object","bool","date"])
                        def Convert_cols(columns,dtype):
                            if dtypes == "date":
                                data[column] = pd.to_datetime(data[column])
                                return data
                            else :
                                data[column] = data[column].astype(dtype)
                                return data
                        df = Convert_cols(column,dtypes)
                elif process == "Arithmetic Operations" :
                    op_type = st.radio("Select Operation type",["Binary","Unary"])
                    type_button = st.button("Operation Type")
                    if type_button :
                        if op_type == "Binary":
                            def Binary_op():
                                st.write("It got here")
                                df = pd.read_sql_query(f'SELECT * FROM {tabs}', conn, index_col= None)
                                col_name = st.text_input("Input the name for the column","column")
                                col_1 = st.selectbox("select first column for the operation",[i for i in df.columns])
                                col_2 = st.radio("Select second column for the operation:", [i for i in df.columns])
                                operator = st.selectbox("Select operation to perform",["+","-","*","/","**"])
                                choice = st.selectbox("Select an option:", ['True','False'])
                                if operator == "+":
                                    df[col_name] = df[col_1] + df[col_2]
                                    st.write(df)
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "-":
                                    df[col_name] = df[col_1] - df[col_2]
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "*":
                                    df[col_name] = df[col_1] * df[col_2]
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "/":
                                    df[col_name] = df[col_1] / df[col_2]
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "**":
                                    df[col_name] = df[col_1]** df[col_2]
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                            Binary_op()
                        elif op_type == "Unary" :
                            def Unary_op():
                                df = pd.read_sql_query(f'SELECT * FROM {tabs}', conn, index_col= None)
                                col_name = st.text_input("Input the name for the column","column")
                                col = st.selectbox("select the column for the operation",[i for i in df.columns])
                                num = st.number_input("Input Number",0)
                                operator = st.selectbox("Select operation to perform",["+","-","*","/","**"])
                                choice = st.selectbox("Select an option:", ['True','False'])
                                if operator == "+":
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                                    df[col] = df[col].fillna(0)
                                    df[col_name] = df[col] + num
                                    st.write(df)
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "-":
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                                    df[col_name] = df[col].fillna(0)
                                    df[col_name] = df[col] - num
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "*":
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                                    df[col_name] = df[col].fillna(1)
                                    df[col_name] = df[col] * num
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "/":
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                                    df[col_name] = df[col].fillna(1)
                                    df[col_name] = df[col] / num
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                elif operator == "**":
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                                    df[col_name] = df[col].fillna(0)
                                    df[col_name] = df[col]** num
                                    if choice == 'True' :
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                                    else :
                                        df.drop(col_name,axis=1,inplace=True)
                                        df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                                        return df
                            Unary_op()
            if data_op == "Add Values": 
                def Add_values():
                    values = st.text_input("Input the values")
                    values = values.split(",")
                    if values == [] :
                        st.write("No Value Was Added")
                    else :
                        submit = st.button("Submit")
                        if submit :
                            data = pd.read_sql_query(f'SELECT * FROM {tabs}', conn, index_col= None)
                            print(len(data.columns))
                            print(data.columns)
                            keys = [i for i in data.columns]
                            dic = {key: [value] for key, value in zip(keys, values)}
                            #st.write(dic)
                            df_1 = pd.DataFrame.from_dict(dic)
                            #df_1 = pd.DataFrame([values],columns= data.columns, index= None)
                            print(df_1.columns)
                            data = pd.concat([data,df_1], ignore_index=False)
                            data.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
                            st.write(data)
                data = Add_values()
            elif data_op == "Create_table":
                def create_table():
                    table_name = input("Input table name")
                    columns = input("Input columns names")
                    columns = columns.split(",")
                    df = pd.DataFrame(columns=columns, index= None)
                    df.to_sql(f"{table_name}",conn,index= False, if_exists= 'replace')
                    print(df.columns)
                    print(len(df.columns))
                create_table()
            elif process == "Add table" :
                def create_table():
                    table_name = st.text_input("Input table names")
                    columns = st.text_input("Input column names")
                    columns = columns.split(",")
                    data = pd.DataFrame(columns=columns, index= None)
                    data.to_sql(f"{table_name}",conn,index= False, if_exists= 'replace')
                    st.write(df.columns)
                    st.write(len(df.columns))
                create_table()
        else :
            print("No results")
            def create_table():
                columns = st.text_input("Input column names")
                columns = columns.split(",")
                table_name = st.text_input("Input table names")
                df = pd.DataFrame(columns=columns, index= None)
                df.to_sql(f"{table_name}",conn,index= False, if_exists= 'replace')
                #st.write(df.columns)
                #st.write(len(df.columns))
            create_table()
    else :
        print("You Have no account here")
        def create_account():
            username = st.text_input("Type Username")
            password = st.text_input("Type password")
            cursor.execute("INSERT INTO user(username, password) VALUES(?, ?)",(username,password))
            conn.commit()
        create_account()
else :
    def create_account():
            username = st.text_input("Type Username")
            password = st.text_input("Type password")
            cursor.execute("INSERT INTO user(username, password) VALUES(?, ?)",(username,password))
            conn.commit()
    create_account()
