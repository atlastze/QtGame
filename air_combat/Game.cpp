#include <QBrush>
#include <QFont>
#include <QGraphicsTextItem>
#include <QImage>
#include <QMediaPlayer>
#include <QMediaPlaylist>
#include <QTimer>
#include "Game.h"
#include "Enemy.h"
#include "Fighter.h"

Game::Game(QWidget *parent) : QGraphicsView(parent)
{
    // create the scene
    scene = new QGraphicsScene();
    // make the scene 800x600 instead of infinity by infinity (default)
    scene->setSceneRect(0, 0, 800, 600);
    setBackgroundBrush(QBrush(QImage(":/images/background.png")));

    // make the newly created scene the scene to visualize (since Game
    // is a QGraphicsView Widget,
    // it can be used to visualize scenes)
    setScene(scene);
    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setFixedSize(800, 600);

    // create the fighter
    fighter = new Fighter(this);
    // TODO generalize to always be in the middle bottom of screen
    fighter->setPos(width()/2-fighter->boundingRect().width()/2,
                    height()-fighter->boundingRect().height()-20);
    // make the fighter focusable and set it to be the current focus
    fighter->setFlag(QGraphicsItem::ItemIsFocusable);
    fighter->setFocus();
    // add the fighter to the scene
    scene->addItem(fighter);

    // create the score/health
    // initialize the score to 0
    score = 0;
    scoreTextItem = new QGraphicsTextItem();
    scoreTextItem->setPlainText(QString("Score  : ") + QString::number(score));
    scoreTextItem->setDefaultTextColor(Qt::green);
    scoreTextItem->setFont(QFont("Arial",16));
    scene->addItem(scoreTextItem);
    escape = 0;
    escapeTextItem = new QGraphicsTextItem();
    escapeTextItem->setPlainText(QString("Escape: ") + QString::number(escape));
    escapeTextItem->setDefaultTextColor(Qt::red);
    escapeTextItem->setFont(QFont("Arial",16));
    escapeTextItem->setPos(scoreTextItem->x(), scoreTextItem->y() + 25);
    scene->addItem(escapeTextItem);

    // spawn enemies
    QTimer *timer = new QTimer();
    connect(timer, SIGNAL(timeout()), this, SLOT(spawn()));
    timer->start(5000);

    // play background music
    QMediaPlaylist *playlist = new QMediaPlaylist();
    playlist->addMedia(QUrl("qrc:/sounds/background.mp3"));
    playlist->setPlaybackMode(QMediaPlaylist::Loop);

    QMediaPlayer *music = new QMediaPlayer();
    music->setPlaylist(playlist);
    music->play();
}

void Game::targetDestroyed()
{
    score++;
    scoreTextItem->setPlainText(QString("Score  : ") + QString::number(score));
}

void Game::targetEscaped()
{
    escape++;
    escapeTextItem->setPlainText(QString("Escape: ") + QString::number(escape));
}

void Game::spawn()
{
    // create an enemy
    Enemy *enemy = new Enemy(this);
    scene->addItem(enemy);
}
