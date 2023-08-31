import logging
mylog = logging.getLogger().getChild('mdl_z')

mylog.info('⬛ Loading '  + mylog.name + '.')

var_a = "Hi! I'm " + mylog.name + '.var_a!'
var_b = "Hi! I'm " + mylog.name + '.var_b!'
var_z = "Hi! I'm " + mylog.name + '.var_z!'

def fnctn_a(var_n):
    mylog.info('⬛ ' + var_n + " I'm in " + mylog.name + '.fnctn_a!')

def fnctn_b(var_n):
    mylog.info('⬛ ' + var_n + " I'm in " + mylog.name + '.fnctn_b!')

def fnctn_z(var_n):
    mylog.info('⬛ ' + var_n + " I'm in " + mylog.name + '.fnctn_z!')


if __name__ == '__main__':
    fnctn_a(var_a)
    fnctn_b(var_b)
    fnctn_z(var_z)