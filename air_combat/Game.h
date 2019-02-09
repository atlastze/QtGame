#ifndef GAME_H
#define GAME_H

#include <QGraphicsScene>
#include <QGraphicsView>
#include <QWidget>


class Fighter;
class QMediaPlayer;

class Game : public QGraphicsView {
    Q_OBJECT

public:
    Game(QWidget *parent = 0);

public slots:
    void targetDestroyed();
    void targetEscaped();
    void spawn();
    void playMissile();
    void playExplosion();

private:
    QGraphicsScene *scene;
    Fighter *fighter;
    int score;
    QGraphicsTextItem *scoreTextItem;
    int escape;
    QGraphicsTextItem *escapeTextItem;
    QMediaPlayer *missileSound;
    QMediaPlayer *explosionSound;
    QMediaPlayer *bgmPlayer;
};

#endif // GAME_H
