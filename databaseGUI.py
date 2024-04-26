import pyodbc
import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("650x650")
app.title("Database")

entry_query = customtkinter.CTkEntry(app,placeholder_text="Enter an SQL query")
entry_query.place(relx=0.1, rely=0.3)

entry_table_name = customtkinter.CTkEntry(app,placeholder_text="Enter a table")
entry_table_name.place(relx=0.7, rely=0.1)

entry_column_name = customtkinter.CTkEntry(app,placeholder_text="Enter a column name")
entry_column_name.place(relx=0.7, rely=0.2)

entry_column_value = customtkinter.CTkEntry(app,placeholder_text="Enter a column value")
entry_column_value.place(relx=0.7, rely=0.3)

entry_table_update = customtkinter.CTkEntry(app,placeholder_text="Enter table to update")
entry_table_update.place(relx=0.4, rely=0.1)

entry_new_values = customtkinter.CTkEntry(app,placeholder_text="Enter new values")
entry_new_values.place(relx=0.4, rely=0.2)

entry_where_values = customtkinter.CTkEntry(app,placeholder_text="Enter where values")
entry_where_values.place(relx=0.4, rely=0.3)

def execute_query():
    try:
        connection = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};'+
                                    'database=AUTOMATION;'+
                                    'server=WIN-E1MB9ES24B3;'+
                                    'trusted_connection=yes;')
        cursor = connection.cursor()
        query = entry_query.get()
        cursor.execute(query)
        if query.lower().startswith("select"):

            columns = [column[0] for column in cursor.description]


            data = cursor.fetchall()
            if data:

                result = "\n".join([" || ".join([f"{col}: {val}" for col, val in zip(columns, row)]) for row in data])
                info_label.configure(text=result)
            else:
                info_label.configure(text="No data found")
        else:
            connection.commit()
            if cursor.rowcount > 0:
                info_label.configure(text=f"{cursor.rowcount} row(s) affected")
            else:
                info_label.configure(text="No rows affected")
    except pyodbc.Error as ex:
        print("Failed!", ex)
        info_label.configure(text="Failed to execute query")


def select():
    try:
        connection = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};'+
                                    'database=AUTOMATION;'+
                                    'server=WIN-E1MB9ES24B3;'+
                                    'trusted_connection=yes;')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM [{entry_table_name.get()}] WHERE {entry_column_name.get()}='{entry_column_value.get()}'")


        columns = [column[0] for column in cursor.description]


        data = cursor.fetchone()
        if data:

            result = zip(columns, data)
            info_label.configure(text=" || ".join([f"{col}: {val}" for col, val in result]))
        else:
            info_label.configure(text="No data found")
    except pyodbc.Error as ex:
        print("Failed!",ex)
        info_label.configure(text="No table found")


def update():
    try:
        connection = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};'+
                                    'database=AUTOMATION;'+
                                    'server=WIN-E1MB9ES24B3;'+
                                    'trusted_connection=yes;')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {entry_table_update.get()} SET {entry_new_values.get()} WHERE {entry_where_values.get()}")
        connection.commit()
        info_label.configure(text="Update successful")
    except pyodbc.Error as ex:
        print("Failed!", ex)
        info_label.configure(text="Failed to update")

execute_button = customtkinter.CTkButton(app,text="Execute", command=execute_query, fg_color="teal")
execute_button.place(relx=0.1, rely=0.4)

select_button = customtkinter.CTkButton(app,text="Select", command=select, fg_color="teal")
select_button.place(relx=0.7, rely=0.4)

update_button = customtkinter.CTkButton(app,text="Update", command=update, fg_color="teal")
update_button.place(relx=0.4, rely=0.4)

info_label = customtkinter.CTkLabel(app,text="Information",font=("Arial",18),wraplength= 640)
info_label.place(relx=0.001, rely=0.5)

app.mainloop()
