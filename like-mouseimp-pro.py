#!/usr/bin/python3
from evdev import InputDevice, UInput, ecodes as ec

#key=ec.KEY_LEFTSHIFT
#kb=InputDevice('/dev/input/event1')     # keybord
input_mouse=InputDevice('/dev/input/event4')  # mouse
output_mouse=UInput.from_device(input_mouse, name='Drag-scroll like MouseImp Pro!')
#hwheel=UInput({ec.EV_REL:[ec.REL_HWHEEL]})
#hwheel_hires=UInput({ec.EV_REL:[ec.REL_HWHEEL_HI_RES]})
#wheel=UInput({ec.EV_REL:[ec.REL_WHEEL]})
#wheel_hires=UInput({ec.EV_REL:[ec.REL_WHEEL_HI_RES]})
#rbut=UInput({ec.EV_KEY:[ec.BTN_RIGHT]})
#ymov=UInput({ec.EV_REL:[ec.REL_Y]})
input_mouse.grab()

rbtn_is_down=0
last_rbtn_event=None

for event in input_mouse.read_loop():
#	for att in dir(event): print (att, getattr(event,att))

	if (ec.EV_KEY == event.type) and (ec.BTN_RIGHT == event.code):
		rbtn_is_down = event.value
		last_rbtn_event = event
		continue

#	if ec.EV_REL == event.type and ec.REL_WHEEL == event.code and key in kb.active_keys():

	if rbtn_is_down and (ec.EV_REL == event.type):
		if event.code == ec.REL_Y:
			last_rbtn_event = None
			output_mouse.write(ec.EV_REL, ec.REL_WHEEL, -event.value)
			output_mouse.write(ec.EV_REL, ec.REL_WHEEL_HI_RES, -event.value * 120)
#			output_mouse.write(ec.EV_REL, ec.REL_Y, event.value)
#			output_mouse.write(ec.EV_SYN, ec.SYN_REPORT, 0)
			output_mouse.syn()
			continue
		elif event.code==ec.REL_X:
			last_rbtn_event=None
			output_mouse.write(ec.EV_REL, ec.REL_HWHEEL, event.value)
			output_mouse.write(ec.EV_REL, ec.REL_HWHEEL_HI_RES, event.value * 120)
#			output_mouse.write(ec.EV_REL, ec.REL_X, event.value)
#			output_mouse.write(ec.EV_SYN, ec.SYN_REPORT, 0)
			output_mouse.syn()
			continue

	if (last_rbtn_event and ((event.sec > last_rbtn_event.sec) or (event.sec == last_rbtn_event.sec and event.usec - last_rbtn_event.usec > 100)) ):
		output_mouse.write_event(last_rbtn_event)
		last_rbtn_event=None

	output_mouse.write_event(event)


input_mouse.ungrab()
