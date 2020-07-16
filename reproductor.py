# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap
# *****************************************************************#
from PyQt5.QtCore import QSize, QUrl, QAbstractListModel, Q_ARG, pyqtSignal, pyqtSlot, QFileInfo, qFuzzyCompare, QMetaObject, QModelIndex, QObject, Qt, QThread, QTime
# *****************************************************************#
from PyQt5.QtWidgets import QWidget, QListWidget, QFrame, QGridLayout, QSlider, QLabel, QPushButton, QApplication, QMainWindow, QAbstractItemView, QGroupBox, QHBoxLayout, QFileDialog, QListView, QDesktopWidget, QSizePolicy, QToolTip
# *****************************************************************#
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
# *****************************************************************#
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Importamos el archivo que contiene la interfaz
from interfaz.genesis import Ui_Genesis as Genesis


def detalle_tiempo(ms):
    h, r = divmod(ms, 36000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))


class ListaModelo(QAbstractListModel):

    def __init__(self, lista_repro, *args, **kwargs):
        super(ListaModelo, self).__init__(*args, **kwargs)

        self.lista_repro = lista_repro

    def data(self, index, rol):
        if rol == Qt.DisplayRole:
            media = self.lista_repro.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.lista_repro.mediaCount()


class Reproductor(Genesis, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Reproductor, self).__init__()
        self.setupUi(self)

        self.transcurso = 0

        # Centramos la ventana principal
        self.centrar()

        # Inicializamos el modulo QMediaPlayer
        self.media = QMediaPlayer()
        self.media.setVolume(5)
        self.reproducir.setEnabled(False)

        # Setup the playlist.
        self.lista_repro = QMediaPlaylist()
        self.media.setPlaylist(self.lista_repro)

        self.modelo = ListaModelo(self.lista_repro)
        self.lista.setModel(self.modelo)

        self.lista_repro.currentIndexChanged.connect(self.cambio_lista_repro)

        modelo_seleccion = self.lista.selectionModel()
        modelo_seleccion.selectionChanged.connect(self.seleccion_lista_repro)


# **********  Inicializamos el modulo QVideoWidget *******
        self.video = QVideoWidget()

        # Agregamos el modulo QVideoWidget al grid donde se mostrara el video
        self.reproductor.addWidget(self.video)

        # Tambien lo agregamos al modulo QMediaPlayer
        self.media.setVideoOutput(self.video)

        # Conectamos el boton de reproducir con su metodo correspondiente
        self.reproducir.clicked.connect(self.play_video)

        # Conectamos el Skider del tiempo con su metodo correspondiente
        self.tiempo.sliderMoved.connect(self.posicion_establecida)


# ******  Conectamos los estados del modulo QMediaPlayer  *****
# ******  con sus correspondientes metodos                *****
        self.media.stateChanged.connect(self.cambios_video)
        self.media.positionChanged.connect(self.posicion_video)
        self.media.durationChanged.connect(self.duracion_video)
        self.total_duracion = 0

        self.cargar.clicked.connect(self.abrir_archivo)
        # self.marco.origen.connect(self.arrastrar_soltar)

        self.parar.pressed.connect(self.media.stop)
        self.atras.pressed.connect(self.lista_repro.previous)
        self.adelante.pressed.connect(self.lista_repro.next)
        self.volumen.valueChanged.connect(self.media.setVolume)
        self.logo_volumen.clicked.connect(self.silenciar)
        self.lista.doubleClicked.connect(self.play_video)
        self.video.keyPressEvent = self.keyPressEvent

#         ****** Boton de menu ******
        self.lista.setMinimumSize(QSize(0, 0))
        self.lista_visible = True
        self.menu.clicked.connect(self.boton_menu)

        self.setAcceptDrops(True)

        self.primera_reproduccion = True
        self.show()

# ---------------- Inicio de Metodos --------------------------- #

    # Detectamos una tecla presionada
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11 or\
          event.key() == Qt.Key_Escape and self.video.isFullScreen():
            self.fullscreen_change()
        elif event.key() == Qt.Key_Space:
            self.play_video()

    # Pantalla completa
    def fullscreen_change(self):
        if self.video.isFullScreen():
            self.video.setFullScreen(False)
            self.lista.setMinimumSize(QSize(300, 16777215))
        else:
            self.video.setFullScreen(True)

    # Ocultar y mostrar la lista de reproduccion
    def boton_menu(self):
        if self.lista_visible:
            self.lista.setVisible(False)
            size_policy = QSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding
            )
            self.marco.setSizePolicy(size_policy)
            self.lista_visible = False
        else:
            self.lista.setVisible(True)
            self.lista_visible = True

    # Metodos para arrastrar y soltar en la lista de reproduccion
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    # Metodos para arrastrar y soltar en la lista de reproduccion
    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.lista_repro.addMedia(QMediaContent(url))

        self.lista_repro.setPlaybackMode(QMediaPlaylist.Loop)

        self.media.setPlaylist(self.lista_repro)
        self.reproducir.setEnabled(True)
        self.reproductor.removeWidget(self.logo)

        self.media.play()

        self.modelo.layoutChanged.emit()

    # Metodo para cargar el video en cuestion
    def abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(
                self,
                '   Abrir Archivo !!!',
                'C:/Users/Duque/Videos',
                'Solo Video (*.mp4 *.mov *.flv *.mkv *.ts *.mts *.avi);;\
 Solo Audio (*.mp3 *.flac *.m4a *.wav)')

        if archivo != '':
            self.reproductor.removeWidget(self.logo)
            self.primera_reproduccion = False
            self.lista_repro.addMedia(
                QMediaContent(
                    QUrl.fromLocalFile(archivo)
                )
            )
            self.reproducir.setEnabled(True)

        self.modelo.layoutChanged.emit()

    # Metodo para el cambio en la lista de reproduccion
    def cambio_lista_repro(self, i):
        if i > -1:
            ix = self.modelo.index(i)
            self.lista.setCurrentIndex(ix)

    # Metodo para la seleccion en la lista de reproduccion
    def seleccion_lista_repro(self, ix):
        i = ix.indexes()[0].row()
        self.lista_repro.setCurrentIndex(i)

    # Metodo para silenciar el audio o video
    def silenciar(self):
        if self.media.isMuted():
            self.media.setMuted(False)
            icon = QIcon()
            icon.addPixmap(
                QPixmap(":/img/altavoz3.png"),
                QIcon.Normal,
                QIcon.Off
            )
            self.logo_volumen.setIcon(icon)
            self.logo_volumen.setToolTip(' Silenciar ')
        else:
            self.media.setMuted(True)
            icon = QIcon()
            icon.addPixmap(
                QPixmap(":/img/altavoz4.png"),
                QIcon.Normal,
                QIcon.Off
            )
            self.logo_volumen.setIcon(icon)
            self.logo_volumen.setToolTip(' Restablecer Sonido ')

    @pyqtSlot(str)
    def arrastrar_soltar(self, archivo):
        if archivo != '':
            self.media.setMedia(QMediaContent(QUrl.fromLocalFile(archivo)))
            self.reproducir.setEnabled(True)
            self.lista_repro.addMedia(
                QMediaContent(
                    QUrl.fromLocalFile(archivo)
                )
            )
            self.modelo.layoutChanged.emit()

    # Metodo para reproducir el video en cuestion
    def play_video(self):
        if self.primera_reproduccion:
            self.reproductor.removeWidget(self.logo)
            self.primera_reproduccion = False
        if self.media.state() == QMediaPlayer.PlayingState:
            self.media.pause()
        else:
            self.media.play()

    # Metodo que detecta el play y pausa
    def cambios_video(self, state):
        if self.media.state() == QMediaPlayer.PlayingState:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/img/pausa.png"), QIcon.Normal, QIcon.Off)
            self.reproducir.setIcon(icon)
            self.reproducir.setToolTip(' Pausar Video o Audio ')
            QToolTip.setFont(QFont('Cascadia Code PL', 18))
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/img/play.svg"), QIcon.Normal, QIcon.Off)
            self.reproducir.setIcon(icon)
            self.reproducir.setToolTip(' Reproducir Video o Audio ')
            QToolTip.setFont(QFont('Cascadia Code PL', 18))

    def duracion_video(self, duracion):
        # Detecta la duración del vídeo en el slider.
        self.tiempo.setMaximum(duracion)
        self.total_duracion = duracion

    # Metodo que detecta la posiscion del video en el slider
    def posicion_video(self, posicion):
        if posicion >= 0:
            reproduccion = f'{detalle_tiempo(posicion)} ||\
{detalle_tiempo(self.total_duracion)}'
            self.datos.setText(reproduccion)

        self.tiempo.blockSignals(True)
        self.tiempo.setValue(posicion)
        self.tiempo.blockSignals(False)

    # Metodo que detecta la posiscion establecida del modulo QMediaPlayer
    def posicion_establecida(self, position):
        self.media.setPosition(position)

    def errores(self):
        self.reproducir.setEnabled(False)
        # self.lbl.setText("Error: " + self.media.errorString())

    # Metodo para centrar la ventana principal
    def centrar(self):
        ventana = self.frameGeometry()
        centro = QDesktopWidget().availableGeometry().center()
        # print(centro)
        ventana.moveCenter(centro)
        self.move(ventana.topLeft())

if __name__ == '__main__':

    reproductor = QApplication(sys.argv)
    player = Reproductor()
    reproductor.setStyle('Fusion')
    sys.exit(reproductor.exec())
