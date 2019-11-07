#include <Arduino.h>

// Main definitions
#ifndef DEFINITIONS_H
#define DEFINITIONS_H

/*  ==========================
    Status Enum for game board
    ==========================

    READY       = ready for training or game start
    PRETRAINING   = connected to training dashboard, not training yet (serial port open - prevents game start)
    PREPLAYING   = connected to game dashboard, not playing yet (serial port open)
    TRAINING    = training new data via dashboard (sends sensor inputs to dashboard via specified port)
    UPLOAD      = ready to upload new training data (after training is finished)
    PLAYING     = actively playing the game (outputs API calls for game logic)
 */

typedef enum  {
    READY,
    PRETRAINING,
    PREPLAYING,
    TRAINING,
    UPLOAD,
    PLAYING
}Status;


typedef enum {

  TRAIN_OK
}Command;

/* ==================
   Physical pin setup
   ================== */

//LED Pins
extern int LED_Red;
extern int LED_Green;


//
extern Status currentStatus;
extern String receivedData;


#endif
