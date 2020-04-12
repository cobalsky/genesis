# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap

from PyQt5.QtCore import QSize, QUrl, QAbstractListModel, Q_ARG, pyqtSignal, pyqtSlot, QFileInfo, qFuzzyCompare, QMetaObject, QModelIndex, QObject, Qt, QThread, QTime

from PyQt5.QtWidgets import QWidget, QListWidget, QFrame, QGridLayout, QSlider, QLabel, QPushButton, QApplication, QMainWindow, QAbstractItemView, QGroupBox, QHBoxLayout, QFileDialog, QListView, QDesktopWidget, QToolTip

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

from PyQt5.QtMultimediaWidgets import QVideoWidget

# Importamos el archivo que contiene las imagenes del reproductor
from interfaz.imagenes import *
from interfaz.arrastrar_soltar import *


class Genesis(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("Genesis")
        self.resize(814, 600)
        font = QFont()
        font.setFamily("Cascadia Code PL")
        font.setPointSize(16)
        self.setFont(font)
        

        self.contenedor = QWidget(self)
        self.contenedor.setObjectName("contenedor")
        self.grid_central = QGridLayout(self.contenedor)
        self.grid_central.setObjectName("grid_central")

        self.marco = QFrame(self.contenedor)
        self.marco.setStyleSheet("background-color: teal;")
        self.marco.setFrameShape(QFrame.Panel)
        self.marco.setFrameShadow(QFrame.Sunken)
        self.marco.setObjectName("marco")
        self.grid = QGridLayout(self.marco)
        self.grid.setObjectName("grid")

        self.reproductor = QGridLayout()
        self.reproductor.setObjectName("reproductor")

        self.logo = QLabel(self.marco)
        self.logo.setMinimumSize(16777215, 16777215)
        self.logo.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(22)
        self.logo.setFont(font)
        self.logo.setFrameShape(QFrame.StyledPanel)
        self.logo.setPixmap(QPixmap(":/img/genesis.jpg"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.reproductor.addWidget(self.logo, 0, 0, 1, 1)
        self.grid.addLayout(self.reproductor, 0, 0, 1, 1)
        self.grid_central.addWidget(self.marco, 1, 0, 1, 1)

        self.lista = QListView(self.contenedor)
        self.lista.setMinimumSize(QSize(300, 16777215))
        self.lista.setMaximumSize(QSize(300, 16777215))
        self.lista.setStyleSheet("color: rgb(255, 255, 255);\n"
        "background-color: darkred;")
        self.lista.setObjectName("lista")
        self.grid_central.addWidget(self.lista, 1, 1, 1, 1)

        self.box_controles = QGroupBox(self.contenedor)
        self.box_controles.setMaximumSize(QSize(16777215, 122))
        self.box_controles.setObjectName("box_controles")
        self.grid_controles = QGridLayout(self.box_controles)
        self.grid_controles.setObjectName("grid_controles")

        self.parar = QPushButton(self.box_controles)
        self.parar.setMaximumSize(QSize(50, 109))
        self.parar.setToolTip('Detener Reproduccion')
        icon = QIcon()
        icon.addPixmap(QPixmap(":/img/stop.svg"), QIcon.Normal, QIcon.Off)
        self.parar.setIcon(icon)
        self.parar.setIconSize(QSize(48, 29))
        self.parar.setFlat(True)
        self.parar.setObjectName("parar")
        self.grid_controles.addWidget(self.parar, 0, 1, 1, 1)

        self.adelante = QPushButton(self.box_controles)
        self.adelante.setMaximumSize(QSize(50, 109))
        self.adelante.setToolTip('Adelantar a la siguiente cancion')
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/img/next.svg"), QIcon.Normal, QIcon.Off)
        self.adelante.setIcon(icon1)
        self.adelante.setIconSize(QSize(48, 29))
        self.adelante.setFlat(True)
        self.adelante.setObjectName("adelante")
        self.grid_controles.addWidget(self.adelante, 0, 3, 1, 1)

        self.reproducir = QPushButton(self.box_controles)
        self.reproducir.setMaximumSize(QtCore.QSize(50, 109))
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/img/play.svg"), QIcon.Normal, QIcon.Off)
        self.reproducir.setIcon(icon2)
        self.reproducir.setIconSize(QSize(48, 29))
        self.reproducir.setFlat(True)
        self.reproducir.setObjectName("reproducir")
        self.grid_controles.addWidget(self.reproducir, 0, 0, 1, 1)

        self.cargar = QPushButton(self.box_controles)
        self.cargar.setMaximumSize(QSize(50, 109))
        self.cargar.setToolTip('Cargar archivo')
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/img/eject-1.svg"), QIcon.Normal, QIcon.Off)
        self.cargar.setIcon(icon3)
        self.cargar.setIconSize(QSize(48, 29))
        self.cargar.setFlat(True)
        self.cargar.setObjectName("cargar")
        self.grid_controles.addWidget(self.cargar, 0, 4, 1, 1)

        self.grid_sliders = QHBoxLayout()
        self.grid_sliders.setObjectName("grid_sliders")

        self.tiempo = QSlider(self.box_controles)
        self.tiempo.setOrientation(Qt.Horizontal)
        self.tiempo.setObjectName("tiempo")
        self.grid_sliders.addWidget(self.tiempo)

        self.logo_volumen = QPushButton(self.box_controles)
        self.logo_volumen.setMaximumSize(QSize(41, 41))
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/img/altavoz3.png"), QIcon.Normal, QIcon.Off)
        self.logo_volumen.setIcon(icon4)
        self.logo_volumen.setIconSize(QSize(25, 25))
        self.logo_volumen.setFlat(True)
        self.logo_volumen.setObjectName("logo_volumen")
        self.grid_sliders.addWidget(self.logo_volumen)

        self.volumen = QSlider(self.box_controles)
        self.volumen.setMaximumSize(QSize(139, 16777215))
        self.volumen.setPageStep(1)
        self.volumen.setOrientation(Qt.Horizontal)
        self.volumen.setObjectName("volumen")
        self.grid_sliders.addWidget(self.volumen)
        self.grid_controles.addLayout(self.grid_sliders, 1, 0, 1, 7)

        self.atras = QPushButton(self.box_controles)
        self.atras.setMaximumSize(QSize(50, 109))
        self.atras.setToolTip('Atrasar a la anterior cancion')
        icon5 = QIcon()
        icon5.addPixmap(QPixmap(":/img/back.svg"), QIcon.Normal, QIcon.Off)
        self.atras.setIcon(icon5)
        self.atras.setIconSize(QSize(48, 29))
        self.atras.setFlat(True)
        self.atras.setObjectName("atras")
        self.grid_controles.addWidget(self.atras, 0, 2, 1, 1)

        self.menu = QPushButton(self.box_controles)
        self.menu.setMaximumSize(QSize(50, 109))
        self.menu.setToolTip('Ocultar la lista de reproduccion')
        icon6 = QIcon()
        icon6.addPixmap(QPixmap(":/img/menu2.png"), QIcon.Normal, QIcon.Off)
        self.menu.setIcon(icon6)
        self.menu.setIconSize(QSize(48, 29))
        self.menu.setFlat(True)
        self.menu.setObjectName("menu")
        self.grid_controles.addWidget(self.menu, 0, 6, 1, 1)

        self.datos = QLabel(self.box_controles)
        self.datos.setMinimumSize(QSize(0, 0))
        self.datos.setFrameShape(QFrame.StyledPanel)
        self.datos.setIndent(13)
        self.datos.setObjectName("datos")
        self.grid_controles.addWidget(self.datos, 0, 5, 1, 1)
        self.grid_central.addWidget(self.box_controles, 0, 0, 1, 2)

        self.setCentralWidget(self.contenedor)

        self.setWindowTitle("   Genesis  Reproductor")
        self.setWindowIcon(QIcon('img/icono.jpg'))
        self.box_controles.setTitle(" Bienvenido ...")
        
        self.show()
