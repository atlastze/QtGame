#ifndef PLAYER_H
#define PLAYER_H

#include <QGraphicsItem>
#include <QGraphicsPixmapItem>
#include <QObject>

class Game;

class Fighter : public QObject, public QGraphicsPixmapItem {
    Q_OBJECT

public:
    Fighter(Game *game, QGraphicsItem *parent = 0);
    void keyPressEvent(QKeyEvent *event);

private:
    Game *game;
};

#endif // PLAYER_H
