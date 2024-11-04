#!/usr/bin/python3
import evdev
from evdev import ecodes

#key=ecodes.KEY_LEFTSHIFT
#kb=evdev.InputDevice('/dev/input/event1')     # keybord
origin=evdev.InputDevice('/dev/input/event4')  # mouse
mouse=evdev.UInput.from_device(origin)
#hwheel=evdev.UInput({ecodes.EV_REL:[ecodes.REL_HWHEEL]})
#hwheel_hires=evdev.UInput({ecodes.EV_REL:[ecodes.REL_HWHEEL_HI_RES]})
#wheel=evdev.UInput({ecodes.EV_REL:[ecodes.REL_WHEEL]})
#wheel_hires=evdev.UInput({ecodes.EV_REL:[ecodes.REL_WHEEL_HI_RES]})
#rbut=evdev.UInput({ecodes.EV_KEY:[ecodes.BTN_RIGHT]})
#ymov=evdev.UInput({ecodes.EV_REL:[ecodes.REL_Y]})
origin.grab()

rbtn_down=False
last_rbtn_event=None
for event in origin.read_loop():
	if event.type==ecodes.EV_KEY and event.code==ecodes.BTN_RIGHT:
		rbtn_down=True if event.value == 1 else False
		last_rbtn_event = event
		continue

#	if event.type==ecodes.EV_REL and event.code==ecodes.REL_WHEEL and key in kb.active_keys():
	if rbtn_down and event.type==ecodes.EV_REL:
		if event.code==ecodes.REL_Y:
			last_rbtn_event=None
			mouse.write(ecodes.EV_REL, ecodes.REL_WHEEL, -event.value)
			mouse.write(ecodes.EV_REL, ecodes.REL_WHEEL_HI_RES, -event.value * 120)
			mouse.write(ecodes.EV_SYN, ecodes.SYN_REPORT, 0)
		elif event.code==ecodes.REL_X:
			last_rbtn_event=None
			mouse.write(ecodes.EV_REL, ecodes.REL_HWHEEL, event.value)
			mouse.write(ecodes.EV_REL, ecodes.REL_HWHEEL_HI_RES, event.value * 120)
			mouse.write(ecodes.EV_SYN, ecodes.SYN_REPORT, 0)
	else:
		mouse.write_event(event)

	if (last_rbtn_event and ((event.sec > last_rbtn_event.sec) or (event.sec == last_rbtn_event.sec and event.usec - last_rbtn_event.usec > 100)) ):
		mouse.write_event(last_rbtn_event)
		last_rbtn_event=None

#	for att in dir(event): print (att, getattr(event,att))
