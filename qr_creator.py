import qrcode

string = """
What is my name?
Tommy Tommy Tommy.
September 28, 2021; 2302492; 1337; N65; W35
"""

img = qrcode.make(string)
img.save("qr_1.png")
