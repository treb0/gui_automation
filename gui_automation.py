import pyautogui
import pandas as pd
import numpy as np
import sys
import time
from datetime import datetime
import os

# global variables
programme_exit = False

def programme_exit_10_s():
    print('')
    print('Programme will shut down in 10 seconds')
    time.sleep(10)
    sys.exit('')

def any_key_to_exit():
    print('')
    any_key = input('Press enter to exit programme')
    sys.exit('')

def clean_string(string):

    if type(string) == str:

        return string.lower().lstrip(' ').rstrip(' ')

    else:
        
        if np.isnan(string):

            return ''

        else:

            return float(string)
        


def execute_action(data_i
                  ,flow_i
                  ,flow_row
                  ,data_row):

    print('')

    action = clean_string(flow_row['action'])
    location_method = clean_string(flow_row['location_method'])
    before_sleep_s = clean_string(flow_row['before_sleep_s'])
    after_sleep_s = clean_string(flow_row['after_sleep_s'])
    x = clean_string(flow_row['x'])
    y = clean_string(flow_row['y'])
    image_name = clean_string(flow_row['image_name'])
    text = clean_string(flow_row['text'])
    interval_s = clean_string(flow_row['interval_s'])
    if interval_s == '': interval_s = 0.25
    
    # detect if text is data.csv data
    if '{' in text:
        data_column = text.replace('{','').replace('}','')
        text = str(data_row[data_column])


    # before sleep
    if before_sleep_s != '':

        print(f'''data_row: {data_i+1}, flow_row:{flow_i+1} - action: {action} - executing before sleep of {before_sleep_s}''')
        time.sleep(int(before_sleep_s))


    # print executing action

    if action not in ('','sleep'):

        print(f'''data_row: {data_i+1}, flow_row:{flow_i+1} - action: {action} - executing action''')


    # execute action logic

    if action == 'move':

        if location_method == 'absolute coordinates':

            pyautogui.moveTo(x,y, duration = 1)

        elif location_method == 'relative coordinates':

            pyautogui.move(x,y, duration = 1)

        elif location_method == 'image':

            # CODE ASDF

            print('CODE Not built yet')
            any_key_to_exit()

        else:
            if location_method == '': error_msg = 'empty'
            else: error_msg = 'unsopported'
            print(f'''ERROR: {error_msg} location_method: {location_method},, for row: {i} of flow: {flow_name}.csv''')
            any_key_to_exit()

            



    elif action == 'click':

        pyautogui.click(x
                       ,y
                       ,button='left'
                       ,clicks = 1
                       ,interval=interval_s
                       )


    elif action == 'right click':

        pyautogui.click(x
                       ,y
                       ,button='right'
                       ,clicks = 1
                       ,interval=interval_s
                       )


    elif action == 'write':

        pyautogui.write(text
                       ,interval=interval_s
                       )

    elif action == 'hotkey':

        for t in text.split(','):

            pyautogui.hotkey(t)


    elif action == 'sleep': 
        # ya se corrió en before_sleep_s
        pass 

    elif action == 'screenshot':

        today_str = datetime.now().strftime("%Y_%m_%d")

        now_str = datetime.now().strftime("%Y_%m_%d__%H_%M")

        floder_path = f'screenshots/{today_str}'

        # create today's folder if it does not exist
        if not os.path.exists(floder_path):
            os.makedirs(floder_path)

        # capture and save screenshot

        pyautogui.screenshot(f'{floder_path}/{now_str}__{data_i}.png')


    else:
        print(f'ERROR: Unsoported action: "{action}"')
        any_key_to_exit()


    # after sleep

    if after_sleep_s != '':

        print(f'''data_row: {data_i+1}, flow_row:{flow_i+1} - action: {action} - executing after sleep of {after_sleep_s}''')
        time.sleep(int(after_sleep_s))





# Run main loop

flow_df = []
data_df = []

while True:

    mode_raw = input('\nChoose programme mode: flow/coordinates/exit \n\nflow: run a flow that you have previously entered in flows.csv \ncoordinates: enter the coordinates and the programme will move your mouse to that point\nexit: exit the programme\n\n>>')

    print('')

    mode = mode_raw.replace(' ','').lower()

    if mode == 'flow':

        # enter flow name
        print('')
        flow_name_raw = input('Enter flow name: ')

        flow_name = flow_name_raw.lstrip(' ').rstrip(' ').replace('.csv','')

        # Get flow csv

        flow_df = pd.read_csv(f'flows/{flow_name}.csv')

        # Get data csv

        if flow_df['action'][0] == 'data csv':

            data_df = pd.read_csv(f'''data/{flow_df['location_method'][0]}''')
            has_data_csv = True
            flow_iterations = len(data_df)

        else: 

            has_data_csv = False
            flow_iterations = 1


        # execute actions on loop for every row of associated data table

        for data_i in range(flow_iterations):

            data_row = data_df.loc[data_i]

            for flow_i,flow_row in flow_df.iterrows():

                if has_data_csv & (flow_i == 0): continue
                    
                execute_action(data_i
                              ,flow_i
                              ,flow_row
                              ,data_row)



    elif mode == 'coordinates':

        while True:
        
            coordinates_raw = input('Enter "get" to get the coordinates of the mouse\nEnter coordinates in the format of: "x,y"\nEnter "back" to go back to main menu, or "exit" to end the programme\n>>')

            coordinates = coordinates_raw.replace(' ','').lower()
        
            if coordinates == 'exit':
                
                programme_exit = True
                break

            elif coordinates == 'get':

                position = pyautogui.position()

                print(f'x: {position.x}')
                print(f'y: {position.y}')
                
            else:
                
                x = int(coordinates.split(',')[0])
                y = int(coordinates.split(',')[1])
                
                print(f'x: {x}')
                print(f'y: {y}')
                
                pyautogui.moveTo(x,y, duration = 1)

                print('')


    elif mode == 'exit':
        print('EXIT: Programme exited by user')
        break




    else:
        print(f'ERROR: You entered: "{mode_raw}",, but only one of the following is acceptable: flow/action/coordinates/exit.')

    if programme_exit:
        print('')
        print('EXIT: Programme exited by user')
        break

