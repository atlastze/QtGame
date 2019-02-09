#ifndef ENEMY_H
#define ENEMY_H

#include <QGraphicsItem>
#include <QGraphicsPixmapItem>
#include <QObject>

class Game;

class Enemy : public QObject, public QGraphicsPixmapItem {
    Q_OBJECT

public:
    Enemy(Game *game, QGraphicsItem *parent = 0);

public slots:
    void move();

private:
    Game *game;
};

#endif // ENEMY_H
