wemos + 馬達驅動板
===

1. wemos 加入支援 motor 控制 （取代原本 Smart自走車積木)
2. 馬達驅動板更新驅動程式
3. 完成樣品交付



~~~python=
Motor M1(0x30,_MOTOR_A, 1000);//Motor A
Motor M2(0x30,_MOTOR_B, 1000);//Motor B
int pwm;
  
  for(int i=0;i<100;i++){
   for ( pwm = 0; pwm <= 100; pwm++)
  {
    M1.setmotor( _CW, pwm);
    M2.setmotor(_CW, pwm);
    Serial.printf("A:%d%, B:%d%, DIR:CW\r\n", pwm,100-pwm);
  }
  
  M1.setmotor(_STOP);
  M2.setmotor( _STOP);
  Serial.println("Motor A&B STOP");
  delay(1000);
  
  for (pwm = 100; pwm >=0; pwm--)
  {
    M1.setmotor(_CCW, pwm);
    M2.setmotor(_CCW, pwm);
    Serial.printf("A:%d%, B:%d%, DIR:CCW\r\n", pwm,100-pwm);
  }
  
  M1.setmotor(_STOP);
  M2.setmotor( _STOP);
  delay(200);
  Serial.println("Motor A&B STOP");

  M1.setmotor(_SHORT_BRAKE);
  M2.setmotor( _SHORT_BRAKE);
  Serial.println("Motor A&B SHORT BRAKE");  
  delay(1000);
  
  M1.setmotor(_STANDBY);//Both Motor standby
  M2.setmotor( _STANDBY);
  Serial.println("Motor A&B STANDBY");  
  delay(1000);
  }
~~~