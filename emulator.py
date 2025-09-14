import argparse
import sys
import clr
import os

clr.AddReference("System.Windows.Forms")
import shlex
from System.Windows.Forms import Form, TextBox, Keys, MessageBox

parser = argparse.ArgumentParser()
parser.add_argument("--vfs-path", type=str)
parser.add_argument("--script", type=str)
args = parser.parse_args()
print(args.script)

form = Form()
form.Text = "VFS"

input = TextBox()
form.Controls.Add(input)

def input_enter(sender, event):
    if event.KeyCode == Keys.Enter:
        user_input = input.Text.strip()
        input.Text = ""

        mes = shlex.split(user_input)
        if not mes: return

        if mes[0].lower() == "ls":
            MessageBox.Show(f"Команда: ls\nАргументы: {mes[1:]}")

        elif mes[0].lower() == "cd":
            MessageBox.Show(f"Команда: cd\nАргументы: {mes[1:]}")

        elif mes[0].lower() == "exit":
            form.Close()

        else:
            MessageBox.Show(str(mes))

input.KeyDown += input_enter

def file_enter(cmd_line):
    mes = shlex.split(cmd_line)
    if not mes: return

    if mes[0].lower() == "ls":
        MessageBox.Show(f"Команда: ls\nАргументы: {mes[1:]}")
    elif mes[0].lower() == "cd":
        MessageBox.Show(f"Команда: cd\nАргументы: {mes[1:]}")
    elif mes[0].lower() == "exit":
        MessageBox.Show("Завершение программы")
        #form.Close()

if args.script:
    f = open(args.script)
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        MessageBox.Show(f"vfs> {line}")
        file_enter(line)
    f.close()

form.ShowDialog()