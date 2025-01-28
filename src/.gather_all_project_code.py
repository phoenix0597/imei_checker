import os
import fnmatch

# Список исключаемых директорий и файлов
excluded_dirs = ['.env', '.venv', '__pycache__', 'logs', '.idea', '.git', '.gitignore', '.arch_template_for_tg_bot.txt',
                 'arch_template_for_tg_bot.txt', '.gather_all_project_code.py', '.gather_selected_files_code.py',
                 '.pytest_cache', '.env-non-dev', 'migrations', 'static'
                 '.all_project_code.txt', 'requirements.txt', 'README.md']


# def is_excluded(path):
#     """
#     Проверяет, находится ли файл или папка в списке исключений.
#     """
#     for excluded in excluded_dirs:
#         if excluded in path.split(os.sep):
#             return True
#     return False


def is_excluded(path):
    """
    Проверяет, находится ли файл или папка в списке исключений.
    Поддерживает маски файлов (например, "*.md").
    """
    path_parts = path.split(os.sep)
    filename = os.path.basename(path)

    for excluded in excluded_dirs:
        # Проверка на точное совпадение с частями пути
        if excluded in path_parts:
            return True

        # Проверка на совпадение с маской файла
        if any(fnmatch.fnmatch(part, excluded) for part in path_parts):
            return True

        # Дополнительная проверка для имени файла
        if fnmatch.fnmatch(filename, excluded):
            return True

    return False


def write_file_list(base_path: str, output_file: str):
    """
    Обходит все файлы и папки начиная с base_path и записывает информацию о них в output_file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(base_path):
            # Исключаем нежелательные директории
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d))]
            for file in files:
                if is_excluded(os.path.join(root, file)):
                    continue
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start=base_path)
                # Записываем имя файла
                f.write(f'- `{relative_path}`:\n')
                # Записываем содержимое файла
                f.write('```\n')
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        f.write(file_content.read())
                except UnicodeDecodeError:
                    f.write('<binary content or non-text data>')
                except Exception as e:
                    f.write(f'<error reading file: {e}>')
                f.write('\n```\n\n')


if __name__ == '__main__':
    # Название файла, в который будет производиться запись
    output_filename = '.all_project_code.txt'
    # Запускаем обработку из текущей директории
    write_file_list('.', output_filename)
    print(f"Processed files are listed in '{output_filename}'")
