#אחמד טללקה-208900027  ו- ואסילה אלהואשלה -315589432
import PySimpleGUI as sg
from PySimpleGUI import Button,Column,Frame , InputText,Text,Window
from password_strength import password_rules
from bloomfilter import BloomFilter



sg.theme('BlueMono')  # Add a little color to your windows

# create the main window parts
main_title_col = [sg.Text('      Bloom Filter & Password Strength ', size=(40, 1), font=("Helvetica", 20))]

col1 = Column([
    [Frame('New Password:',
           [[Button('Insert new password', enable_events=True), InputText(key='-NEW-PASSWORD-', size=(15, 1))],
            [Button('Show complete password strength analysis', enable_events=True)]], )]
])
col2 = Column([
    [Frame('Bloom Filter:',
           [[Text('#Array_Bits'), sg.InputText('0', key='-K-', size=(5, 1)), Text('#Size of Hashs'),
             InputText('0', key='-N-', size=(5, 1)), Button('Enter', enable_events=True)],
            [Button('           Show filter statistics           ', enable_events=True)], ], )]
])
col3 = Column([
    [Frame('Password Check:',
           [[Text('Insert password to check'), InputText(key='-PASSWORD-TO-CHECK-', size=(15, 1))],
            [Button('        Check the presence of the password      ', enable_events=True)]], )]
])

col4 = Column([
    [Frame('Filter Visualization', [[Button('    Show full visual of the filter    ', enable_events=True)],
                                    [Button('    Show/update full dictionary word of the filter    ', enable_events=True)]], )]

])

layout = [main_title_col, [col1, col2], [col3, col4]]

# Create the Window
main_window = Window(' Bloom Filter & Password Strength Checker', layout)

redundency_count = 0
false_positive=0

# set default values of the bfilters.

# Event Loop to process "events"
while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Enter':
         Array_size = int(values['-K-'])
         sizeofhashs = int(values['-N-'])
         if Array_size>0 and  sizeofhashs>0:
          bloomf = BloomFilter(Array_size, sizeofhashs)
          confirm = sg.PopupOKCancel( "Are you sure you want to change\Add filter parameters?\nThis operation resets the filters and dictionaries",title='Confirm')
          sg.PopupOKCancel("Update successfully")
          if confirm == 'OK':
              redundency_count = 0
              false_positive = 0
          else:
            sg.PopupError("Update unsuccessfully , Try again Error inputs  ! ")
    elif event=="    Show/update full dictionary word of the filter    ":
        try:
            dict1= {bloomf.dits[i]: i for i in range(0, len(bloomf.dits) ) }
            dict_bin_col = Column([
                [Frame('dictionary words:',
                       [
                           [sg.Text(dict1, size=(64, 32))]
                       ],

                       )],

            ])


            curr_ok_col = [Button('Ok', enable_events=True)]
            col1 = Column([
                [Frame('New Password:',
                       [[Button('Insert  password to remove from dictionary', enable_events=True),
                         InputText(key='-del-', size=(15, 1))],
                        [Button('remove', enable_events=True)]], )]
            ])

            filter_visual_layout = [[dict_bin_col,col1],curr_ok_col]

            filter_visual_window = Window('Full filter ', filter_visual_layout)

            while True:
                ana_event, ana_values = filter_visual_window.read()
                if ana_event == sg.WIN_CLOSED or ana_event == 'Ok':
                    break
                elif ana_event == 'remove':
                    try:
                        if ana_values.get('-del-') in dict1:
                            del dict1[values['-NEW-PASSWORD-']]
                            bloomf.dits.remove(ana_values.get('-del-'))
                            print(bloomf.dits)
                            sg.PopupOK("Update successfully")
                        else:
                            sg.PopupError("Update was unsuccessfully The Password not found ! , try again !  ")
                    except:  # invalid data or mistake
                        pass
            filter_visual_window.close()
            pass
        except:
            pass
    elif event == 'Insert new password':
        try:
            if len(values['-NEW-PASSWORD-'])!=0 :
                if bloomf.check_if_add(values['-NEW-PASSWORD-']):
                    sg.PopupError("inserted not successfully  This word[ "+str(values['-NEW-PASSWORD-'])+" ] in bloom filter , Try Again!")
                else:
                 bloomf.add(values['-NEW-PASSWORD-'])
                 sg.PopupOK("The password has been inserted successfully [ we Found overlap "+str(bloomf.c)+"bits]")
                if bloomf.c==sizeofhashs:
                  sg.popup_ok("ohh ! , we Found False positive ")
                  false_positive+=1
            else:
                 sg.PopupError("inserted not successfully  Null input, Try Again!")
        except:
            pass
    elif event == 'Show complete password strength analysis':
        try:
            if len(values['-NEW-PASSWORD-'])==0:
                sg.popup_error("Null input :(")

            else:
                weaknesses, strengths, score, popup_msg, ruls_violation = password_rules(values['-NEW-PASSWORD-'])
                headings = ['property', 'exists','socre']
                sg.PopupOK(popup_msg)
                subject_pass_to_analysis_col = [
                   sg.Text('                     Password: {}'.format(values['-NEW-PASSWORD-']), size=(30, 1),
                        font=("Helvetica", 25))]

                strength_analysis_col = Column([
                   [Frame('Password Strength Parameters',
                       [
                           [sg.Table(values=strengths[1:][:], max_col_width=60, headings=headings,
                                     auto_size_columns=True,
                                     display_row_numbers=True,
                                     justification='left',
                                     num_rows=14,
                                     alternating_row_color='lightyellow',
                                     key='-STRENGTH-TABLE-',
                                     row_height=35,
                                     )]
                       ],
                       )]
                ])
                ok_col = [Button('Ok', enable_events=True),
                      Text("Password strength: {}".format(score))]
                analysis_layout = [subject_pass_to_analysis_col, [strength_analysis_col], ok_col]
                analisys_window = Window('Password Strength Analysis', analysis_layout)

            while True:
                ana_event, ana_values = analisys_window.read()
                if ana_event == sg.WIN_CLOSED or ana_event == 'Ok':
                    break
            analisys_window.close()
            pass
        except:
            pass
    elif event == '        Check the presence of the password      ':
        try:
            if bloomf.check(values['-PASSWORD-TO-CHECK-']):
                 popup_txt = 'The password is in dictionary '
                 sg.PopupOK(popup_txt)
            else:
                sg.PopupError('The password is not present in any dictionary')
        except:  # invalid data or mistake
            pass
    elif event == '           Show filter statistics           ':
        try:
            insert_count = bloomf.get_element_count()
            marked_bits_dict1 = bloomf.get_marked_bits_count()
            sg.PopupOK('Insert Counter: {}\n\nMarked Bits in filter  : {}\n\nFalse positive Counter : {}\n'.format(
                    insert_count, marked_bits_dict1, false_positive))
        except:
            pass
    elif event == '    Show full visual of the filter    ':
        try:
            filter_visual_title_col = [
                sg.Text('Full visualization of the filters', size=(30, 1), font=("Helvetica", 25))]
            dict1_bits = str(bloomf.get_bit_array().unpack(zero=b'0', one=b'1')).replace('b', " ").replace("'", " ")
            dict1_hexa = bytearray(bloomf.get_bit_array()).hex()

            dict_bin_col = Column([
                [Frame('Bloom Filter 1: Binary',
                       [
                           [sg.Text(dict1_bits, size=(64, 32))]
                       ],
                       )],

            ])

            curr_ok_col = [Button('Ok', enable_events=True)]

            filter_visual_layout = [filter_visual_title_col, [dict_bin_col], curr_ok_col]

            filter_visual_window = Window('Full filter visual', filter_visual_layout)

            while True:
                ana_event, ana_values = filter_visual_window.read()
                if ana_event == sg.WIN_CLOSED or ana_event == 'Ok':
                    break
            filter_visual_window.close()
            pass
        except:
            pass

main_window.close()

c = str(bloomf.get_bit_array().unpack(zero=b'0', one=b'1')).replace('b', "").replace("'", "")