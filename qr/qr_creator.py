import qrcode

string = """Questions:
Tshirt colour? Hair colour? Item carried?
2021-08-18; 16:37; S_Comm1; S02; 49.90440649280493; -98.27393447717382
"""

img = qrcode.make(string)
img.save("sampleQR2.png")
