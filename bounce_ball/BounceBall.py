"""Implementation of Air Combat in PyQt5

This is a standalone program, only require resources
in 'sounds' and 'images' directories.
"""


import sys
import random
import math
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsItem,
                             QGraphicsPixmapItem, QGraphicsScene,
                             QGraphicsTextItem, QGraphicsLineItem)
from PyQt5.QtCore import Qt, QTimer, QUrl, QDir, QLineF
from PyQt5.QtGui import QFont, QBrush, QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


RESOURCES_DIR = r''


class Ball(QGraphicsPixmapItem):

    def __init__(self, game):
        super().__init__()
        self.setPos(random.randint(10, game.width()-100),
                    random.randint(10, game.height() - 100))
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/ball.png')
        self.setPixmap(QPixmap(path))
        self.setTransformOriginPoint(self.boundingRect().width() / 2,
                                     self.boundingRect().height() / 2)
        self.angle = random.randint(30, 60)
        self.bounce = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(100)
        self.game = game

    def move(self):
        # if ball collides with paddle, bounce it
        for item in self.collidingItems():
            if isinstance(item, Paddle):
                self.angle -= 90
                self.game.plusScore()
                self.game.playSound()
                self.angle %= 360
                dx = 40 * math.cos(math.radians(self.angle))
                dy = 40 * math.sin(math.radians(self.angle))
                self.moveBy(dx, dy)
                return
            elif isinstance(item, QGraphicsLineItem):
                self.angle -= 90
                self.angle %= 360
                dx = 40 * math.cos(math.radians(self.angle))
                dy = 40 * math.sin(math.radians(self.angle))
                self.moveBy(dx, dy)
                return

        # move
        dx = 20 * math.cos(math.radians(self.angle))
        dy = 20 * math.sin(math.radians(self.angle))

        self.angle %= 360
        self.moveBy(dx, dy)


class Paddle(QGraphicsPixmapItem):

    def __init__(self, game):
        super().__init__()
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/paddle.png')
        self.setPixmap(QPixmap(path))
        self.game = game

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.x() >= 10:
                self.setPos(self.x() - 10, self.y())
        elif event.key() == Qt.Key_Right:
            if self.x() + 10 + self.boundingRect().width() <= self.game.width():
                self.setPos(self.x() + 10, self.y())
        elif event.key() == Qt.Key_Down:
            if self.y() + 10 + self.boundingRect().height() <= self.game.height():
                self.setPos(self.x(), self.y() + 10)
        elif event.key() == Qt.Key_Up:
            if self.y() >= 10:
                self.setPos(self.x(), self.y() - 10)


class Game(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        # create a scene
        self.scene = QGraphicsScene()
        # create a item
        self.paddle = Paddle(self)
        # make rect focusable
        self.paddle.setFlag(QGraphicsItem.ItemIsFocusable)
        self.paddle.setFocus()
        # add item to the scene
        self.scene.addItem(self.paddle)
        # add boundaries
        self.scene.addLine(QLineF(0, 0, 800, 0))
        self.scene.addLine(QLineF(0, 0, 0, 600))
        self.scene.addLine(QLineF(800, 0, 800, 600))
        self.scene.addLine(QLineF(0, 600, 800, 600))
        self.scene.setSceneRect(0, 0, 800, 600)
        bgPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                'images/background.png')
        self.setScene(self.scene)
        self.setFixedSize(800, 600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QImage(bgPath)))
        self.paddle.setPos((self.scene.width() - self.paddle.boundingRect().width()) / 2,
                            (self.scene.height() - self.paddle.boundingRect().height()))
        # create the score / escape
        self.score = 0
        self.scoreTextItem = QGraphicsTextItem()
        # draw the text
        self.scoreTextItem.setPlainText("Score  : " + str(self.score))  # Score: 0
        self.scoreTextItem.setDefaultTextColor(Qt.green)
        self.scoreTextItem.setFont(QFont("Arial", 16))
        self.scene.addItem(self.scoreTextItem)
        self.escape = 3
        self.escapeTextItem = QGraphicsTextItem()
        # draw the text
        self.escapeTextItem.setPlainText("Escape: " + str(self.escape))  # Escape: 0
        self.escapeTextItem.setDefaultTextColor(Qt.red)
        self.escapeTextItem.setFont(QFont("Arial", 16))
        self.escapeTextItem.setPos(self.scoreTextItem.x(),
                                   self.scoreTextItem.y() + 25)
        self.scene.addItem(self.escapeTextItem)
        self.scene.addItem(Ball(self))

        self.bounceSound = QMediaPlayer()
        bounceSoundPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                             'sounds/bounce.mp3')
        self.bounceSound.setMedia(QMediaContent(QUrl.fromLocalFile(bounceSoundPath)))

        # play background music
        self.playlist = QMediaPlaylist()
        bgmPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                  'sounds/background.mp3')
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(bgmPath)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.bgmPlayer = QMediaPlayer()
        self.bgmPlayer.setPlaylist(self.playlist)
        self.bgmPlayer.play()

    def plusScore(self):
        self.score += 1
        self.scoreTextItem.setPlainText("Score   : " + str(self.score))

    def minusScore(self):
        self.escape -= 1
        self.escapeTextItem.setPlainText("Escape: " + str(self.escape))

    def playSound(self):
        if self.bounceSound.state() == QMediaPlayer.PlayingState:
            self.bounceSound.setPosition(0)
        elif self.bounceSound.state() == QMediaPlayer.StoppedState:
            self.bounceSound.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
