"""
Utils for testing
"""
import sys
import subprocess


def run_scenario(application='', feature='', scenario='', **opts):
    """
    Runs a Django scenario and returns it's output vars
    """
    if application:
        application = ' {0}/features/'.format(application)

    if feature:
        feature = '{0}.feature'.format(feature)

    if scenario:
        scenario = ' -s {0:d}'.format(scenario)

    opts_string = ''
    for opt, val in opts.items():
        if not val:
            val = ''

        opts_string = ' '.join((opts_string, opt, val))

    cmd = '{0} manage.py harvest -v 3 -T {1}{2}{3}{4}'.format(sys.executable,
                                                                 opts_string,
                                                                 application,
                                                                 feature,
                                                                 scenario,
                                                                 )
    return subprocess.getstatusoutput(cmd)
