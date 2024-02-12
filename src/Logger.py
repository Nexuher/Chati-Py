import data_pack
import inspect

data_package = data_pack.return_data_pack()
file_directory = data_package.create_logger_path_location()

# Error Logger
def handle_logs(error_type, error_name, user_message):
    file_handler = open(f"{file_directory}","a")

    error_log = f"""\n
            Date of error occurrence:    {data_package.date_string_formatted}
            Error Type:                  {error_type}-{error_name}
            Function:                    {inspect.stack()[1][3]}

            Message inputted:            {user_message}
"""

    file_handler.write(error_log)
    file_handler.close()


# Info Logger
def handle_logs(error_type, error_message):
    file_handler = open(f"{file_directory}","a")

    error_log = f"""\n{data_package.date_string_formatted} {data_package.datatime_information_set.hour}:{data_package.datatime_information_set.minute} - {error_type} - {error_message} - {inspect.stack()[1][3]}"""

    file_handler.write(error_log)
    file_handler.close()