import gspread
import pandas as pd
import numpy as np
import os, glob


class SheetFile():
    def __init__(self, sheetname:str, load_all_on_init=True)->None:
        self.verbose = True
        # authenticate and open google sheets file
        self.authenticate_and_open(fname=sheetname)

        # determine all sheet name(s)
        self._refresh_worksheets()
        if self.verbose: print(f"Sheets File Opened.  Found {len(self.sheetnames)} worksheets: {self.sheetnames}")

    def _refresh_worksheets(self, load_all=True)->None:
        """ (private) method to refresh the class 'sheetnames' attr """
        self.sheetnames = [i.title for i in self.sheetfile.worksheets()]
        if load_all:
            # load all tabs as pandas dataframe
            for c,_sheet in enumerate(self.sheetnames):
                self.load_worksheet(_sheet)

    def authenticate_and_open(self, fname:str, verbose:bool=True) -> gspread.spreadsheet.Spreadsheet:
        """ load service account credentials and open the Google Sheets file (fname) """
        # authenticate - grocery-list-admin@grocery-list-482415.iam.gserviceaccount.com
        creds = glob.glob(os.path.join(os.path.dirname(__file__), "..", "keys", "*"))
        gc = gspread.service_account(filename=creds[0])
        # open
        sh = gc.open(fname)
        self.sheetfile = sh
        if self.verbose: print(f"Successfully Loaded {fname} Google Sheets")

    def update_sheet(self, sheetname:str, df_update:pd.DataFrame)->None:
        """ load new dataframe into given tab (sheetname) of open Google Sheets file """
        to_update = self.sheetfile.worksheet(sheetname) if sheetname in self.sheetnames else \
            self.sheetfile.add_worksheet(sheetname, rows=10, cols=4)
        _update = [df_update.columns.tolist()] + df_update.fillna("UNK").values.tolist()
        to_update.update(_update)
        if self.verbose: print(f">>> Updated {sheetname} tab successfully.")

        # update sheetnames attr
        self._refresh_worksheets()
        return True

    def delete_sheet(self, sheetname:str):
        to_delete = self.sheetfile.worksheet(sheetname)
        self.sheetfile.del_worksheet(to_delete)
        if self.verbose: print(f">>> Deleted {sheetname} tab successfully.")

        # update sheetnames attr
        self._refresh_worksheets()
        return True

    def load_worksheet(self, sheetname:str, set_attr=True)->pd.DataFrame:
        _df = pd.DataFrame(self.sheetfile.worksheet(sheetname).get_all_records())
        if setattr: setattr(self, sheetname, _df)
        return _df

