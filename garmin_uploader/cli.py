import argparse
import os.path
from garmin_uploader.workflow import Workflow


def main():
    """
    CLI Entry point
    """
    base_dir = os.path.realpath(os.path.dirname(__file__))
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description='A script to upload .TCX, .GPX, and .FIT'
                  'files to the Garmin Connect web site.',
      epilog=open(os.path.join(base_dir, 'help.txt')).read(),
    )

    parser.add_argument(
        'paths',
        type=str,
        nargs='+',
        help='Path and name of file(s) to upload, list file name, or directory'
             'name containing fitness files.')
    parser.add_argument(
        '-a',
        '--name',
        dest='activity_name',
        type=str,
        help='Sets the activity name for the upload file. This option is'
             'ignored if multiple upload files are given.')
    parser.add_argument(
        '-t',
        '--type',
        dest='activity_type',
        type=str,
        help='Sets activity type for ALL files in filename list, except files'
             'described inside a csv list file.')
    parser.add_argument(
        '-u',
        '--username',
        dest='username',
        type=str,
        help='Garmin Connect user login')
    parser.add_argument(
        '-p',
        '--password',
        dest='password',
        type=str,
        help='Garmin Connect user password')
    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        type=int,
        default=2,
        choices=[1, 2, 3, 4, 5],
        help='Verbose - select level of verbosity. 1=DEBUG(most verbose),'
             ' 2=INFO, 3=WARNING, 4=ERROR, 5= CRITICAL(least verbose).'
             ' [default=2]')

    # Run workflow with these options
    options = parser.parse_args()
    workflow = Workflow(**vars(options))
    workflow.run()


if __name__ == '__main__':
    main()
