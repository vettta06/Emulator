import clr

clr.AddReference("System.Windows.Forms")
import shlex
from System.Windows.Forms import Form, TextBox, Keys, MessageBox

form = Form()
form.Text = "VFS"

input = TextBox()
form.Controls.Add(input)

def input_enter(sender, event):
    if event.KeyCode == Keys.Enter:
        user_input = input.Text.strip()
        input.Text = ""

        mes = shlex.split(user_input)

        if mes and mes[0].lower() == "ls":
            MessageBox.Show(f"Команда: ls\nАргументы: {mes[1:]}")
            return

        if mes and mes[0].lower() == "cd":
            MessageBox.Show(f"Команда: cd\nАргументы: {mes[1:]}")
            return

        if mes and mes[0].lower() == "exit":
            form.Close()
            return

        MessageBox.Show(str(mes))

input.KeyDown += input_enter
form.ShowDialog()