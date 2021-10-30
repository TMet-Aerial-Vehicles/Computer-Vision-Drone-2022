from qr_reader import QRReader

# Main Python script


def main():
    qrr = QRReader()

    display_qr = False   # Whether to continuously display QR captured

    # img_path = "/Users/craig/Projects/JTC_ComputerVision/sampleQR1.png"
    # qrr.read(active_display=display_qr, image=img_path)
    qrr.read(active_display=display_qr)

    print(qrr.message)


if __name__ == "__main__":
    main()
