import logging

import PySimpleGUI as sg

from .exceptions import ClosedError


logger = logging.getLogger(__name__)


class GUI:
    def __init__(self, workers):
        self.workers = workers
        self.layout = [[sg.Text("Enter links below:")],
                       [sg.Multiline(size=(70, 20), key='URLS')],
                       [sg.Text(size=(40,1), key='STATUS')],
                       [sg.FolderBrowse('Choose download folder'), sg.Text(size=(50, 0), key='FOLDER', text='Choose download folder...')],
                       [sg.Button('Ok'), sg.Button('Quit')]]
        self.window = sg.Window('domascraper', self.layout)

    def run(self):
        while True:
            try:
                self.process_event()
            except ClosedError:
                self.window.close()
                break
            except Exception as exc:
                logger.error(exc, exc_info=True)
                sg.Popup(f'{exc}', title='Error')

    def process_event(self):
        window = self.window

        # Read event - raise ClosedError on close
        logger.info('Waiting for event...')
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            raise ClosedError
        logger.info('Got event: %s', (event, values))

        return

        folder = window['FOLDER'].get()
        if folder == 'Choose download folder...':
            raise RuntimeError('Please choose download folder')
        if not os.path.isdir(folder):
            os.makedirs(folder, exist_ok=True)

        os.chdir(folder)

        urls = list(filter(bool, values['URLS'].split('\n')))
        if not urls:
            raise RuntimeError('Please enter ArtStation artwork URLs')

        for url in urls:
            if not url.startswith('https://www.artstation.com/artwork/'):
                raise RuntimeError(f'Not an ArtStation URL: {url}')

        n = len(urls)
        logger.info('Downloading images [%d]...', n)
        window['STATUS'].update(f'Downloading images from URLs... [0/{n}]')
        window.read(timeout=0.001)
        documents = []
        for i, _ in enumerate(map(pull_images, urls)):
            logger.info('%d...', i+1)
            window['STATUS'].update(f'Downloading images from URLs... [{i+1}/{n}]')
            window.read(timeout=0.001)

        window['STATUS'].update(f'Download finished :^)')
