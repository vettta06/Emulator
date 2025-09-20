import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame
import argparse
import os


class VFSApp:
    def __init__(self, root, vfs_path='./vfs_root', script_path=None):
        self.root = root
        self.root.title("VFS")
        self.root.geometry("800x600")
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.current_vfs = {}
        self.current_dir = "/"

        self.create_widgets()
        self.initialize_vfs()
        self.print_output(f"VFS Emulator запущен")
        self.print_output(f"VFS путь: {vfs_path}")
        if script_path:
            self.print_output(f"Скрипт для выполнения: {script_path}")
            self.root.after(1000, self.run_script)

    def create_widgets(self):
        self.output_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state='disabled',
            height=20
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        input_frame = Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.command_entry = Entry(input_frame, font=('Courier', 12))
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.command_entry.bind('<Return>', self.execute_command)

        self.execute_button = Button(input_frame, text="Execute", command=self.execute_command)
        self.execute_button.pack(side=tk.RIGHT, padx=(5, 0))

    def execute_command(self, event=None):
        command_line = self.command_entry.get().strip()
        if command_line:
            self.print_output(f"> {command_line}")
            try:
                tokens = self.parse_command(command_line)
                if tokens:
                    command = tokens[0]
                    args = tokens[1:] if len(tokens) > 1 else []

                    if command == "exit":
                        self.root.quit()
                    elif command == "ls":
                        self.list_directory(args)
                    elif command == "cd":
                        self.change_directory(args)
                    elif command == "echo":
                        message = " ".join(args)
                        self.print_output(message)
                    elif command == "vfs-init":
                        self.initialize_vfs()
                        self.print_output("VFS инициализирована по умолчанию")
                    elif command == "pwd":
                        self.print_output(f"Текущая директория: {self.current_dir}")
                    else:
                        self.print_output(f"Unknown command: {command}")

            except ValueError as e:
                self.print_output(f"Ошибка синтаксиса: {e}")
            except Exception as e:
                self.print_output(f"Неожиданная ошибка: {e}")

            self.command_entry.delete(0, tk.END)

    def print_output(self, text):
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

    def parse_command(self, command_line):
        tokens = []
        current_token = ""
        in_quotes = False
        quote_char = None

        for char in command_line:
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                else:
                    current_token += char
            elif char == ' ' and not in_quotes:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append(current_token)

        if in_quotes:
            raise ValueError("Незакрытые кавычки в команде")

        return tokens

    def run_script(self):
        if not self.script_path or not os.path.exists(self.script_path):
            self.print_output(f"Ошибка: Скрипт {self.script_path} не найден")
            return

        self.print_output(f"# Выполнение скрипта: {self.script_path}")
        self.print_output("#" + "=" * 50)

        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    self.print_output(f"[Скрипт:{line_num}] > {line}")
                    self.command_entry.delete(0, tk.END)
                    self.command_entry.insert(0, line)
                    self.execute_command()

        except Exception as e:
            self.print_output(f"Ошибка чтения скрипта: {e}")


    def initialize_vfs(self):
        self.current_vfs = {
            "/": {
                "type": "directory",
                "content": {
                    "home": {
                        "type": "directory",
                        "content": {
                            "user": {
                                "type": "directory",
                                "content": {
                                    "documents": {"type": "directory", "content": {}},
                                    "photos": {"type": "directory", "content": {}}
                                }
                            }
                        }
                    },
                    "etc": {
                        "type": "directory",
                        "content": {
                            "config.txt": {"type": "file", "size": 1024},
                            "settings.ini": {"type": "file", "size": 512}
                        }
                    },
                    "readme.txt": {"type": "file", "size": 2048}
                }
            }
        }
        self.current_dir = "/"

        if os.path.exists(self.vfs_path):
            import shutil
            shutil.rmtree(self.vfs_path)
        os.makedirs(self.vfs_path, exist_ok=True)


    def list_directory(self, args):
        try:
            current = self.get_current_directory()
            if not current or current["type"] != "directory":
                self.print_output("Ошибка: не является директорией")
                return

            items = []
            for name, item in current["content"].items():
                item_type = "d" if item["type"] == "directory" else "f"
                items.append(f"{item_type} {name}")

            self.print_output("\n".join(items) if items else "Директория пуста")

        except Exception as e:
            self.print_output(f"Ошибка ls: {e}")


    def change_directory(self, args):
        if not args:
            self.print_output("Ошибка: укажите путь")
            return

        path = args[0]
        try:
            if path == "/":
                self.current_dir = "/"
            elif path == "..":
                if self.current_dir != "/":
                    parts = self.current_dir.rstrip('/').split('/')
                    self.current_dir = '/' + '/'.join(parts[:-1]) if len(parts) > 1 else "/"
            else:
                new_path = os.path.join(self.current_dir, path).replace('\\', '/')
                if self.path_exists(new_path):
                    self.current_dir = new_path
                else:
                    self.print_output(f"Ошибка: директория {path} не существует")

            self.print_output(f"Текущая директория: {self.current_dir}")

        except Exception as e:
            self.print_output(f"Ошибка cd: {e}")


    def get_current_directory(self):
        if self.current_dir == "/":
            return self.current_vfs.get("/")

        parts = self.current_dir.strip('/').split('/')
        current = self.current_vfs.get("/")
        for part in parts:
            if part and current and current["type"] == "directory":
                current = current["content"].get(part)
            else:
                return None
        return current


    def path_exists(self, path):
        if path == "/":
            return True

        parts = path.strip('/').split('/')
        current = self.current_vfs.get("/")
        for part in parts:
            if part and current and current["type"] == "directory":
                current = current["content"].get(part)
            else:
                return False
        return current is not None


def parse_arguments():
    parser = argparse.ArgumentParser(description='VFS Emulator')
    parser.add_argument('--vfs-path', '-v', type=str, default='./vfs_root',
                        help='Путь к физическому расположению VFS')
    parser.add_argument('--script', '-s', type=str,
                        help='Путь к стартовому скрипту')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print("=" * 50)
    print("ПАРАМЕТРЫ ЗАПУСКА:")
    print(f"VFS путь: {args.vfs_path}")
    print(f"Скрипт: {args.script if args.script else 'Не указан'}")
    print("=" * 50)

    root = tk.Tk()
    app = VFSApp(root, vfs_path=args.vfs_path, script_path=args.script)
    root.mainloop()