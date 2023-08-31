import utils.logz
mylog = utils.logz.init_logfile('logs\\', __file__).getChild('test')

mylog.info('Loading '  + mylog.name + '.')

import mdl_a
import mdl_b
import mdl_z
import pkg_a.mdl_a
import pkg_a.mdl_b
import pkg_a.mdl_z
import pkg_b.mdl_a
import pkg_b.mdl_b
import pkg_b.mdl_z
import pkg_z.mdl_a
import pkg_z.mdl_b
import pkg_z.mdl_z

if __name__ == '__main__':
    try: # Code to execute, at least until an exception occurs
        mylog.info('⬛ Trying Actions…')
        
        # … user messages as needed …
        print('🟩 MSG_TYPE: Message.')
        mylog.info('⬛ Message')
        mylog.debug('⚪ Message.')
        mylog.warning('🟧 Message.', exc_info = True)
        mylog.error('🟥 Message.', exc_info = True)
        mylog.critical('🟥🟥 Message.', exc_info = True)
        mylog.exception('🟥 Specified Exception Message.', exc_info = True)
        mylog.exception('🟥🟥 Unspecified Exception Message.', exc_info = True)

        pkg_z.mdl_a.fnctn_b(pkg_z.mdl_z.var_z)
        pkg_a.mdl_z.fnctn_a(pkg_b.mdl_a.var_b)
        pkg_b.mdl_a.fnctn_z(pkg_z.mdl_z.var_z)
        pkg_a.mdl_z.fnctn_a(mdl_z.var_z)
        pkg_a.mdl_b.fnctn_a(pkg_z.mdl_a.var_a)
        mdl_z.fnctn_b(mdl_a.var_b)
        mdl_z.fnctn_z(pkg_a.mdl_b.var_b)
        
        mylog.info('🟩 …Completed Actions.')
    # … optional code to handle specified exceptions …
    except Exception: # Code to handle unspecified exceptions
        mylog.exception('🟥🟥 FATAL ERROR: UNEXPECTED EXCEPTION OCCURRED!',
                        exc_info = True
        )
    finally: # Code to always execute, even if an exception occurs
        utils.logz.term_logfile(mylog, __file__)