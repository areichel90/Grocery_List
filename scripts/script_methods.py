import datetime
import SheetFile as sf
import pandas as pd


def next_friday():
    '''
    Determine the date of next friday
    :return:
    '''
    today = datetime.date.today()
    fri_weekday = 4
    days_to_fri = (fri_weekday - today.weekday() +7) % 7
    # calculate days until next friday - next friday if today is friday
    next_fri_delta = days_to_fri if days_to_fri !=0 else 7
    # determine date of next friday
    next_fri = today + datetime.timedelta(days=next_fri_delta)
    return next_fri


def load_current_list(googlefile:sf.SheetFile)->pd.DataFrame:
    curr_list, time_delta = "", -1e3
    for c, i in enumerate(googlefile.sheetnames):
        try:
            _date = datetime.datetime.strptime(i, "%Y%m%d")
            time_from_next = (_date.date() - next_friday()).days
            # find current list
            if (time_from_next > time_delta) and (time_from_next < 0):
                time_delta = time_from_next
                curr_list = i
            # copy current list
            new_list = getattr(googlefile, curr_list).copy()
            # format last list - keep only non-purchased rows
            new_list = new_list[new_list.Purchased == '']
        except:
            pass
            print(f"{i} is not a valid datetime string")
    return new_list


def create_next_week_list(googlefile:sf.SheetFile, carry_over=True):
    '''
    Create new tab in Google Sheets for upcoming week
        googlefile: google sheets SheetFile obj
        carry_over: process last week's list and carry over any outstanding row
    '''
    # establish timestamp/tab label
    _next_friday = next_friday().strftime("%Y%m%d")
    print(_next_friday)

    # establish base list for next week
    new_list = load_current_list(googlefile) if carry_over else pd.DataFrame()

    # create new tab in googlefile
    googlefile.update_sheet(_next_friday, new_list)
