import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame


class VFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VFS")
        self.root.geometry("800x600")
        self.create_widgets()

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
                        self.print_output(f"ls command with args: {args}")
                    elif command == "cd":
                        self.print_output(f"cd command with args: {args}")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = VFSApp(root)
    root.mainloop()