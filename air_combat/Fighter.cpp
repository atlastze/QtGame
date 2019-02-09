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
    // set bullet sound
    missileSound = new QMediaPlayer();
    missileSound->setMedia(QUrl("qrc:/sounds/missile.mp3"));

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
        // create a bullet
        Missile *bullet = new Missile(game);
        bullet->setPos(x() + 45, y());
        scene()->addItem(bullet);

        // play missileSound
        if (missileSound->state() == QMediaPlayer::PlayingState) {
            missileSound->setPosition(0);
        } else if (missileSound->state() == QMediaPlayer::StoppedState) {
            missileSound->play();
        }
    }
}
