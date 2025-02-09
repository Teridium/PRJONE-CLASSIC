from storage import *

items = [
    {'id':3, 'count':10},
    {'id':1, 'count':100},
    {'id':3, 'count':100},
    {'id':1, 'count':10},
    {'id':3, 'count':100},
    {'id':1, 'count':100},
]

list_allow = [
    {'id':1, 'count':50},
    {'id':3, 'count':30},
    {'id':6, 'count':80},
]

sklad = storage(None, None, 3, None, list_allow)
not_fit = sklad.add_items(items)

print('****************sklad.cell')
print(sklad.cell)
print('****************not fit')
print(not_fit)


