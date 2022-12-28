import pyautogui
import pandas as pd
import sys

# global variables
programme_exit = False

# import csv
flows_df = pd.read_csv('flows.csv')
actions_df = pd.read_csv('flows.csv')

def programme_exit_10_s():
    print('')
    print('Programme will shut down in 10 seconds')
    time.sleep(10)
    sys.exit('')

def clean_string(string):

    return string.lower().lstrip(' ','').rstrip(' ','')


def execute_action(action_name):

    # find action in df

    try:
        i = actions_df.loc[actions_df['name']==action_name].index.tolist()[0]
    except:
        print(f'ERROR: Cannot find action "{action_name}" in actions.csv')

        programme_exit_10_s()

    action = clean_string(actions_df['action'][i])
    location_method = clean_string(actions_df['location_method'][i])
    x = int(clean_string(actions_df['x'][i]))
    y = int(clean_string(actions_df['y'][i]))
    image_name = clean_string(actions_df['image_name'][i])
    write_text = clean_string(actions_df['write_text'][i])

    if action == 'move':

        if location_method == 'absolute coordinates':

            pyautogui.moveTo(x,y, duration = 1)

        elif location_method == 'relative coordinates':





    elif action == 'click':

        pyautogui.moveTo(x,y, duration = 1)


    elif action == 'right click':

        print('EXIT: rigth click action not supported yet. contact developer')
        programme_exit_10_s()


    elif action == 'write':






    elif action == 'special keys':



    elif action == 'pause':




    elif action == 'screenshot':









    else:
        print(f'ERROR: Unsoported action: "{action}" for action named: {action_name}')
        programme_exit_10_s()







# Run main loop

while True:

    mode_raw = input('\nChoose programme mode: flow/action/coordinates/exit \n\nflow: run a flow that you have previously entered in flows.csv \naction: run a specific action you have previously entered in actions.csv \ncoordinates: enter the coordinates and the programme will move your mouse to that point\nexit: exit the programme\n\n>>')

    print('')

    mode = mode_raw.replace(' ').lower()

    if mode == 'flow':

        # enter flow name

        # confirm

        # execute actions on loop for every row of associated data table


    elif mode == 'action':

        # enter action name

        # execute that action


    elif mode == 'coordinates':

        while True:
        
            coordinates_raw = input('Enter "get" to get the coordinates of the mouse\nEnter coordinates in the format of: "x,y"\nEnter "back" to go back to main menu, or "exit" to end the programme\n>>')

            coordinates = coordinates_raw.replace(' '.'').lower()
        
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

