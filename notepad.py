from random import randint
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import os, sys

def onClickKeyF1():
    def onCloseFormRef(): formRef.destroy()
    formRef = Toplevel()
    formRef.geometry("{}x{}+{}+{}".format(425, 115, (formRef.winfo_screenwidth() - 425) // 2, (formRef.winfo_screenheight() - 425) // 2))
    formRef.resizable(False, False)
    formRef.title('О программе')
    formRef.iconbitmap(default=os.path.join(application_path, 'icon.ico'))
    Label(formRef, text="Блокнот - версия 1.0.\n© KitsuruDev, 2024. Все права защищены", font=('Segoe UI', 16)).place(x=8, y=8, width=400, height=92)
    formRef.protocol("WM_DELETE_WINDOW", onCloseFormRef)
    formRef.grab_set()
    formRef.mainloop()

def onCaretChange(event):
    line, column = Memo.index(INSERT).split(".")
    StatusBar['text'] = f"Строка {line}, столбец {column}"

def clipboardAny():
    try: Memo.selection_get(selection="CLIPBOARD")
    except TclError: return False
    return True

def LoadCryptoKeys():
    global KeyPriv, SimpleDigit
    with open(os.getcwd()+"\\Key.txt", 'r', encoding='utf-8') as f: KeyPriv = int(f.readline())
    SimpleDigit, i = [True for t in range(0, 60001)], 2 # Решето Эратосфена
    while i*i <= 60000:
        if SimpleDigit[i] == True:
            j = i*i
            while j <= 60000:
                SimpleDigit[j] = False
                j+=i
        i+=1

def Code(text, generateKey=True):
    global KeyOpen, KeyPriv
    if generateKey:
        while True:
            Key = randint(20000, 60000)
            if SimpleDigit[Key] == True: break
        KeyOpen = KeyPriv * Key
    else: Key = KeyOpen // KeyPriv
    s_new = ''
    for i in range(len(text)): s_new += chr(ord(text[i])^Key)
    if generateKey: return str(KeyOpen) + '\n' + s_new
    return s_new

def onClickNewFile():
    Memo.delete("1.0", END)

def onClickOpenFile():
    global KeyOpen
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), initialfile="Note_file.txt", filetypes=(("Зашифрованный файл", "*.txt"),))
    if file_path:
        Memo.delete("1.0", END)
        with open(file_path, encoding='utf-8') as f:
            KeyOpen = int(f.readline())
            Memo.insert("1.0", Code(f.read().split('\n')[-1], generateKey=False))
    
def onClickSaveFile():
    global KeyPriv
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), initialfile="Note_file.txt", filetypes=(("Зашифрованный файл", "*.txt"),))
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f: f.write(Code(Memo.get("1.0", END)))

def onClickUndo():
    if Memo.edit("canundo"): Memo.edit_undo()

def onClickCopy(cut):
    if Memo.tag_ranges(SEL):
        Memo.clipboard_clear()
        Memo.clipboard_append(Memo.selection_get())
        if cut: onClickDel()

def onClickPaste():
    if clipboardAny(): Memo.insert(INSERT, Memo.clipboard_get())

def onClickDel():
    if Memo.tag_ranges(SEL):
        Memo.edit_separator() # для разграничения в стеке действий, чтобы функция была отдельной при возврате
        Memo.delete("sel.first", "sel.last")

def onClickSelectAll():
    Memo.tag_add(SEL, "1.0", END)
    Memo.mark_set(INSERT, "1.0")
    Memo.see(INSERT)

def onClickCtrlHotKeys(event):
    dict_hot_keys_translate = {90: 'onClickUndo()', 88: 'onClickCopy(cut=True)', 67: 'onClickCopy(cut=False)', 86: 'onClickPaste()', 65: 'onClickSelectAll()',
                               81: 'formMain.quit', 78: 'onClickNewFile()', 83: 'onClickSaveFile()', 79: 'onClickOpenFile()'}
    if event.keycode in dict_hot_keys_translate: eval(dict_hot_keys_translate[event.keycode])

formMain, KeyPriv, KeyOpen, SimpleDigit = Tk(), 0, 0, []
application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

LoadCryptoKeys()

formMain.geometry("{}x{}+{}+{}".format(446, 360, (formMain.winfo_screenwidth()-446)//2, (formMain.winfo_screenheight()-360)//2))
formMain.iconbitmap(default=os.path.join(application_path, 'icon.ico'))
formMain.title('Блокнот')

Style().configure(style=".", background="white", foreground="black", font=('Segoe UI', 10))

dic_key_actions = {1: ["<KeyPress>",'onCaretChange'],
                   2: ["Del",'lambda i:onClickDel()'],
                   3: ["<F1>",'lambda i:onClickKeyF1()'],
                   4: ["<Control-KeyPress>",'onClickCtrlHotKeys'],
                   5: ["<Left>",'onCaretChange'],
                   6: ["<Right>",'onCaretChange'],
                   7: ["<Up>",'onCaretChange'],
                   8: ["<Down>",'onCaretChange']}
for i in dic_key_actions: formMain.bind(dic_key_actions[i][0], eval(dic_key_actions[i][1]))

formMain.option_add("*tearOff", FALSE) # убираем лишние полосы в начале списков подменю

main_menu, file_menu, text_menu, about_menu = Menu(), Menu(), Menu(), Menu()
formMain.config(menu=main_menu)

dic_main_menu = {1: ["Файл",'file_menu'], 2: ["Изменить",'text_menu'], 3: ["Справка",'about_menu']}
dict_text_menu = {1: ["Отменить","Ctrl+Z",'onClickUndo'],
                  2: [],
                  3: ["Вырезать","Ctrl+X",'lambda:onClickCopy(cut=True)'],
                  4: ["Копировать","Ctrl+C",'lambda:onClickCopy(cut=False)'],
                  5: ["Вставить","Ctrl+V",'onClickPaste'],
                  6: ["Удалить","Del",'onClickDel'],
                  7: [],
                  8: ["Выбрать всё","Ctrl+A",'onClickSelectAll']}
dic_file_menu = {1: ["Создать","Ctrl+N",'onClickNewFile'],
                 2: ["Сохранить","Ctrl+S",'onClickSaveFile'],
                 3: ["Открыть","Ctrl+O",'onClickOpenFile'],
                 4: [],
                 5: ["Выход","Ctrl+Q",'formMain.quit']}

for i in dic_main_menu: 
    main_menu.add_cascade(label=dic_main_menu[i][0], menu=eval(dic_main_menu[i][1]))

for i in dict_text_menu:
    if i == 2 or i == 7: text_menu.add_separator()
    else: text_menu.add_command(label=dict_text_menu[i][0], accelerator=dict_text_menu[i][1], command=eval(dict_text_menu[i][2]))

for i in dic_file_menu:
    if i == 4: file_menu.add_separator()
    else: file_menu.add_command(label=dic_file_menu[i][0], accelerator=dic_file_menu[i][1], command=eval(dic_file_menu[i][2]))

about_menu.add_command(label="О программе", accelerator="F1", command=onClickKeyF1)

Memo, StatusBar = Text(wrap="none", undo=True), Label(text="Строка 1, столбец 0", border=1, relief=SUNKEN, anchor=W)
StatusBar.pack(side=BOTTOM, fill=X)

dic_scrollbars = {1: ["vertical",'Memo.yview', 'RIGHT', 'Y', "yscrollcommand"], 2: ["horizontal", 'Memo.xview', 'BOTTOM', 'X', "xscrollcommand"]}
for i in dic_scrollbars:
    scrollbar = Scrollbar(orient=dic_scrollbars[i][0], command=eval(dic_scrollbars[i][1]))
    scrollbar.pack(side=eval(dic_scrollbars[i][2]), fill=eval(dic_scrollbars[i][3]))
    Memo[dic_scrollbars[i][4]] = scrollbar.set
    
Memo.pack(expand=True, fill='both')

formMain.mainloop()
