import machine , time

def play(freq=300,delay=0.1):
        pin25 = machine.PWM(machine.Pin(0), duty=512)
        pin25.freq(freq)
        time.sleep(delay)
        machine.PWM(machine.Pin(0), duty=0)

play(262,0.2)
play(294,0.2)
play(330,0.2)
