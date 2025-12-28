import gspread as gs
import pandas as pd
import SheetFile as sf
import script_methods as sm
import numpy as np
import os, sys, glob


def main(fname):
    # instantiate google sheet obj
    google_sheet = sf.SheetFile(sheetname=fname)
    print(vars(google_sheet))

if __name__=="__main__":
    ### globals ###
    fname = "Groceries"
    main(fname)