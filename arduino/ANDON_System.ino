/*
 * ANDON System - Arduino Controller
 * 
 * This sketch implements an ANDON (manufacturing alert system) controller
 * Features:
 * - Multiple button inputs for different alert types
 * - LED indicators for visual alerts
 * - Buzzer for audio alerts
 * - Serial communication with Python application
 */

// Pin Definitions
const int BUTTON_PIN_1 = 2;  // Emergency button
const int BUTTON_PIN_2 = 3;  // Quality issue button
const int BUTTON_PIN_3 = 4;  // Material shortage button
const int BUTTON_PIN_4 = 5;  // Maintenance needed button

const int LED_RED = 8;       // Emergency LED
const int LED_YELLOW = 9;    // Quality/Maintenance LED
const int LED_GREEN = 10;    // Normal operation LED
const int BUZZER_PIN = 11;   // Buzzer for audio alert

// Button states
bool lastButtonState1 = HIGH;
bool lastButtonState2 = HIGH;
bool lastButtonState3 = HIGH;
bool lastButtonState4 = HIGH;

unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;
unsigned long lastDebounceTime4 = 0;
const unsigned long debounceDelay = 50;

// System state
enum SystemState {
  NORMAL,
  EMERGENCY,
  QUALITY_ISSUE,
  MATERIAL_SHORTAGE,
  MAINTENANCE_NEEDED
};

SystemState currentState = NORMAL;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize button pins
  pinMode(BUTTON_PIN_1, INPUT_PULLUP);
  pinMode(BUTTON_PIN_2, INPUT_PULLUP);
  pinMode(BUTTON_PIN_3, INPUT_PULLUP);
  pinMode(BUTTON_PIN_4, INPUT_PULLUP);
  
  // Initialize LED pins
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  
  // Initialize buzzer pin
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Set initial state to normal
  setNormalState();
  
  Serial.println("ANDON System Ready");
}

void loop() {
  // Read button states with debouncing
  checkButton(BUTTON_PIN_1, &lastButtonState1, &lastDebounceTime1, 1);
  checkButton(BUTTON_PIN_2, &lastButtonState2, &lastDebounceTime2, 2);
  checkButton(BUTTON_PIN_3, &lastButtonState3, &lastDebounceTime3, 3);
  checkButton(BUTTON_PIN_4, &lastButtonState4, &lastDebounceTime4, 4);
  
  // Check for serial commands from Python
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    processCommand(command);
  }
  
  // Update system state visuals
  updateStateIndicators();
}

void checkButton(int pin, bool* lastState, unsigned long* lastDebounce, int buttonNum) {
  bool reading = digitalRead(pin);
  
  if (reading != *lastState) {
    *lastDebounce = millis();
  }
  
  if ((millis() - *lastDebounce) > debounceDelay) {
    if (reading == LOW) {  // Button pressed (active LOW with pullup)
      handleButtonPress(buttonNum);
    }
  }
  
  *lastState = reading;
}

void handleButtonPress(int buttonNum) {
  switch(buttonNum) {
    case 1:
      currentState = EMERGENCY;
      Serial.println("ALERT:EMERGENCY");
      break;
    case 2:
      currentState = QUALITY_ISSUE;
      Serial.println("ALERT:QUALITY_ISSUE");
      break;
    case 3:
      currentState = MATERIAL_SHORTAGE;
      Serial.println("ALERT:MATERIAL_SHORTAGE");
      break;
    case 4:
      currentState = MAINTENANCE_NEEDED;
      Serial.println("ALERT:MAINTENANCE_NEEDED");
      break;
  }
}

void processCommand(String command) {
  if (command == "RESET") {
    setNormalState();
    Serial.println("STATUS:RESET_OK");
  } else if (command == "STATUS") {
    sendStatus();
  } else if (command == "TEST") {
    testSystem();
  }
}

void setNormalState() {
  currentState = NORMAL;
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(BUZZER_PIN, LOW);
}

void updateStateIndicators() {
  switch(currentState) {
    case NORMAL:
      digitalWrite(LED_RED, LOW);
      digitalWrite(LED_YELLOW, LOW);
      digitalWrite(LED_GREEN, HIGH);
      digitalWrite(BUZZER_PIN, LOW);
      break;
      
    case EMERGENCY:
      digitalWrite(LED_RED, HIGH);
      digitalWrite(LED_YELLOW, LOW);
      digitalWrite(LED_GREEN, LOW);
      // Pulsing buzzer for emergency
      digitalWrite(BUZZER_PIN, (millis() / 500) % 2);
      break;
      
    case QUALITY_ISSUE:
    case MAINTENANCE_NEEDED:
      digitalWrite(LED_RED, LOW);
      digitalWrite(LED_YELLOW, HIGH);
      digitalWrite(LED_GREEN, LOW);
      digitalWrite(BUZZER_PIN, LOW);
      break;
      
    case MATERIAL_SHORTAGE:
      digitalWrite(LED_RED, LOW);
      digitalWrite(LED_YELLOW, (millis() / 1000) % 2);  // Blinking yellow
      digitalWrite(LED_GREEN, LOW);
      digitalWrite(BUZZER_PIN, LOW);
      break;
  }
}

void sendStatus() {
  Serial.print("STATUS:");
  switch(currentState) {
    case NORMAL:
      Serial.println("NORMAL");
      break;
    case EMERGENCY:
      Serial.println("EMERGENCY");
      break;
    case QUALITY_ISSUE:
      Serial.println("QUALITY_ISSUE");
      break;
    case MATERIAL_SHORTAGE:
      Serial.println("MATERIAL_SHORTAGE");
      break;
    case MAINTENANCE_NEEDED:
      Serial.println("MAINTENANCE_NEEDED");
      break;
  }
}

void testSystem() {
  Serial.println("TEST:START");
  
  // Test all LEDs
  digitalWrite(LED_RED, HIGH);
  delay(500);
  digitalWrite(LED_RED, LOW);
  
  digitalWrite(LED_YELLOW, HIGH);
  delay(500);
  digitalWrite(LED_YELLOW, LOW);
  
  digitalWrite(LED_GREEN, HIGH);
  delay(500);
  digitalWrite(LED_GREEN, LOW);
  
  // Test buzzer
  digitalWrite(BUZZER_PIN, HIGH);
  delay(200);
  digitalWrite(BUZZER_PIN, LOW);
  
  setNormalState();
  Serial.println("TEST:COMPLETE");
}
