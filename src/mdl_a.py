import logging
log = logging.getLogger().getChild('mdl_a')

log.info('Loading '  + log.name + '.')

var_a: str = "Hi! I'm " + log.name + '.var_a!'
var_b: str = "Hi! I'm " + log.name + '.var_b!'
var_z: str = "Hi! I'm " + log.name + '.var_z!'

def fnctn_a(var_n: str):
    log.info(var_n + " I'm in " + log.name + '.fnctn_a!')

def fnctn_b(var_n: str):
    log.info(var_n + " I'm in " + log.name + '.fnctn_b!')

def fnctn_z(var_n: str):
    log.info(var_n + " I'm in " + log.name + '.fnctn_z!')


if __name__ == '__main__':
    fnctn_a(var_a)
    fnctn_b(var_b)
    fnctn_z(var_z)