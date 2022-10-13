import psycopg2


def connect():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="12321",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        connection.autocommit = True
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    return connection, cursor


def execute(cursor, req: str):
    try:
        cursor.execute(req)
        desc = cursor.description
        desc = [i[0] for i in desc]
        record = cursor.fetchall()
        print("-" * 40)
        for item in record:
            for i in range(len(item)):
                print(f"{desc[i]}: {item[i]}")
            print("-" * 40)
        print()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def print_menu():
    print("=" * 40, """
1. Все объявления
2. Объявления конкретного пользователя
3. Объявления в диапазоне цен, в порядке возрастания цены
4. Объявления для конкретного города
5. Информация для определенного пользователя и цены
0. Выход
""", "=" * 40)


def main():
    connection, cursor = connect()
    print_menu()
    while True:
        user_input = input("Запрос: ")
        match user_input:
            case "1":
                req = "SELECT * FROM ads;"
            case "2":
                name = input("Имя пользователя: ")
                req = f"""SELECT a."Id",
                                 name,
                                 author,
                                 price,
                                 address,
                                 is_published,
                                 description
                          FROM ads a
                            JOIN authors b
                              ON author_id = b."Id"
                            JOIN addresses c
                              ON address_id = c."Id"
                          WHERE author = '{name}';"""
            case "3":
                min_price = input("От: ")
                max_price = input("До: ")
                req = f"""SELECT a."Id",
                                 name,
                                 author,
                                 price,
                                 address,
                                 is_published,
                                 description
                          FROM ads a
                            JOIN authors b
                              ON author_id = b."Id"
                            JOIN addresses c
                              ON address_id = c."Id"
                          WHERE price >= {min_price}
                                AND price <= {max_price}
                          ORDER BY price;"""
            case "4":
                city = input("Город: ")
                req = f"""SELECT a."Id",
                                 name,
                                 author,
                                 price,
                                 address,
                                 is_published,
                                 description
                          FROM ads a
                            JOIN authors b
                              ON author_id = b."Id"
                            JOIN addresses c
                              ON address_id = c."Id"
                          WHERE address LIKE '{city}%';"""
            case "5":
                req = f"""SELECT author,
                                 SUM(price)
                          FROM ads a
                            JOIN authors b
                              ON author_id = b."Id"
                          GROUP BY author;"""
            case "0":
                break
            case _:
                continue
        execute(cursor, req)


if __name__ == "__main__":
    main()
