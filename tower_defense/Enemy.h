#ifndef ENEMY_H
#define ENEMY_H

#include <QGraphicsPixmapItem>
#include <QList> // list << element
#include <QObject>
#include <QPointF>

class Enemy : public QObject, public QGraphicsPixmapItem {
    Q_OBJECT
public:
    Enemy(QGraphicsItem *parent = 0);
    //void rotateToPoint(QPointF p);
public slots:
    void move_forward();

private:
    QList<QPointF> points;
    QPointF dest;
    int point_index;
    double angle;
};

#endif // ENEMY_H
