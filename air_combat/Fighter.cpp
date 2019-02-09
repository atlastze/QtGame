#include <QGraphicsScene>
#include <QKeyEvent>
#include "Game.h"
#include "Fighter.h"
#include "Enemy.h"
#include "Missile.h"

Fighter::Fighter(Game *game, QGraphicsItem *parent)
    : QGraphicsPixmapItem(parent)
{
    this->game =  game;
    // set graphic
    setPixmap(QPixmap(":/images/fighter.png"));
}

void Fighter::keyPressEvent(QKeyEvent *event)
{
    // move the player left and right
    if (event->key() == Qt::Key_Left) {
        if (pos().x() >= 20)
            setPos(x() - 20, y());
    } else if (event->key() == Qt::Key_Right) {
        if (pos().x() + 20 + boundingRect().width() <= game->width())
            setPos(x() + 20, y());
    } else if (event->key() == Qt::Key_Down) {
        if (pos().y() + 20 + boundingRect().height() <= game->height())
            setPos(x(), y() + 20);
    } else if (event->key() == Qt::Key_Up) {
        if (pos().y() >= 20)
            setPos(x(), y() - 20);
    } else if (event->key() == Qt::Key_Space) { // shoot with the space
        // create a missile
        Missile *missile = new Missile(game);
        missile->setPos(x() + 45, y());
        scene()->addItem(missile);

        // play missileSound
        game->playMissile();
    }
}
