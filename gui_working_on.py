# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:16:52 2022

@author: Michael P. Mariani PhD

################### COPYRIGHT ######################
#Copyright (c) 2023, Mariani Systems LLC
#  All rights reserved.
#
#This source code is licensed under the license found in the
#LICENSE file in the root directory of this source tree. 
####################################################

"""

import PySimpleGUI as sg
#import PySimpleGUIQt as sg

#PySimpleGuiQt is having dev issues it seems
#https://github.com/PySimpleGUI/PySimpleGUI/issues/5244
#I believe I have to choose one of the above
#or ":ImportError: 
#    Importing PySide2 disabled by IPython, which has
#    already imported an Incompatible QT Binding: pyqt5"

filePath='C:\\Users\\Mike_2\\Desktop\\my_stuff\\project_x'+'\\projext_x.py'

#set the theme for the screen/window
sg.theme('SandyBeach')
#define layout
layout=[[sg.Text('Choose Implementation',
                  size=(100, 1), 
                  font='Lucida',
                  justification='left')],
        [sg.Combo(['USA',
                    'EU',
                    'NATO', 
                    'OTHER'],
                   default_value='USA',
                   key='board',
                  size=(100, 10))],
        [sg.Text('Choose System ',
                  size=(100, 1), 
                  font='Lucida',
                  justification='left')],
        [sg.Combo(['Imperial',
                    'Metrix'],
                   default_value="imperial",
                   key='dest',
                   size=(100, 10))],
        [sg.Text('Choose Core',
                  size=(100, 1), 
                  font='Lucida',
                  justification='left')],
        [sg.Listbox(
            values=['Army', 
                    'Airforce', 
                    'Navy',
                    'Marines', 
                    'Coast Guard'], 
            select_mode='extended', 
            key='fac', 
            size=(100, 10))],
        [sg.Button('Next', 
                    font=('Times New Roman',20),
                    size=(20, 2)),
         sg.Button('CANCEL', 
                    font=('Times New Roman',20),
                    size=(20, 2))]]

#Define Window
win=sg.Window('TargetSys V1.0',layout).Finalize()
win.Maximize()
#Read  values entered by user
e,v=win.read()
#close first window
#win.close()
#access the selected value in the list box and add them to a string
strx=""
for val in v['fac']:
    strx=strx+ " "+ val+","
        
#display string in a popup         
sg.popup('Options Chosen',      
            'Implementation: '+ 
            v['board'] + 
            '\nSystem: ' + 
            v['dest'] +
            '\nCore(s): ' +
            strx[1:len(strx)-1] )

win.close()
#win.clear()
#win.refresh()

############################################################
############################################################
############################################################
############################################################
############################################################

#set the theme for the screen/window

sg.theme("LightBlue")

#define layout

col1=[[sg.Text("Relative assesssed total",
                 font='Lucida',
                 size=(25,2))],
         [sg.Slider(orientation ='horizontal', 
                   key='Slider1', 
                   range=(0,100))],
         [sg.Text("Personal assessed total", 
                 font='Lucida',
                 size=(25,2))],
         [sg.Slider(orientation ='horizontal', 
                   key='Slider2',
                   range=(0,100))],
         [sg.Text("Equipment assessed total", 
                  font='Lucida',
                  size=(25,2))],
         [sg.Slider(orientation = 'horizontal', 
                   key='Slider3',
                   range=(0,100))]]

col2=[[sg.Input(key='sl1',
                  size=(6, 3))],
       [sg.Input(key='sl2',
                  size=(6, 3))],
       [sg.Input(key='sl3',
                  size=(6, 3))]]

col3 = [[sg.Button('Button 1'),] for i in range(10)]
col4 = [[sg.Slider((1,10)) for i in range(10)]]

num_buttons = 2
layout2 = [[[sg.Column(col1),
       sg.Column(col2)],       
        [sg.Spin(values=['Air',
                         'Sea',
                         'Land'],
                 size=(40,20), 
                 key='spnMnt')],
        [sg.Submit(key='btnSubmit',
                   size=(20,5)), 
         sg.Cancel(size=(20,5))],
        [sg.ProgressBar(50, 
                        orientation='h', 
                        size=(40, 20), 
                        border_width=4, 
                        key='progbar',
                        bar_color=['Red','Green'])]],
[[sg.Text('Your typed chars appear here:'), 
           sg.Text('', key='_OUTPUT_')],
            [sg.Input(do_not_clear=True, key='_IN_')],
            *[[sg.Button('Button'),] for i in range(num_buttons)],
            [sg.Slider(range=(1,100), 
                       text_color='white', 
                       orientation='h', 
                       key='SLIDER'),
            sg.Drop(('Choice 1', 'choice 2'), 
                    key='DROP'), 
            sg.Stretch()],
            [sg.Button('Detailed Info'), 
             sg.Button('Delete Rows' ), 
             sg.Button('Disappear'),
             sg.Button('Reappear')],
            [sg.Button('Show Sliders'),
             sg.Button('Show Buttons'),
             sg.Button('Hide Sliders'),
             sg.Button('Hide Buttons'),
             sg.Button('Exit')],
            [sg.Column(col3, 
                       key='col3', 
                       visible=False),
             sg.Column(col4, 
                       key='col4', 
                       visible=False)]
          ]]

#window = sg.Window('Force Allocation', 
#                 resizable=True).Layout(layout2).Finalize()

#Define Window
window=sg.Window('TargetSys V1.0', 
                 layout2,
                 resizable=True)
window.Finalize()
window.Maximize()

#Read  values entered by user
event,values=window.read()

window.Element('SLIDER').Update(visible=False)
window.Element('SLIDER').Update(visible=False)
window.Refresh()
window.Refresh()

window['sl1'].update(int(values['Slider1']))
window['sl2'].update(int(values['Slider2']))
window['sl3'].update(int(values['Slider3']))

window.Size = window.Size

num_buttons = 2
while True:             # Event Loop
    event, values = window.Read()
    print(event, values, window.Size)
    if event is None or event == 'Exit':
        break
    
    if event == 'Detailed Info':
        
        layout3 = [[sg.Button('Option %s'%i) 
                   for i in range(num_buttons)],
                  [sg.Button('Add Rows'), 
                   sg.Button('Delete Rows'), 
                   sg.Button('Exit')]]
        
        window1 = sg.Window('Window Title', 
                            no_titlebar=True).Layout(layout3)
        # window.Close()
        # window = window1
        window1.Read(timeout=0)
        
    if event == 'btnSubmit':
        event,values=window.read()
        i=int(values['sl1'])
        k=int(values['sl2'])
        j=int(values['sl3'])
        window['btnSubmit'].set_focus()
        val=0
        for i in range(k):
            event, values = window.read(timeout=100)
            # update prograss bar value
            val=val+100/(k-i)    
            window['progbar'].update_bar(val)
        
            window.Refresh()
            window.Refresh()
            window.Size =  window.Size

            print(window.Size[0])
    
    elif event == 'Hide Buttons':
        window.Element('SLIDER').Update(visible=False)
        window.Element('col3').Update(visible=False)
    elif event == 'Show Buttons':
        window.Element('SLIDER').Update(visible=True)
        window.Element('col3').Update(visible=True)
    elif event == 'Hide Sliders':
        window.Element('col4').Update(visible=False)
        window.Element('DROP').Update(visible=False)
    elif event == 'Show Sliders':
        window.Element('col4').Update(visible=True)
        window.Element('DROP').Update(visible=True)

window.close()

# =============================================================================
# def make_win1():
#     layout = [[sg.Text('This is the FIRST WINDOW'), 
#                sg.Text('      ', 
#                        k='-OUTPUT-')],
#               [sg.Text('Click Popup anytime to see a modal popup')],
#               [sg.Button('Launch 2nd Window'), 
#                sg.Button('Popup'), 
#                sg.Button('Exit')]]
#     return sg.Window('Window Title', 
#                      layout, 
#                      location=(800,600), 
#                      finalize=True)
# def make_win2():
#     layout = [[sg.Text('The second window')],
#               [sg.Input(key='-IN-', enable_events=True)],
#               [sg.Text(size=(25,1), k='-OUTPUT-')],
#               [sg.Button('Erase'), sg.Button('Popup'), sg.Button('Exit')]]
#     return sg.Window('Second Window', layout, finalize=True)
# window1, window2 = make_win1(), None        # start off with 1 window open
# while True:             # Event Loop
#     window, event, values = sg.read_all_windows()
#     if event == sg.WIN_CLOSED or event == 'Exit':
#         window.close()
#         if window == window2:       # if closing win 2, mark as closed
#             window2 = None
#         elif window == window1:     # if closing win 1, exit program
#             break
#     elif event == 'Popup':
#         sg.popup('This is a BLOCKING popup',
#                  'all windows remain inactive while popup active')
#     elif event == 'Launch 2nd Window' and not window2:
#         window2 = make_win2()
#     elif event == '-IN-':
#         window['-OUTPUT-'].update(f'You enetered {values["-IN-"]}')
#     elif event == 'Erase':
#         window['-OUTPUT-'].update('')
#         window['-IN-'].update('')
#         
# window.close()
# =============================================================================
