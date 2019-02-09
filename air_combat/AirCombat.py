"""Implementation of Air Combat in PyQt5

This is a standalone program, only require resources
in 'sounds' and 'images' directories.
"""


import sys
import random
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsItem,
                             QGraphicsPixmapItem, QGraphicsScene,
                             QGraphicsTextItem)
from PyQt5.QtCore import Qt, QTimer, QUrl, QDir
from PyQt5.QtGui import QFont, QBrush, QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


RESOURCES_DIR = r''


class Missile(QGraphicsPixmapItem):

    def __init__(self, game):
        super().__init__()
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/missile.png')
        self.setPixmap(QPixmap(path))
        # In the C++ version of this example, this class is also derived from
        # QObject in order to receive timer events.  PyQt does not support
        # deriving from more than one wrapped class so we just create an
        # explicit timer instead.
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(50)
        self.game = game

    def move(self):
        # if missile collides with enemy, destroy both
        for item in self.collidingItems():
            if isinstance(item, Enemy):
                self.scene().removeItem(item)
                self.scene().removeItem(self)
                self.game.targetDestroyed()
                self.game.playExplosion()
                return

        # move down
        self.setPos(self.x(), self.y() - 10)
        if self.y() + self.boundingRect().height() < 0:
            self.scene().removeItem(self)


class Enemy(QGraphicsPixmapItem):

    def __init__(self, game):
        super().__init__()
        self.setPos(random.randint(0, game.width()-100), 0)
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/enemy.png')
        self.setPixmap(QPixmap(path))
        self.setTransformOriginPoint(self.boundingRect().width() / 2,
                                     self.boundingRect().height() / 2)
        self.setRotation(180)
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(100)
        self.game = game

    def move(self):
        self.setPos(self.x(), self.y() + 5)
        if self.y() > self.scene().height():
            self.game.targetEscaped()
            self.scene().removeItem(self)


class Fighter(QGraphicsPixmapItem):

    def __init__(self, game):
        super().__init__()
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/fighter.png')
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
        elif event.key() == Qt.Key_Space:
            # create a missile
            missile = Missile(self.game)
            missile.setPos(self.x() + 45, self.y())
            self.scene().addItem(missile)
            self.game.playMissile()


class Game(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        # create a scene
        self.scene = QGraphicsScene()
        # create a item
        self.fighter = Fighter(self)
        # make rect focusable
        self.fighter.setFlag(QGraphicsItem.ItemIsFocusable)
        self.fighter.setFocus()
        # add item to the scene
        self.scene.addItem(self.fighter)
        # create a view and set the scene

        self.scene.setSceneRect(0, 0, 800, 600)
        bgPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                'images/background.png')
        self.setScene(self.scene)
        self.setFixedSize(800, 600)
        self.setBackgroundBrush(QBrush(QImage(bgPath)))
        self.fighter.setPos((self.scene.width() - self.fighter.boundingRect().width()) / 2,
                            (self.scene.height() - self.fighter.boundingRect().height()))
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
        # spawn enemies
        self.timer = QTimer()
        self.timer.timeout.connect(self.spawn)
        self.timer.start(5000)

        self.missileSound = QMediaPlayer()
        missileSoundPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                           'sounds/missile.mp3')
        self.missileSound.setMedia(QMediaContent(QUrl.fromLocalFile(missileSoundPath)))
        self.explosionSound = QMediaPlayer()
        explosionSoundPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                             'sounds/explosion.mp3')
        self.explosionSound.setMedia(QMediaContent(QUrl.fromLocalFile(explosionSoundPath)))
        self.explosionSound = QMediaPlayer()
        explosionSoundPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                             'sounds/explosion.mp3')
        self.explosionSound.setMedia(QMediaContent(QUrl.fromLocalFile(explosionSoundPath)))

        # play background music
        self.playlist = QMediaPlaylist()
        bgmPath = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                                  'sounds/background.mp3')
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(bgmPath)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.bgmPlayer = QMediaPlayer()
        self.bgmPlayer.setPlaylist(self.playlist)
        self.bgmPlayer.play()

    def spawn(self):
        self.scene.addItem(Enemy(self))

    def targetDestroyed(self):
        self.score += 1
        self.scoreTextItem.setPlainText("Score   : " + str(self.score))

    def targetEscaped(self):
        self.escape -= 1
        self.escapeTextItem.setPlainText("Escape: " + str(self.escape))

    def playExplosion(self):
        if self.explosionSound.state() == QMediaPlayer.PlayingState:
            self.explosionSound.setPosition(0)
        elif self.explosionSound.state() == QMediaPlayer.StoppedState:
            self.explosionSound.play()

    def playMissile(self):
        if self.missileSound.state() == QMediaPlayer.PlayingState:
            self.missileSound.setPosition(0)
        elif self.missileSound.state() == QMediaPlayer.StoppedState:
            self.missileSound.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
