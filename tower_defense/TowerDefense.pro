#-------------------------------------------------
#
# Project created by QtCreator 2014-11-17T19:51:56
#
#-------------------------------------------------

QT       += core gui \
         multimedia

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = TowerDefense 
TEMPLATE = app


SOURCES += main.cpp \
    Tower.cpp \
    Bullet.cpp \
    Enemy.cpp \
    Game.cpp

HEADERS  += \
    Tower.h \
    Bullet.h \
    Enemy.h \
    Game.h

RESOURCES += \
    res.qrc

macx {
    QMAKE_MAC_SDK = macosx
}
