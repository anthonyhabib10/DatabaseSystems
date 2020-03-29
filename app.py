from flask import Flask, render_template, request
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine('mysql+mysqldb://root:@localhost:3306/school', pool_recycle=3600)


def query_database(string):
    try:
        with engine.connect() as con:
            rows = con.execute(string)
            return list(rows)
    except Exception as e:
        print("Something went wrong!\n", "Error:", e)


def get_rows_from_query_string(query_string):
    return query_string.lower().split("select ")[1].split(" from")[0].split(",")


def get_row_aliases(row_names):
    row_name_aliases = []
    for row_name in row_names:
        if "as" in row_name:
            row_name_aliases.append(row_name.split("as ")[1])
        else:
            row_name_aliases.append(row_name)
    return row_name_aliases


def get_table_name_from_query_string(query_string):
    return query_string.lower().split("from")[1].split(" ")[1]


@app.route('/', methods=['GET', 'POST'])
def index():
    table_rows = []
    row_names = []
    if request.method == "POST":
        query_string = request.form['content']
        try:
            if query_string:
                # Get row names to display
                selected_rows = get_rows_from_query_string(query_string)
                if selected_rows[0] == "*":

                    table_name = get_table_name_from_query_string(query_string)
                    row_names = query_database(
                        f"select column_name from information_schema.columns where table_name='{table_name}'")
                    # row_names is list of 1 element tuples... make it a flat list
                    row_names = [name_t[0] for name_t in row_names]
                else:

                    row_names = selected_rows

                row_names = get_row_aliases(row_names)
                table_rows = query_database(query_string)
        except IndexError:
            print("Incomplete query!?")
    return render_template('index.html', table_rows=table_rows, row_names=row_names)


@app.route('/select', methods=['GET', 'POST'])
def select():
    table_rows = []
    row_names = []
    if request.method == "POST":
        query_string = request.form['content']

        try:
            if query_string:
                # Get row names to display
                selected_rows = get_rows_from_query_string(query_string)
                print(selected_rows)
                if selected_rows[0] == "*":

                    table_name = get_table_name_from_query_string(query_string)
                    row_names = query_database(
                        f"select column_name from information_schema.columns where table_name='{table_name}'")
                    # row_names is list of 1 element tuples... make it a flat list
                    row_names = [name_t[0] for name_t in row_names]
                else:
                    row_names = selected_rows
                row_names = get_row_aliases(row_names)
                table_rows = query_database(query_string)
        except IndexError:
            print("Incomplete query!?")
    return render_template('select.html', table_rows=table_rows, row_names=row_names)


if __name__ == '__main__':
    app.run(debug=True)

