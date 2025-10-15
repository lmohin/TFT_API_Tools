# Python program to create a table
 
from tkinter import *
from quickstart import *
    

class Table:
    
    def __init__(self,case,lst):
        total_rows = len(lst)
        total_columns = len(lst[0])
        self.root = Tk()
        self.root2 = Tk()
        self.case = case
        self.lst = lst
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                
                self.e = Entry(self.root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
        bnt = Button(self.root2, text="Valider", command=self.Write_cells_call, width=20)
        bnt.pack()
        bnt = Button(self.root2, text="Annuler", command=self.Destroy, width=20)
        bnt.pack()
        self.root.mainloop()
        self.root2.mainloop()
    def Write_cells_call(self):
        self.Destroy()
        write_cells(self.case, self.lst)
    def Destroy(self):
        self.root.destroy()
        self.root2.destroy()
# take the data

 
# find total number of rows and
# columns in list

 
# create root window
