from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import pafy
import humanize

import urllib.request

##### import UI file #####
FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "layout.ui"))


class mainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        self.handle_buttons()

    def handle_UI(self):
        self.setWindowTitle("Abdelrhman Downloader")
        self.setFixedSize(650, 290)

    def handle_buttons(self):
        self.downloadBtn.clicked.connect(self.download)
        self.browseBtn.clicked.connect(self.handle_browse)
        self.downloadBtn_Yvideo.clicked.connect(self.download_youtube_video)
        self.getVideoBtn.clicked.connect(self.get_youtube_video)
        self.browseBtnVideo.clicked.connect(self.save_browse)
        self.browseBtnPlaylist.clicked.connect(self.save_browse)
        self.downloadBtnPlaylist.clicked.connect(self.playlist_download)




    def handle_browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption = "Save As", directory=".", filter = "All Files (*.*)")
        place_str = str(save_place)
        str_slice = (place_str.split(',')[0])[2:-1]     # split and slice
        self.locationText.setText(str_slice)

    def handle_progress(self, blockNum, blockSize, totalSize):
        read = blockNum * blockSize
        if totalSize > 0:
            percent = (read * 100) / totalSize
            self.progressBar.setValue(percent)
            QApplication.processEvents()


    def download(self):     # url - location - progress
        url = self.urlText.text()
        save_location = self.locationText.text()

        try:
            urllib.request.urlretrieve(url, save_location, self.handle_progress)
        except Exception:
            QMessageBox.warning(self, "Error", "The Download Failed")
            return

        QMessageBox.information(self, "Download Completed", "The Download Finished")
        self.progressBar.setValue(0)
        self.urlText.setText('')
        self.locationText.setText('')

    def save_browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.locationTextVideo.setText(save)
        self.locationTextPlaylist.setText(save)



    def get_youtube_video(self):
        video_url = self.videoUrlText.text()
        v = pafy.new(video_url)

        st = v.videostreams
        for s in st:
            file_size = humanize.naturalsize(s.get_filesize())
            data = '{} {} {} {}'.format(s.mediatype, s.extension, s.quality, file_size)    # format string
            self.comboBox.addItem(data)

    def download_youtube_video(self):
        video_url = self.videoUrlText.text()
        save_location = self.locationTextVideo.text()
        v = pafy.new(video_url)
        st = v.videostreams
        quality = self.comboBox.currentIndex()
        down = st[quality].download(filepath=save_location)

        QMessageBox.information(self, "Download Completed", "The Video Download Finished")
        self.videoUrlText.setText('')
        self.locationTextVideo.setText('')

    def playlist_download(self):
        playlist_url = self.playlistUrlText.text()
        save_location = self.locationTextPlaylist.text()
        playlist = pafy.get_playlist(playlist_url)
        videos = playlist['items']

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        for video in videos:
            p = video['pafy']   # return all info. about video
            best = p.getbest(preftype='mp4')
            best.download()


def main():
    app = QApplication(sys.argv)
    window = mainApp()
    window.show()
    app.exec_()     #infinite loop

if __name__ == '__main__':
    main()