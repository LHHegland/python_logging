import logging

from lib.log import Log, ExceptionMessageFormatted

log = logging.getLogger(__name__)

with Log(__file__):
    log.info('Loading '  + log.name + '.')

    import mdl_a
    import mdl_b
    import mdl_z
    import lib.pkg_a.mdl_a
    import lib.pkg_a.mdl_b
    import lib.pkg_a.mdl_z
    import lib.pkg_b.mdl_a
    import lib.pkg_b.mdl_b
    import lib.pkg_b.mdl_z
    import lib.pkg_z.mdl_a
    import lib.pkg_z.mdl_b
    import lib.pkg_z.mdl_z


    if __name__ == '__main__':
        try:
            log.info('Trying Actions…')
            
            # … user messages as needed …
            print('MSG_TYPE: Message.')
            log.info('Message')
            log.debug('Message.')
            log.warning('Message.')
            log.error('Message.')
            log.critical('Message.')
            log.exception('Specified Exception Message.')
            log.exception('🟥 Unspecified Exception Message.')

            lib.pkg_z.mdl_a.fnctn_b(lib.pkg_z.mdl_z.var_z)
            lib.pkg_a.mdl_z.fnctn_a(lib.pkg_b.mdl_a.var_b)
            lib.pkg_b.mdl_a.fnctn_z(lib.pkg_z.mdl_z.var_z)
            lib.pkg_a.mdl_z.fnctn_a(mdl_z.var_z)
            lib.pkg_a.mdl_b.fnctn_a(lib.pkg_z.mdl_a.var_a)
            mdl_z.fnctn_b(mdl_a.var_b)
            mdl_z.fnctn_z(lib.pkg_a.mdl_b.var_b)
        
            log.info('🟩 …Completed Actions.')
        except Exception:
            msg = ExceptionMessageFormatted(
                title='UNEXPECTED ERROR',
                details='An unexpected error has occurred.',
                suggestions='Please check your inputs and try again. Or, contact the developer.',
            )
            log.critical(str(msg))