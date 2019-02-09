#include "Game.h"
#include <QApplication>

/*
Tutorial Topics:
-QGraphicsPixmapItem, QPixmap, QImage
*/

Game *game;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    game = new Game();
    game->show();

    return a.exec();
}
