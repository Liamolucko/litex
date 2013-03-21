import string
import time
import serial
from struct import *
from migen.fhdl.structure import *

def write_b(uart, data):
	uart.write(pack('B',data))

class Uart2Spi:
	def __init__(self, port, baudrate, debug = False):
		self.port = port
		self.baudrate = baudrate
		self.debug = debug
		self.uart = serial.Serial(port, baudrate, timeout=0.25)
	
	def read(self, addr):
		write_b(self.uart, 0x02)
		write_b(self.uart, (addr>>8)&0xFF)
		write_b(self.uart, (addr&0xFF))
		write_b(self.uart, 0x00)
		read = self.uart.read()
		if self.debug:
			print("RD @ %04X" %addr)
		return int(read[0])
	
	def read_n(self, addr, n, endianess = "LE"):
		r = 0
		words = int(2**bits_for(n-1)/8)
		for i in range(words):
			if endianess == "BE":
				r += self.read(addr+i)<<(8*i)
			elif endianess == "LE":
				r += self.read(addr+words-1-i)<<(8*i)
		if self.debug:
			print("RD @ %04X" %addr)
		return r
		
	
	def write(self, addr, data):
		write_b(self.uart, 0x01)
		write_b(self.uart, (addr>>8)&0xFF)
		write_b(self.uart, (addr&0xFF))
		write_b(self.uart, data)
		if self.debug:
			print("WR %02X @ %04X" %(data, addr))
		
	def write_n(self, addr, data, n, endianess = "LE"):
		words = int(2**bits_for(n-1)/8)
		for i in range(words):
			if endianess == "BE":
				self.write(addr+i, (data>>(8*i)) & 0xFF)
			elif endianess == "LE":
				self.write(addr+words-1-i, (data>>(8*i)) & 0xFF)
		if self.debug:
			print("WR %08X @ %04X" %(data, addr))