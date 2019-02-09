#ifndef MISSILE_H
#define MISSILE_H

#include <QGraphicsItem>
#include <QGraphicsPixmapItem>
#include <QMediaPlayer>
#include <QObject>

class Game;

class Missile : public QObject, public QGraphicsPixmapItem {
    Q_OBJECT

public:
    Missile(Game *game, QGraphicsItem *parent = 0);

public slots:
    void move();

private:
    Game *game;
    QMediaPlayer *explosionSound;
};

#endif // MISSILE_H
