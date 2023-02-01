import PySimpleGUI as sg


def popup(title: str, message: str, action_button):
    """
        this function can be used to show any kind of popup
        title: title of the popup
        message: message inside the popup
        action_button: any action button to be incorporated in the popup, if needed
    """
    sg.theme('LightGrey4')
    layout = [[sg.Text(message)]]

    if action_button is not None:
        layout.append(action_button)

    layout.append([sg.Button('Ok')])

    window = sg.Window(title, layout, keep_on_top=True, finalize=True)

    return window
