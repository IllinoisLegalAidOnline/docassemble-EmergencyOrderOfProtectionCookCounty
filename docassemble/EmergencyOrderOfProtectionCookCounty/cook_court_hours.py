from docassemble.base.util import format_date

def ah_open(test_time):
  if test_time.dow <= 5: #weekdays
    if test_time.hour < 3 and test_time.dow != 1:
      next_ah_open = test_time.minus(days=1)
      next_ah_open = next_ah_open.replace(hour=21)
      next_ah_open = next_ah_open.replace(minute=0)
    else:
      next_ah_open = test_time
      next_ah_open = next_ah_open.replace(hour=21)
      next_ah_open = next_ah_open.replace(minute=0)
  else: #sat or sun
    if test_time.hour > 17: # after 6pm
      if test_time.dow == 6: # sat - next is sun at 1pm
        next_ah_open = test_time
        next_ah_open = next_ah_open.plus(days=1)
        next_ah_open = next_ah_open.replace(hour=13)
        next_ah_open = next_ah_open.replace(minute=0)
      else: # sun - next is mon at 9pm
        next_ah_open = test_time.plus(days=1)
        next_ah_open = next_ah_open.replace(hour=21)
        next_ah_open = next_ah_open.replace(minute=0)
    else: # before 6pm
      if test_time.dow == 6 and test_time.hour < 3: # sat - next is fri 9pm
        next_ah_open = test_time.minus(days=1)
        next_ah_open = next_ah_open.replace(hour=21)
        next_ah_open = next_ah_open.replace(minute=0)
      else:
        next_ah_open = test_time
        next_ah_open = next_ah_open.replace(hour=13)
        next_ah_open = next_ah_open.replace(minute=0)
  court_holidays = load_court_holidays()
  for holiday in court_holidays:
    if str(next_ah_open.format_date('MM/dd/yyyy')) == holiday:
      next_ah_open = next_ah_open.replace(hour=6)
      return ah_open(next_ah_open.plus(days=1))
  else:
    return next_ah_open  

def load_court_holidays():
  holiday_list = [ '01/01/2024', '01/15/2024', '02/12/2024', '02/19/2024', '03/04/2024',
    '05/27/2024', '06/19/2024', '07/04/2024', '09/02/2024', '10/14/2024', '11/05/2024',
    '11/11/2024', '11/28/2024', '11/29/2024', '12/25/2024',
    '01/01/2025', '01/20/2025', '02/12/2025', '02/17/2025', '03/03/2025', '05/26/2025',
    '06/19/2025', '07/04/2025', '09/01/2025', '10/13/2025', '11/11/2025', '11/27/2025',
    '11/28/2025', '12/25/2025',
    '01/01/2026', '01/19/2026', '02/12/2026', '02/16/2026', '03/02/2026', '05/25/2025',
    '06/19/2026', '07/03/2026', '09/07/2026', '10/12/2026', '11/11/2026', '11/26/2026',
    '11/27/2026', '12/25/2026' ]
  return holiday_list

def ah_close(next_ah_open):
  if next_ah_open.dow < 6:
    return next_ah_open.plus(hours=6)
  else:
    return next_ah_open.plus(hours=5)        

def reg_open(test_time):
  if test_time.dow > 5 or (test_time.dow == 5 and ( test_time.hour > 16 or (test_time.hour == 16 and test_time.minute >= 30))): #weekend or friday after 4:30p office closed
    if test_time.dow == 6:
      next_reg_open = test_time.plus(days=2)
    elif test_time.dow == 7:  
      next_reg_open = test_time.plus(days=1)
    else:    
      next_reg_open = test_time.plus(days=3)
    next_reg_open = next_reg_open.replace(hour=8)
    next_reg_open = next_reg_open.replace(minute=30)
  else:
    if test_time.hour > 16 or (test_time.hour == 16 and test_time.minute >= 30): #mon-thurs after 4:30p
      next_reg_open = test_time.plus(days=1)
    else:
      next_reg_open = test_time
    next_reg_open = next_reg_open.replace(hour=8)
    next_reg_open = next_reg_open.replace(minute=30)
  court_holidays = load_court_holidays()
  for holiday in court_holidays:
    if str(next_reg_open.format_date('MM/dd/yyyy')) == holiday:
      next_reg_open = reg_open(next_reg_open.plus(days=1))
      
  return next_reg_open

def reg_close(reg_open):
  return reg_open.plus(hours=8)

def upcoming_court_holidays(date_to_check):
  court_holidays = load_court_holidays()
  holiday_text = ''
  any_holidays = False
  for holiday in court_holidays:
    if str(date_to_check.format_date('MM/dd/yyyy')) == holiday:
      holiday_text = format_date(date_to_check, format='EEEE, MMMM d, yyyy')
      any_holidays = True
      
  for x in range(3):    
    date_to_check = date_to_check.plus(days=1)
    for holiday in court_holidays:
      if str(date_to_check.format_date('MM/dd/yyyy')) == holiday:
        if any_holidays:
          holiday_text += ' and '
        holiday_text += format_date(date_to_check, format='EEEE, MMMM d, yyyy')
        any_holidays = True
  
  return holiday_text
