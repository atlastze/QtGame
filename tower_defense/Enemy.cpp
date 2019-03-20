#include "Enemy.h"
#include <QPixmap>
#include <QTimer>
#include <qmath.h>

Enemy::Enemy(QGraphicsItem *parent)
    : QObject()
    , QGraphicsPixmapItem(parent)
{
    // set graphics
    setPixmap(QPixmap(":/images/lumberman.png"));

    // set points
    points << QPointF(800, 200) << QPointF(600, 500)
           << QPointF(300, 500) << QPointF(300, 200); // move down-right then right
    point_index = 0;
    dest = points[0];
    //rotateToPoint(dest);

    // connect timer to move_forward
    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(move_forward()));
    timer->start(150);
}

/*void Enemy::rotateToPoint(QPointF p){
    QLineF ln(pos(),p);
    angle = -ln.angle();
}*/

void Enemy::move_forward()
{
    // if close to dest, rotate to next dest
    QLineF ln(pos(), dest);
    if (ln.length() < 5) {
        point_index++;
        if (point_index >= points.size()) {
            return;
        }
        dest = points[point_index];
    }
    angle = -ln.angle();

    // move enemy forward at current angle
    int STEP_SIZE = 5;

    double dy = STEP_SIZE * qSin(qDegreesToRadians(angle));
    double dx = STEP_SIZE * qCos(qDegreesToRadians(angle));

    moveBy(dx, dy);
}
