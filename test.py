# Team Memebers Contributiing to this page: 
# Grant Kite -


from sqlalchemy import create_engine, text


print('running main')
engine = create_engine("postgresql://postgres:@localhost:5432/battleborn")
# print('create_engine')
connection = engine.connect()

q = "SELECT * FROM table_1"
results = connection.execute(q).fetchall()

print(results)

# with engine.connect() as conn:
#     print('inside the connect')
#     result = conn.execution_options(stream_results=True).execute(text("select * from table_1"))
# print('working?')
# print(result)

