import yagmail
yag = yagmail.SMTP('pyclassinterface@gmail.com')


def __init__():
    '''
    initializing module
    '''
    return 'Email Handler Service Initialized!'


def sendmail(sender, mailing_list, files_to_attach):
    '''sends the attachments to the recipients provided'''
    yag.send(to=mailing_list, subject="You've got Mail!", 
             contents='Hello, from PyClass.\n' + sender + ' from PyClass has sent you the attached. \n'
                                                                              + 'Happy Learning!\n This is an automatically generated mail. The sender does not support replies.'
                                                                                , attachments=files_to_attach)
    print('Success')
    return True
