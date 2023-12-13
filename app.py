import sys
from interface.cli import start_cli
from interface.web import start_web

def main():
    try:
        interface = sys.argv[1]
        if interface not in ["cli", "web"]:
            print ("Interface not found. Auto select interface web")
            interface = "web"
    except IndexError:
        print ("No interface selected. Auto select interface web")
        interface = "web"
    
    if interface == "web":
        start_web()
    elif interface == "cli":
        start_cli()

if __name__ == "__main__":    
    main()