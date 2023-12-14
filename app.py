import optparse
from interface.cli import CLI
from interface.web import Web

class App:
    def __init__(self) -> None:
        self.parser = optparse.OptionParser()
        self.cli = CLI()
        self.web = Web()

    def configure(self):
        self.parser.add_option("-i", "--interface", dest="interface", help="Application interface, default: web")
        self.parser.add_option("-f", "--filename", dest="filename", help="Your file image")
        self.parser.add_option("--cuda", dest="cuda", help="Use GPU", action="store_true")

    def main(self):
        options, args = self.parser.parse_args()
        if options.interface is None:
            options.interface = "web"
        if options.interface == "web":
            self.web.start()
        elif options.interface == "cli":
            self.cli.set_options(options=options)
            self.cli.start()
        else:
            self.parser.print_help()
     
if __name__ == "__main__":    
    app = App()
    app.configure()
    app.main()