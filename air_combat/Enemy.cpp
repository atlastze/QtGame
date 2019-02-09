#include <QGraphicsScene>
#include <QList>
#include <QTimer>
#include <stdlib.h>
#include "Enemy.h"
#include "Game.h"

Enemy::Enemy(Game *game, QGraphicsItem *parent)
    : QObject()
    , QGraphicsPixmapItem(parent)
{
    this->game =  game;
    //set random x position
    int random_number = rand() % (game->width()-100);
    setPos(random_number, 0);

    // drew the rect
    setPixmap(QPixmap(":/images/enemy.png"));
    setTransformOriginPoint(boundingRect().width() / 2,
                            boundingRect().height() / 2);
    setRotation(180);

    // make/connect a timer to move() the enemy every so often
    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(move()));

    // start the timer
    timer->start(50);
}

void Enemy::move()
{
    // move enemy down
    setPos(x(), y() + 5);

    // destroy enemy when it goes out of the screen
    if (pos().y() > game->height()) {
        //decrease the health
        game->targetEscaped();

        scene()->removeItem(this);
        delete this;
    }
}
