#-------------------------------------------------
#
# Project created by QtCreator 2019-1-9 9:25:56
#
#-------------------------------------------------

QT       += core gui \
         multimedia

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = AirCombat 
TEMPLATE = app


SOURCES += main.cpp \
    Missile.cpp \
    Enemy.cpp \
    Game.cpp \
    Fighter.cpp

HEADERS  += \
    Missile.h \
    Enemy.h \
    Game.h \
    Fighter.h

RESOURCES += \
    res.qrc

macx {
    QMAKE_MAC_SDK = macosx
}
