
# The parameter passed in must be an array of strings where the first string is the table name. 
# The rest of the strings are the column variables of the table in order.
# example table_data = ["table_name", "column 1", "column 2", "column 3".....]

def save_query(table_data):
    data_len = len(table_data)-1
    q1 = "INSERT INTO " + table_data[0] + " ( "

    for i in range(1,data_len):
        q1 += table_data[i] + ", "
        # print(q1)
    q1 += table_data[data_len]
    # print(q1)
    
    
    q1 += ") VALUES ( %(" + table_data[1] + ")s, "
    for i in range(2,data_len):
        if table_data[i] == "created_at" or table_data[i] == "updated_at":
            if i == data_len:
                q1 += "NOW() "
                print(q1,table_data[i])
                # continue
            else:
                q1 += "NOW(), "
                print(q1,table_data[i])
                # continue
        else:
            q1 += "%(" + table_data[i] + ")s, "
            print(q1,table_data[i])

    if table_data[data_len] == "created_at" or table_data[data_len] == "updated_at":
        q1 += "NOW() );"
        print(q1,table_data[data_len])
    else:
        q1 += "%(" + table_data[data_len] + ")s );"
        print(q1,table_data[data_len])

    return q1


def update_query(table_data):
    data_len = len(table_data)-1
    q2 = "UPDATE " + table_data[0] + " SET "
    
    for i in range(1,data_len):
        if table_data[i] != "created_at" and table_data[i] != "updated_at":
            q2 += table_data[i] + "=%(" + table_data[i] + ")s, "
    
    if table_data[data_len] != "created_at" and table_data[data_len] != "updated_at":
        q2 += table_data[data_len] + "=%(" + table_data[data_len] + ")s WHERE id=%(id)s; "
    else:
        q2 += " WHERE id=%(id)s; "
        
    
    return q2

