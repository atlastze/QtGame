#ifndef GAME_H
#define GAME_H

#include <QGraphicsScene>
#include <QGraphicsView>
#include <QWidget>


class Fighter;

class Game : public QGraphicsView {
    Q_OBJECT

public:
    Game(QWidget *parent = 0);

public slots:
    void targetDestroyed();
    void targetEscaped();
    void spawn();

private:
    QGraphicsScene *scene;
    Fighter *fighter;
    int score;
    QGraphicsTextItem *scoreTextItem;
    int escape;
    QGraphicsTextItem *escapeTextItem;
};

#endif // GAME_H
