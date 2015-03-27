
class Email:
    def __init__(self, args):
        self.fromAddress = args["from"]
        self.toAddress = args["to"]
        self.subject = args["subject"]
    def run(self):
        pass

def init(args):
    return Email(args)
