from cpal.core.main import device

r1 = device('r1','cisco','10.1.1.110')

r1.getBaseMAC()

r1.native.disconnect()