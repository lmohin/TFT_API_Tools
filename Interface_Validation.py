# Python program to create a table
 
from tkinter import *
from quickstart import *
    

class Table:
    
    def __init__(self,case,lst):
        total_rows = len(lst)
        total_columns = len(lst[0])
        self.RootList = []
        self.root = Tk()
        self.RootList.append(self.root)
        self.root2 = Tk()
        self.RootList.append(self.root2)
        self.case = case
        self.lst = lst
        #self.grid = deepcopy(lst)
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                
                self.e = Entry(self.root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
                self.e.bind("<Return>", lambda event,I = i, J= j : self.on_change (event, I,J) )
                #self.grid[i][j] = self.e
        bnt = Button(self.root2, text="Valider", command=self.Write_cells_call, width=20)
        bnt.pack()
        bnt = Button(self.root2, text="Annuler", command=self.DestroyAll, width=20)
        bnt.pack()
        self.root.mainloop()
        self.root2.mainloop()
    def Write_cells_call(self):
        self.DestroyAll()
        write_cells(self.case, self.lst)
    def DestroyAll(self):
        for root in self.RootList:
            root.destroy()
    def on_change(self,e,i,j):
        print("index :", i,j)
        print("old : ", self.lst[i][j])
        #print("old : ", self.grid[i][j].get())
        new_value = e.widget.get()
        print ("Change : ", new_value)
        print("liste : ", self.lst)
        self.lst[i][j] = new_value

# take the data

 
# find total number of rows and
# columns in list

 
# create root window
