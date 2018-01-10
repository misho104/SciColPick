import os
import sys

"""
Entry point if executed as 'python scicolpick'
"""

if __name__ == '__main__':
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
    sys.path.insert(0, path)
    from scicolpick.scicolpick import scicolpick_main
    sys.exit(scicolpick_main())
