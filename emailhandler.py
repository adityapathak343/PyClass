import yagmail
yag = yagmail.SMTP('adityapathak343@gmail.com')


def __init__():
    '''
    initializing module
    '''
    return 'Email Handler Service Initialized!'


def sendmail(sender, mailing_list, files_to_attach):
    yag.send(to=mailing_list, contents='Hello, from PyClass. ' + sender + 'from PyClass has sent you the attached.'
                                                                              + 'Happy Learning!\n'
                                                                                , attachments=files_to_attach)
