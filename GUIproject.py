from tkinter import *

import datetime
import threading
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time
from PIL import Image

def Servo(angle):
  duty = angle / 18 + 2
  GPIO.output(3, True)
  pwm.ChangeDutyCycle(duty)
  sleep(1)
  GPIO.output(3, False)
  pwm.ChangeDutyCycle(0)
  pwm.stop()
  GPIO.cleanup()

present = datetime.now()

uandp = {}



def run_motor_sequence(motor_number, duration, rot_type):
  global all_pins
  global halfstep_seq
  #1 -- seller motor,,,, 2 == milk_motor,,,,, 3 == chips_motor,,,,, 4 == last_motor +
  GPIO.setmode(GPIO.BOARD)

  all_pins = [7, 11, 13, 15] + [29, 31, 33, 35] + [32, 36, 38, 40] + [16, 18, 22, 37]

  for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

  halfstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
  ]
  if motor_number == 1:
    control_pins = all_pins[:4]

  if motor_number == 2:
    control_pins = all_pins[4:8]

  if motor_number == 3:
    control_pins = all_pins[8:12]

  if motor_number == 4:
    control_pins = all_pins[12:16]





  if rot_type == 'clock':
    for i in range(duration):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
    GPIO.cleanup()
  else:
    for i in range(duration):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][-1*pin-1])
        time.sleep(0.001)
    GPIO.cleanup()


def sell(arg):
  if arg == 'Milk':
    run_motor_sequence(1,400,'clock')
    time.sleep(0.1)
    run_motor_sequence(2, 120, 'clock')
    Servo(180)
    time.sleep(0.1)
    Servo(-180)
    run_motor_sequence(2,120,'not-clock')

  if arg == 'Chips':
    run_motor_sequence(1, 400, 'clock')
    time.sleep(0.1)
    run_motor_sequence(3, 120, 'clock')
    Servo(180)
    time.sleep(0.1)
    Servo(-180)
    run_motor_sequence(3, 120, 'not-clock')


def buy(x,status):

  if len(items[x][0]) > 0:

    print(x)

    items[x][0].pop()
    try:
      labels[x]['text'] = '\n' + ' ' * 4 + '  {}.   '.format(len(x)) + '  ' + x + '_' * int(26 - len(x)) + str(items[x][1]) + '_' * 12 + str(len(items[x][0]))
    except NameError:
      pass
    # do motor code
    if x == 'Milk':
      run_motor_sequence(2, 120, 'clock')
      time.sleep(0.1)
      if status == 'expired':
        run_motor_sequence(4,512, 'not-clock')
      else:
        run_motor_sequence(4,512,'clock')

      run_motor_sequence(2, 512,'not-clock')

    if x == 'Chips':
      run_motor_sequence(3, 120, 'clock')
      time.sleep(0.1)
      if status == 'expired':
        run_motor_sequence(4, 512, 'not-clock')
      else:
        run_motor_sequence(4, 512, 'clock')

      run_motor_sequence(3,120,'not-clock')




def create_item_info_window(arg):
  global item_info

  item_info = Tk()

  item_info.title('{} info'.format(arg))

  item_info.geometry("{0}x{1}+0+0".format(item_info.winfo_screenwidth(), item_info.winfo_screenheight()))

  item_info.configure(background = 'light blue')

  item = Label(item_info, text = '\n' *1 + ' '*55 + arg, bg = 'light blue', fg = 'black', font = 'none 36')
  item.grid(row = 0, column = 0, sticky= E)

  expiry = Label(item_info, text = 'best before {}-{}'.format(items[arg][0][0].month, items[arg][0][0].year), bg = 'light blue', fg = 'black', font = 'none 18')
  expiry.grid(row=1, column=0,sticky=S)



  exitscr = Label(item_info, text = 'press X to cancel', bg = 'light blue', fg = 'black', font = 'none 24')
  exitscr.grid(row=2, column=1, sticky = W)

  ok = Button(item_info, text='BUY', width=5, font='none 24')
  ok.grid(row=3, column=0, sticky=W)
  ok['command'] = lambda arg1 = arg, arg2 = 'buy' : buy(arg1,arg2)




def student_data():
  students = 'rishav	arun	gaurav	harsh	rohit	sahil	kirti	prakhar	abhishek	anuj	dhruv	mayank	mohit	palle	parag	vaibhav	tano	anu	sidhant	aakash	aashish	aastha	abdul	abhimanyu	abhinav	aditi	agrim	akhilesh	akshat	anant	aniket	anisha	anoushka	ayush	bhaskar	bijendar	chintan	garmit	gitansh	gugulothu	harshit	harshita	ishaan	ishaan	ishani	jyotiraditya	keshav	krishna	madhav	madhur	meetakshi	mitul	mohammad	mohit	mohit	mudit	nikhil	nikhil	nikhil	pankaj	pranay	rahul	rahul	rahul	ravi	rohit	rohit	saksham	saurav	shivam	shivansh	shruti	shubham	siddhant	siddharth	sourabh	sudarshan	tushar	udit	ujjwal	uttam	vaibhav	varun	vidhi	vikram	vinay	yash	yashasvi	yuvraj	aditi	ajay	aman	ananya	anmol	apeksha	arihant	arnav	arshad	ayush	devansh	dhroov	dolly	dushyant	harshal	hribhav	ishan	ishan	ishika	kanu	khushi	sudeep	navam	nimisha	piyush	prakhar	rahul	rhea	ritik	ritik	ritvik	rohan	rohan	saarthak	sachleen	sakshat	samarth	sambhav	sameer	samiksha	shivam	shiven	shrey	shrivatsa	shubham	sneh	sushmita	tarun	tushar	vaibhav	vaibhav	vasu	vasu	yash	yatharth	yugansh	adey	akhil	anirudh	ansh	anushka	ayush	bhavesh	bhavesh	bhawna	deepanshu	dheeraj	divyanshi	etash	harshwardhan	himanshu	isha	ishita	kabir	karan	kheya	manas	manasvi	mansi	medhavi	mohit	nishchay	ojaswi	prachi	prakhar	prakhar	prerak	raghav	rahul	rishabh	rishit	rishita	ritesh	saksham	saransh	saurav	shabeg	shefali	shivam	srishti	taral	tushar	tushar	vani	vanshika	vasu	vikrant	vishrut	yatharth	abhishek	abhishek	abhyudit	aditya	aditya	aditya	amal	ananya	ankit	aparna	arham	ashmeet	ashutosh	atharv	barundeep	bhaskar	deepak	dev	esha	eshu	hardik	harsh	harshit	harshita	hitesh	kartikey	kishan	kumud	kunal	lakshay	manvik	md	meenal	meet	naman	niranjan	palak	prakriti	pritish	reshmi	riya	rohan	rohit	saarthak	samad	shashwat	srijan	stuti	sushant	tarini	tarushi	vaibhav	vaibhav	vishal	yash'

  roll_numbers = '2017259	2018224	2018233	2018234	2018259	2018260	2018291	2018300	2018325	2018330	2018335	2018341	2018344	2018354	2018355	2018370	2018374	2018383	2018416	2019222	2019223	2019224	2019225	2019226	2019227	2019228	2019229	2019230	2019231	2019232	2019233	2019234	2019235	2019236	2019237	2019238	2019239	2019240	2019241	2019242	2019243	2019244	2019245	2019246	2019247	2019248	2019249	2019250	2019251	2019252	2019253	2019254	2019255	2019256	2019257	2019258	2019259	2019260	2019261	2019262	2019263	2019264	2019265	2019266	2019267	2019268	2019269	2019270	2019271	2019272	2019273	2019274	2019275	2019276	2019277	2019278	2019279	2019280	2019281	2019282	2019283	2019284	2019285	2019286	2019287	2019288	2019289	2019290	2019291	2019292	2019293	2019294	2019295	2019296	2019297	2019298	2019299	2019300	2019301	2019302	2019303	2019304	2019305	2019306	2019307	2019308	2019309	2019310	2019311	2019312	2019313	2019314	2019315	2019316	2019317	2019318	2019319	2019320	2019321	2019322	2019323	2019324	2019325	2019326	2019327	2019328	2019329	2019330	2019331	2019332	2019333	2019334	2019335	2019336	2019337	2019338	2019339	2019340	2019341	2019342	2019343	2019344	2019345	2019346	2019347	2019348	2019349	2019350	2019351	2019352	2019353	2019354	2019355	2019356	2019357	2019358	2019359	2019360	2019361	2019362	2019363	2019364	2019365	2019366	2019367	2019368	2019369	2019370	2019371	2019372	2019373	2019374	2019375	2019376	2019377	2019378	2019379	2019380	2019381	2019382	2019383	2019384	2019385	2019386	2019387	2019388	2019389	2019390	2019391	2019392	2019393	2019394	2019395	2019396	2019397	2019398	2019399	2019400	2019401	2019402	2019403	2019404	2019405	2019406	2019407	2019408	2019409	2019410	2019411	2019412	2019413	2019414	2019415	2019416	2019417	2019418	2019419	2019420	2019421	2019422	2019423	2019424	2019425	2019426	2019427	2019428	2019429	2019430	2019431	2019432	2019433	2019434	2019435	2019436	2019437	2019438	2019439	2019440	2019441	2019442	2019443	2019444	2019445	2019446	2019447	2019448	2019449	2019450	2019451	2019452	2019453	2019454	2019455	2019456'

  students = students.split('\t')

  roll_numbers = roll_numbers.split('\t')

  for x in range(len(students)):
    uandp[students[x]] = roll_numbers[x][2:]

student_data()

items = {'Milk':[[datetime(2020, 11, 11)], 30], 'Dhai':([], 10),'Chips':([], 1)}

def check_expired():
  i = 0

  threading.Timer(24*60*60, check_expired).start()

  for x in list(items.keys()):

    for y in items[x][0]:

      if y < datetime.now():

        print('one {} expired'.format(x))

        buy(x,'expired')

        items[x][0].remove(y)


def create_sell():
  global sell_portal

  sell_portal = Tk()

  sell_portal.title('Sell')

  sell_portal.geometry("{0}x{1}+0+0".format(sign_in_portal.winfo_screenwidth(), sign_in_portal.winfo_screenheight()))

  sell_portal.configure(background='light blue')

  global labels

  labels = {}

  def place_items(text1, r, c, position, size=12, colour='black',i=''):
    labels['{}'.format(i)] = Label(sell_portal, text=text1, bg='light blue', fg=colour, font="none {}".format(size))
    labels['{}'.format(i)].grid(row=r, column=c, sticky=position)

  i = 1

  place_items('\n' + ' ' * 4 + 'S.no' + '  ' + 'Item' + '_' * 20 + 'Price(Rs)' + '_' * 5 + 'number left', 0, 0, W, 30)

  for x in list(items.keys()):
    place_items( '\n' + ' ' * 4 + '  {}.   '.format(i) + '  ' + x + '_' * int(26 - len(x)) + str(items[x][1]) + '_' * 12 + str(len(items[x][0])), i, 0, W, 30, i = x)
    btn = Button(sell_portal, text='sell', width=10, font='none 19')
    btn['command'] = lambda arg1=x: sell(arg1)
    btn.grid(row=i, column=1, sticky=SE)

    i += 1
  place_items('\n' + ' ' * 7, i, 0, W, 30)



  sell_portal.mainloop()




def create_buy_portal():

  global buy_portal

  buy_portal = Tk()

  buy_portal.title('Buy')

  buy_portal.geometry("{0}x{1}+0+0".format(sign_in_portal.winfo_screenwidth(), sign_in_portal.winfo_screenheight()))

  buy_portal.configure(background='light blue')

  global labels

  labels = {}

  def place_items(text1, r, c, position, size=12, colour='black',i=''):
    labels['{}'.format(i)] = Label(buy_portal, text=text1, bg='light blue', fg=colour, font="none {}".format(size))
    labels['{}'.format(i)].grid(row=r, column=c, sticky=position)

  i = 1

  place_items('\n' + ' ' * 4 + 'S.no' + '  ' + 'Item' + '_' * 20 + 'Price(Rs)' + '_' * 5 + 'number left', 0, 0, W, 30)

  for x in list(items.keys()):
    place_items( '\n' + ' ' * 4 + '  {}.   '.format(i) + '  ' + x + '_' * int(26 - len(x)) + str(items[x][1]) + '_' * 12 + str(len(items[x][0])), i, 0, W, 30, i = x)
    btn = Button(buy_portal, text='item info', width=10, font='none 19')
    btn['command'] = lambda arg1=x: create_item_info_window(arg1)
    btn.grid(row=i, column=1, sticky=SE)

    i += 1
  place_items('\n' + ' ' * 7, i, 0, W, 30)



  buy_portal.mainloop()

check_expired()


def get_username_and_password():
  uname = username.get()

  pword = password.get()


  if uname in uandp.keys():
    un = True
    l = list(uandp.keys()).index(uname)

    if list(uandp.values())[l] == pword:
      p = True

    else:
      p = False

  else:
    if uname == 'sell' and pword == 'sell':
      # define selling window here
      create_sell()
      un = 'ud'
    else:
      un = False

  if un == True :

    if p == False:
      create_label('\n'*2 + ' '*70 +'Wrong Password ', 4, 0, W, 24)

    if p == True:
      create_buy_portal()


  else:
    create_label('\n' * 2 + ' ' * 70 + 'Wrong Username', 4, 0, W, 24)


# creating sign_in_portal
sign_in_portal = Tk()
def set_sign_in_portal(title, background_colour):
  sign_in_portal.title(title)
  sign_in_portal.geometry("{0}x{1}+0+0".format(sign_in_portal.winfo_screenwidth(), sign_in_portal.winfo_screenheight()))
  sign_in_portal.configure(background= background_colour)

set_sign_in_portal('sign in', 'light blue')


def create_label(text1, r,c,position, size=12, colour='black'):
  l1 = Label(sign_in_portal,text=text1,bg = 'light blue',fg =colour, font="none {}".format(size))

  l1.grid(row = r, column = c, sticky = position)


create_label(' '*35 + 'SIGN IN TO CONTINUE', 0, 0, W, 36)

create_label('\n'*6 + ' '*20 + 'Username :-', 1, 0, N, 24)

create_label( '\n'*2 + ' '*20 + 'Password :-', 2, 0, N, 24)

username = Entry(sign_in_portal, width = 15, bg = 'white', fg= 'black', font = "none 23")
username.grid(row= 1 , column= 0, sticky = SE)

password = Entry(sign_in_portal, width = 15, bg = 'white', fg = 'black', font = "none 23", show = '*')
password.grid(row= 2, column= 0, sticky =SE)

create_label('\n'*2, 3, 0, W, 24)

submit = Button(sign_in_portal, text='SUBMIT', width = 7, command = get_username_and_password, font = 'none 19')
submit.grid(row = 3, column = 0, sticky = SE)


mainloop()
