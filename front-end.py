from tkinter import *
import rec
window = Tk()
import pandas as pd
from bloom_filter import BloomFilter
movies_data = pd.read_csv('./movies.csv')
list_of_all_titles = movies_data['title'].tolist()
b = BloomFilter(max_elements=10000, error_rate=0.1)
for list in list_of_all_titles:
  b.add(list)

def get_row_id(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0,END)
    e1.insert(END,selected_tuple[1])
def getRec():
    list1.delete(0, END)
    title_name = rec.getRef(title_text.get())
    for title in title_name:
        list1.insert(END,title)
def check():
    list1.delete(0,END)
    title_of_movie = title_text.get()
    result =  title_of_movie in b
    if(result == 1):
        list1.insert(END, 'Yes!Your title of movie in our dataset')

    else:
        list1.insert(END, 'Your given not in our dataset')
l1 = Label(window, text="Title of movie:")
l1.grid(row=0, column=0)

title_text = StringVar()
e1 = Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)


list1 = Listbox(window, height=6, width=35)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

list1.bind('<<ListboxSelect>>',get_row_id)
sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

b1 = Button(window, text="Check valid?", width=12,command=check)
b1.grid(row=2, column=3)
b2 = Button(window, text="Get rec", width=12,command=getRec)
b2.grid(row=3, column=3)


window.mainloop()
