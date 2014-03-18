from onep.cdp.CDPListener import CDPListener
from onep.cdp.CDPEvent import CDPEvent

class cpalCDPListener(CDPListener):
    
    name = str()
    

    def __init__(self, name):        
        super(cpalCDPListener, self).__init__()
        self.name = name
        self.neighbors = set()

    """
      Invoked when an event is received from a network element.
      @param event
                 An event object that indicates that an event has occurred in a network element.
      @param clientData
                 The clientData is an object that is passed in when the application calls an API to add/register
                 the event listener. The application is responsible for casting the input clientData to the
                 appropriate class before using it.
    """     
    def handle_event(self, event, clientData):
        """print "---------------------------"
        print CDPEvent.CDPEventNotifyType.enumval(event.notify_type)
        print "---------------------------"
        print "NetworkInterface = " + event.intf
        print "neighbor  = " + str(event.device_id)
        print "platform = " + event.platform
        print "version = " + event.version
        print "capabilitites = " + event.capabilities
        print "---------------------------\n" """
        neigh = str(event.device_id)
        #print neigh
        self.neighbors.update([neigh])
        #print " ".join(str(x) for x in self.neighbors)
      
