import sys
# DEPENDENCY ( pyqrcode )

try:
    b = u'\u2588'
    sys.stdout.write(b + '\r')
    sys.stdout.flush()
except UnicodeEncodeError:
    BLOCK = 'MM'
else:
    BLOCK = b


class QR:

    def __init__(self, path):
        from pyqrcode import QRCode
        self.qr_code = QRCode(path)

    def print_cmd_qr(self, white=BLOCK, black='  ', block_width=2):
        block_count = int(block_width)
        if abs(block_count) == 0:
            block_count = 1
        white *= abs(block_count)
        if block_count < 0:
            white, black = black, white
        sys.stdout.write(' ' * 50 + '\r')
        sys.stdout.flush()
        qr = self.qr_code.text(1).replace('0', white).replace('1', black)
        sys.stdout.write(qr)
        sys.stdout.flush()
