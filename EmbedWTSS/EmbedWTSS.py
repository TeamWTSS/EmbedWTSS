from .Exceptions import InvalidSyntax
from .Exceptions import InvalidSyntaxCompiler
from .Exceptions import NeedAnArgument
from tkinter import *

KEYWORDS = [
    "SET",
    "RUN",
    "ADD"
]

"""
Example Grammar:

    SET window.title TO GianC
    ADD label.gianc
    SET label.gianc.text TO GianC

"""


class EmbedWTSS:
    window_settings = {
        "window.title": "EmbedWTSS",
        "window.width": 300,
        "window.heigth": 300
    }

    windows = {}

    default_settings = {
        "button": {"button.text": "TeamWTSS", "button.side": "left", "button.expand": False,
                   "button.fill": BOTH, "button.padx": False, "button.pady": False},
        "label": {"label.text": "TeamWTSS", "label.side": "left", "label.expand": False,
                  "label.fill": BOTH, "label.padx": False, "label.pady": False}
    }

    labels = {}

    buttons = {}

    def run(self, singleline_code: str = None, file: str = None):
        if singleline_code is None and file is None:
            raise NeedAnArgument
        if singleline_code is not None:
            self._run_singleline_code(singleline_code)
        elif file is not None:
            self._run_compiler(file)

    def _run_singleline_code(self, code: str):
        code_syntax = False
        command = code.split(" ")[0].lower()
        command_string = ""
        for i in KEYWORDS:
            keyword_check = code.split(" ")[0].lower()
            if keyword_check.endswith(";"):
                keyword_check = keyword_check[:-1]
            if i.lower() == keyword_check:
                code_syntax = True
        if not code.endswith("\\"):
            if code_syntax is False:
                raise InvalidSyntax
        else:
            command_string += code[0:(len(code) - 1)]
            while True:
                command_input_1 = input("\t-->\t")
                if not command_input_1.endswith(";"):
                    command_string += f"{command_input_1} "
                if command_input_1.endswith(";"):
                    break
            command = command_string.split(" ")[0].lower()
            code = command_string
        if not code.endswith(";"):
            raise InvalidSyntax
        if command.endswith(";") and code.endswith(";"):
            self._run_functions(command[:-1], code[:-1])
        elif code.endswith(";"):
            self._run_functions(command, code[:-1])
        elif command.endswith(";"):

            self._run_functions(command[:-1], code[:-1])
        else:
            self._run_functions(command, code)

    def _run_compiler(self, file_path: str):
        code = open(file_path, "r").read()
        i = True
        command = ""
        for index, value in enumerate(code.splitlines()):
            code_syntax = False
            if index == (len(code.splitlines())):
                i = False
                break
            if value.endswith(";"):
                command += value[0:(len(value) - 1)]
            else:
                command += value[0:(len(value))]
                continue
            for keyword in KEYWORDS:
                keyword_check = code.split(" ")[0].lower()
                if keyword_check.endswith(";"):
                    keyword_check = keyword_check[:-1]
                if keyword.lower() == keyword_check:
                    code_syntax = True
            if not code.endswith("\\"):
                if code_syntax is False:
                    raise InvalidSyntaxCompiler((index + 1), command)
            if command == "":
                self._run_functions(value[0:(len(value) - 1)], command)
            else:
                self._run_functions(command.split(" ")[0].lower(), command)
                command = ""
                continue

    def _set_function(self, code: str):
        code_split = code.split(" ")
        after_to = code_split.copy()
        after_to.pop(0)
        after_to.pop(0)
        after_to.pop(0)
        after_to_string = " ".join(after_to)

        def add_to_list(list_for_add, code_split):
            label_split = code_split[1].split(".")
            if after_to_string.lower() == r"s(bool{true})" or after_to_string.lower() == r"s(boolean{true})":
                list_for_add[f"{label_split[0]}.{label_split[1]}"][f"{label_split[0]}.{label_split[2]}"] = True
                return False
            elif after_to_string.lower() == r"s(bool{false})" or after_to_string.lower() == r"s(boolean{false})":
                list_for_add[f"{label_split[0]}.{label_split[1]}"][f"{label_split[0]}.{label_split[2]}"] = False
                return False
            list_for_add[f"{label_split[0]}.{label_split[1]}"][f"{label_split[0]}.{label_split[2]}"] = after_to_string

        if code_split[1].startswith("window."):
            try:
                window, window_name, window_option = code_split[1].split(".")
                self.windows[f"{window}.{window_name}"][f"{window}.{window_option}"] = after_to_string
                return
            except ValueError:
                if after_to_string.lower() == "sys(boolean{true})" or after_to_string.lower() == "sys(boolean{true})":
                    self.window_settings[code_split[1]] = True
                    return False
                elif after_to_string.lower() == "sys(bool{false})" or after_to_string.lower() == "sys(boolean{false})":
                    self.window_settings[code_split[1]] = False
                    return False
                self.window_settings[code_split[1]] = after_to_string
        elif code_split[1].startswith("label."):
            add_to_list(self.labels, code_split)
        elif code_split[1].startswith("button."):
            add_to_list(self.buttons, code_split)
        elif code_split[1].startswith("default."):
            label_split = code_split[1].split(".")
            if after_to_string.lower() == r"s(bool{true})" or after_to_string.lower() == r"s(boolean{true})":
                self.default_settings[f"{label_split[1]}"][f"{label_split[1]}.{label_split[2]}"] = True
                return False
            elif after_to_string.lower() == r"s(bool{false})" or after_to_string.lower() == r"s(boolean{false})":
                self.default_settings[f"{label_split[1]}"][f"{label_split[1]}.{label_split[2]}"] = False
                return False
            self.default_settings[f"{label_split[1]}"][f"{label_split[1]}.{label_split[2]}"] = after_to_string

    def _add_function(self, code: str):
        code_split = code.split(" ")
        if code_split[1].lower().startswith("label."):
            self.labels[code_split[1]] = self.default_settings["label"].copy()
        elif code_split[1].lower().startswith("button."):
            self.buttons[code_split[1]] = self.default_settings["button"].copy()
        elif code_split[1].lower().startswith("window."):
            self.windows[code_split[1]] = self.window_settings.copy()

    def _run_functions(self, command, code):
        if command == "set":
            self._set_function(code)
        elif command == "run":
            try:
                run_command, filepath_or_name = code.split(" ")
                if str(filepath_or_name).startswith("file://"):
                    if str(filepath_or_name).endswith(";"):
                        self.run(file=filepath_or_name[7:(len(filepath_or_name) - 1)])
                    else:
                        self.run(file=filepath_or_name[7:(len(filepath_or_name))])
                elif str(filepath_or_name).startswith("window://"):
                    if str(filepath_or_name).endswith(";"):
                        self._new_window(filepath_or_name[9:(len(filepath_or_name) - 1)])
                    else:
                        self._new_window(filepath_or_name[9:(len(filepath_or_name))])
                else:
                    self._run_window()
            except ValueError:
                self._run_window()

        elif command == "add":
            self._add_function(code)

    def add_items_to_window(self, window):

        for lbl in self.labels.items():
            if lbl[1]['label.padx'] is not False and lbl[1]['label.pady'] is not False:
                newlbl = Label(window, text=f"{lbl[1]['label.text']}", padx=lbl[1]['label.padx'],
                               pady=lbl[1]['label.pady'])
                newlbl.pack(side=(lbl[1]['label.side']), fill=lbl[1]['label.fill'],
                            expand=lbl[1]['label.expand'])
            elif lbl[1]['label.pady'] is not False and lbl[1]['label.padx'] is False:
                newlbl = Label(window, text=f"{lbl[1]['label.text']}", pady=lbl[1]['label.pady'])
                newlbl.pack(side=(lbl[1]['label.side']), fill=lbl[1]['label.fill'],
                            expand=lbl[1]['label.expand'])
            elif lbl[1]['label.pady'] is False and lbl[1]['label.padx'] is not False:
                newlbl = Label(window, text=f"{lbl[1]['label.text']}", padx=lbl[1]['label.padx'])
                newlbl.pack(side=(lbl[1]['label.side']), fill=lbl[1]['label.fill'],
                            expand=lbl[1]['label.expand'])
            else:
                newlbl = Label(window, text=f"{lbl[1]['label.text']}")
                newlbl.pack(side=(lbl[1]['label.side']), fill=lbl[1]['label.fill'],
                            expand=lbl[1]['label.expand'])
        for lbl in self.buttons.items():
            if lbl[1]['button.padx'] is not False and lbl[1]['button.pady'] is not False:
                newlbl = Button(window, text=f"{lbl[1]['button.text']}", padx=lbl[1]['button.padx'],
                                pady=lbl[1]['button.pady'])
                newlbl.pack(side=(lbl[1]['button.side']), fill=lbl[1]['button.fill'],
                            expand=lbl[1]['button.expand'])
            elif lbl[1]['button.pady'] is not False and lbl[1]['button.padx'] is False:
                newlbl = Button(window, text=f"{lbl[1]['button.text']}", pady=lbl[1]['button.pady'])
                newlbl.pack(side=(lbl[1]['button.side']), fill=lbl[1]['button.fill'],
                            expand=lbl[1]['button.expand'])
            elif lbl[1]['button.pady'] is False and lbl[1]['button.padx'] is not False:
                newlbl = Button(window, text=f"{lbl[1]['button.text']}", padx=lbl[1]['button.padx'])
                newlbl.pack(side=(lbl[1]['button.side']), fill=lbl[1]['button.fill'],
                            expand=lbl[1]['button.expand'])
            else:
                newlbl = Button(window, text=f"{lbl[1]['button.text']}")
                newlbl.pack(side=(lbl[1]['button.side']), fill=lbl[1]['button.fill'],
                            expand=lbl[1]['button.expand'])

    def _new_window(self, window_name):
        try:
            window = Tk()
            window_name = str(window_name).replace("//", "")
            title, width, height = self.windows[window_name].items()
            window.title(title[1])
            window.geometry(f'{width[1]}x{height[1]}')
            self.add_items_to_window(window)
            window.mainloop()
        except TclError:
            raise InvalidSyntax

    def _run_window(self):
        try:
            window = Tk()
            title, width, height = self.window_settings.items()
            window.title(title[1])
            window.geometry(f'{width[1]}x{height[1]}')
            self.add_items_to_window(window)
            window.mainloop()
        except TclError:
            raise InvalidSyntax

