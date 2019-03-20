import sys
import math
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsPixmapItem,
                             QGraphicsPolygonItem,
                             QGraphicsScene)
from PyQt5.QtCore import QDir, QPointF, Qt, QTimer, QLineF
from PyQt5.QtGui import QPixmap, QPolygonF


RESOURCES_DIR = r''


class Bullet(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/stone.png')
        self.setPixmap(QPixmap(path))
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(50)

    def move(self):
        angle = self.rotation()
        dx = 30 * math.cos(math.radians(angle))
        dy = 30 * math.sin(math.radians(angle))
        self.moveBy(dx, dy)


class Enemy(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/lumberman.png')
        self.setPixmap(QPixmap(path))
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(200)
        self.route = [QPointF(800, 200), QPointF(600, 500),
                      QPointF(300, 500), QPointF(300, 200)]
        self.index = 0
        self.angle = 0

    def move(self):
        path = QLineF(self.pos(), self.route[self.index])
        if path.length() < 10:
            self.index += 1
            if self.index >= len(self.route):  # stop
                self.index -= 1
                return
        self.angle = -path.angle()
        dx = 10 * math.cos(math.radians(self.angle))
        dy = 10 * math.sin(math.radians(self.angle))
        self.moveBy(dx, dy)


class Tower(QGraphicsPixmapItem):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        path = QDir.current().absoluteFilePath(RESOURCES_DIR +
                                               'images/background.png')
        self.setPixmap(QPixmap(path))
        points = [QPointF(1, 0), QPointF(0.707, 0.707),
                  QPointF(0, 1), QPointF(-0.707, 0.707),
                  QPointF(-1, 0), QPointF(-0.707, -0.707),
                  QPointF(0, -1), QPointF(0.707, -0.707)]
        scale_factor = 240
        for i in range(len(points)):
            points[i] *= scale_factor

        self.attack_area = QGraphicsPolygonItem(QPolygonF(points), self)
        # move the polygon center to the pixmap center
        self.attack_area.setPos(550, 250)

        self.attack_dest = QPointF(800, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.attack_target)
        self.timer.start(500)

    def attack_target(self):
        colliding_items = self.attack_area.collidingItems()
        if len(colliding_items) == 1:
            return
        for item in colliding_items:
            if isinstance(item, Enemy):
                bullet = Bullet(self)
                bullet.setPos(550, 250)
                self.attack_dest = item.pos()
                direct = QLineF(QPointF(550, 250), self.attack_dest)
                bullet.setRotation(-direct.angle())
                #self.scene().addItem(bullet)


class Game(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.tower = Tower()
        self.scene.addItem(self.tower)
        self.enemy = Enemy()
        self.enemy.setPos(700, 0)
        self.scene.addItem(self.enemy)
        self.setFixedSize(800, 600)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, event):
        # create a bullet
        bullet = Bullet()
        bullet.setPos(event.pos())
        bullet.setRotation(40)
        self.scene.addItem(bullet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
