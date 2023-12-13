import sys
import optparse
from interface.cli import start_cli
from interface.web import start_web

def main():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Application interface, default: web")
    parser.add_option("-f", "--filename", dest="filename", help="Your file image")
    parser.add_option("--cuda", dest="cuda", help="Use GPU", action="store_true")
    options, args = parser.parse_args()
    
    if options.interface is None:
        options.interface = "web"
    if options.interface == "web":
        start_web(options)
    elif options.interface == "cli":
        start_cli(options, args)
    else:
        parser.print_help()

if __name__ == "__main__":    
    main()