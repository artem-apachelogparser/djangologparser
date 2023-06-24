import apache_log_parser
import psycopg2
import json
import glob

with open('config.json', 'r') as f:
    config = json.load(f)

log_dir = config['log_dir']
file_mask = config['file_mask']


def parse_and_store_logs(logfile):
    # Соединение с базой данных
    conn = psycopg2.connect(
        host="localhost",
        database="apache_logs",
        user="postgres",
        password=""
    )

    # Создание курсора
    cur = conn.cursor()

    # Определение формата журнала Apache
    line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b")

    with open(logfile, 'r') as f:
        for line in f:
            # Разбор строки журнала
            log_data = line_parser(line)

            # Запись данных в БД
            cur.execute(
                "INSERT INTO djangologparser_apachelog (host, user_name, time, request, status, size, referer, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    log_data['remote_host'],
                    log_data['remote_user'] if log_data['remote_user'] else '',
                    log_data['time_received_datetimeobj'],
                    log_data['request_first_line'],
                    log_data['status'],
                    log_data['response_bytes_clf'],
                    log_data.get('request_header_referer', ''),
                    log_data.get('request_header_user_agent', ''),

                )
            )

        # Осуществление транзакции
        conn.commit()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

# Использование функции
path = f"{log_dir}/{file_mask}"

# Использование glob.glob для получения всех файлов, соответствующих пути
for filename in glob.glob(path):
    parse_and_store_logs(filename)

