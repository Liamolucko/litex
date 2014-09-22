from miscope.host.uart2wishbone import Uart2Wishbone

csr_csv_file = "./csr.csv"
busword = 8
debug_wb = False

com = 2
baud = 115200
wb = Uart2Wishbone(com, baud, csr_csv_file, busword, debug_wb)