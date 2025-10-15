# Python program to create a table
 
from tkinter import *
from quickstart import *
    

class Preview:
    
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
        _, starting_cell = case.split('!')
        for j in range(total_columns):
            self.e = Entry(self.root, width=20, fg='blue',
                               font=('Arial',10,'bold'))
            self.e.grid(row=0, column=j+1)
            self.e.insert(END, chr((ord(starting_cell[0])+j)))
        for i in range(total_rows):
            self.e = Entry(self.root, width=10, fg='blue',
                               font=('Arial',10,'bold'))
            self.e.grid(row=i+1, column=0)
            self.e.insert(END, str(int((starting_cell[1:]))+i))
        for i in range(total_rows):
            for j in range(total_columns):
                
                self.e = Entry(self.root, width=20, fg='blue',
                               font=('Arial',10,'bold'))
                
                self.e.grid(row=i+1, column=j+1)
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
if __name__ == "__main__":
    liste = [['RCS Xperion', 'EUW11', 'EVXI1JpKx9XCGODIE6lfFg_w9fFPkVFozuT_JoYiMYMLQXfUzjxBCLauw2fTl5qhkxCqqOqedC6bOQ', 'Pro circuit ', '=IMAGE("https://liquipedia.net/commons/images/thumb/7/77/TFT_Regional_Finals_icon_darkmode.png/42px-TFT_Regional_Finals_icon_darkmode.png")', '/'], ['M8 Jedusor', '12345', 'yTHZ96PDUn1nNK0B6ijXbG0SJ0AdoQcmciUigLZDXmD11a4dVr_fI9ItfsKFDDrtTxPxvj9vQMBo0g', 'Pro circuit ', '=IMAGE("https://liquipedia.net/commons/images/thumb/7/77/TFT_Regional_Finals_icon_darkmode.png/42px-TFT_Regional_Finals_icon_darkmode.png")', '/'], ['MIH TarteMan', 'EUW', 'PrvzoRleTX2Eo6Jc6ZL4CFUJ49Y5rIjD3ErMtm2Iaw3sQcF3yjiQnCZb3COeqJu-bIh_Gpmy5Mp1aA', 'Pro circuit ', '=IMAGE("https://liquipedia.net/commons/images/thumb/7/77/TFT_Regional_Finals_icon_darkmode.png/42px-TFT_Regional_Finals_icon_darkmode.png")', '/'], ['ACE Joe', 'ACE', 'hNzbor8uQMTfj4Iut2qCTPNfX8xz579321qM4AVZHCqLr8SAzYEV0uw803XOrtFucgXWxe5_i6xMow', 'Challenger ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/challenger.png?set=10")', '1189'], ['Failo Potato 小土豆', 'EUTNT', '4upQL9V-Diq6TOl_JnB-NalbcdjckszuEPdDrgCl9rJocaPbahANKNzmIFr6FD91CTOhjOxH1SI5Ow', 'Challenger ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/challenger.png?set=10")', '1038'], ['OSW Watki', '8888', 'qtxthwINrc2xtYkgHLhc_mzLZu4wtF0-LNV5m-18LArGaDpiupDGPATCN2pX2yV3R5WCvr8E3KSjLA', 'Challenger ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/challenger.png?set=10")', '1005'], ['OSW Sadyb', '7940', 'z3FztGEBb0OQphh-mwhwkKO2M2tneyAMC7iiLg1fxBM6HPrttk79zD0RBdfTELnhutTlJZOKgGRooA', 'Challenger ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/challenger.png?set=10")', '970'], ['MIH Armatruc', 'EU1', 'hqBN6toC5fHMwZBdMb14oVM42Yc2XbkVFsFN762WSoPpWF09AOWnaFBHCu1SNdIF0ig7XHL_BAlrvQ', 'Grandmaster ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/grandmaster.png?set=10")', '886'], ['MB ChocooBN', 'GATO', 'uT7SMPgBhtVBELvgc8tWgX9RRoHa3i__JPqaWEdzbGrxTcZkFtNrstSki5dni7j5h9GY48EQu7jz-g', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '532'], ['OSW Pashiorz', '3003', 'I0dZcH7TMVJLgxI4vlPe1vAeb5PNv3T3cUchEYTr8L3rrxb0XorJJyzDCxUbXO6vvCcQZ-e504NFzA', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '508'], ['DrEaMeR', 'EUWFR', 'hPGJcEF8_-vUHn6ZxMJvhRw9xks-UsF9VPvFrJVe1rgDn7l_kWcPqJgKpNBUepfS4sNh_mGiEUUpEQ', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '253'], ['Maidz', 'EUW', '6QP-Twlgl8IHt_61jzXs22P1pWOih6CI27w1l5o9dy7ZVGzFTYOwCBhrSSR1dqQnakIni9XaAtVj4w', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '211'], ['Hopeless', 'emz', '7zKsXL-finozV40c0YIqIi8ZDMjGoSEizEez_mZnKHKrGOeHWU9Zytbqvn0Vi6PQOmF2MX_fBSW_kA', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '147'], ['ACE Maumotte', 'UwU', '5y69nnf0lB1zoV8B55mgFr2msPEQXHehpDLSuq4LCwOAyGOk4gsSQsZ9kFAcp6rvEtQkc18eD79tcg', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '137'], ['cfou et willump', 'EUW', 'qArGE87ZRDY6HoSev666-YTlIMxmAAiTd41hMA0Bc4X16wBckqs1JB_aRk2byty00KDzPx0eyddgLQ', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '65'], ['CAP Coiffure', 'EUW', 'lvBgUSVEubQC2KnYZeX7eQ7xbaFRLkzYt9ilvyvA6DP0R5VMi7EYgUtEzsa-42G7QyHAVgBhhWtPxQ', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '42'], ['MAO THEDONG', 'EUW', 'lXcCrOoNCyqYa6gWxRjtq5l1m2XVCR24EReiUjC7h9hYWC2K0sLTg_lJmYMOzPgRyya7RLmkA43eFA', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '39'], ['CUTE CRAB', 'EUW', 'BQxiNQCqvwSX0tWlMKUYKNPFnbvNvkylClr0e_I3GgW0uckPBq06ycFRVKLevMxMV1y3oDq2egkiBw', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '20'], ['ACE Dufro', 'euwfr', 'lRIGwslblRRSAUz7tJRUUL3BDIfqdHFveW_xke7hpOnnTiFPhD2HaR5TfsoF4YrFRZuFksqf917qpg', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '10'], ['ACE Suberlol', 'EUW', 't9-qz4jrQVh2zlNbsuX2K4s_0VS84WTvbUqQAMJtvDDWfVTbrv8Fv-vblm_Ny0nVC3a7sj3MJ2Oo3g', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '0'], ['Arestidios', 'AAA', 'B0NWmAf1wcammc7cwIGyrwoP3T8llNpMbq_Rl-a4oWWNhJLg2mQJMxkp0r2W4ppgMeipVZ8STBDd5Q', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '0'], ['InPhasis', '5478', 'ntkXclU5ULSs888TvqiMMG2oZIkkz4Uwnw7P0WTZ9VybtedkUAlGK4bMqKkGrO84QgGqtfzjEQpsEQ', 'Master ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/master.png?set=10")', '0'], ['Kinymaru', '1234', 'bWfCDfLMDjghREik6WnGKPIHAra3GvVy3c8i9pw8FLZHcAlvIqmhSL2nulfK0VqHYHIOt8VlurZ3fw', 'Diamond II', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/diamond.png?set=10")', '62'], ['Kekeman77', 'EUW', 'K2HpT4vDDx3QB1wWh92eGX4X2cUNqg3UMwvpD7FPYWvLJp9O6444loyl4G-pFWMNIVnGVAJyDEtbOQ', 'Diamond III', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/diamond.png?set=10")', '66'], ['ShiningBob', 'EUW', '9R-byuxz-BAw6LmyP0pCSea3Nl__iuQbJoodyqDlRdqJ1sHSvzak7Xf__Oze3HhZ0av0K6eLI7Oy0Q', 'Diamond IV', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/diamond.png?set=10")', '0'], ['MB Koddhe', 'SINJ', 'gyJxHis8TosDQjRxKy5GFK_CEzXBMdZ5OvMKpq5FHswSb_5zJCYhl0TjJ_JTdlA-DDhMkimoOjjo8Q', 'Emerald I', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/emerald.png?set=10")', '15'], ['crocob', '0420', 'Pbqwl8FuI2vW92_CXbWq-TmeCcFnCrabiXK5G5_wxn9d8ZzC7Ul03hm0zm1GFpX_pORMKIWfcnTQnw', 'Emerald III', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/emerald.png?set=10")', '63'], ['WILDESTjungle', 'EUW', '_IiFg9cowL-utaDowTKVZ17l6FO1gEOC8zZGIHjssd5nFgNurnjxXfjWgjsr883C4rfA1STtrJn_LQ', 'Emerald III', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/emerald.png?set=10")', '30'], ['Alkora', 'Silk', 'jtfDEw3OXQrm2oX-WF4an49p-4E9YMaBynFIP8Fc5aUXpjiGQbFKLVc4la2TAjNjAzCxn4CZ4lHEvg', 'Emerald III', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/emerald.png?set=10")', '0'], ['ElPando77', 'EUW', '_rmChXGn-PVEQqAEP-q2cTBI00RWzeJi2K80LTob12zAIVTVzfQWA6CrgNt9NFZHqbhgpWlZzr2kPg', 'Emerald IV', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/emerald.png?set=10")', '0'], ['JinSu', 'FRA', 'uf9nvmavutSRQwV73m8MZAbBVQeLLFxC87wI-2gRnuvzrlkqXwdZcRsISO9Mi-d2KLMPcROA3j3wnw', 'Platinum I', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/platinum.png?set=10")', '59'], ['Nalana', 'EUW', 'x1Vax4TZow9bKmVxjtsj2VStUdSdxMdyncWulbIc9vQzF48U3X-H0Q-BMaTfJAG_VEdCyXKG7sPE5w', 'Platinum II', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/platinum.png?set=10")', '95'], ['StarIordFR', 'EUW', 'A5ek-tYSi-qxo0085kQPwcVmE59Bwwk2dJDVAoZaAvpGcSoMBNPLxUF5oPt2YJ4fRGzYD7IirUo-Bw', 'Platinum II', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/platinum.png?set=10")', '46'], ['coroziy', 'EUW', 'ZWnfo0PDDlbJme-JEHMTIPe62VRraDrkRA5hlgIHN-Urt4_XZn_yUFysXnXS7hXnUct90JzFpGd51w', 'Platinum III', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/platinum.png?set=10")', '76'], ['Screwbob', 'EUW', 'FWABP4qqVN3ov_Me8L39zxZep5Rwk5N0NbsSWz2MuSGl_evgalEg3vbB_6nMFIyeTD7A6U2bLlTOVA', 'Platinum IV', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/platinum.png?set=10")', '27'], ['Pocra', '5117', 'bHWbyg-WFfeohO9syygHM-AN-3hfZ8CFPDZc9SQCapnM4TmFyY9E6ql0tRJ9Y8yYyxz9bBkKK6HpRg', 'Platinum IV', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/platinum.png?set=10")', '0'], ['Kyiara', 'EUW', 'TZcHz1M9-p6N7MYmVjBfj66KAuWF-27g3CnbjGxnvM7xMzvN8LW-AoW0cY6g5dzARcWNjaiIH0aZAg', 'Gold III', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/gold.png?set=10")', '87'], ['MasterJujuV', 'None', 'None', 'Unranked ', '=IMAGE("https://cdn.dak.gg/tft/images2/tft/tiers/unranked.png?set=10")', '0']]

    Preview("xx!D3",liste)
 
# create root window
