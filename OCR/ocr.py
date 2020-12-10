# ocr
#
# @refer https://github.com/PaddlePaddle/PaddleOCR
#

from PaddleOCR import PaddleOCR, draw_ocr
from PIL import Image

# 模型路径下必须含有model和params文件
ocr = PaddleOCR(
    det_model_dir='PaddleOCR/inference/ch_ppocr_mobile_v1.1_det_infer',
    rec_model_dir='PaddleOCR/inference/ch_ppocr_mobile_v1.1_rec_infer',
    cls_model_dir='PaddleOCR/inference/ch_ppocr_mobile_v1.1_cls_infer',
    use_pdserving=False,
    use_angle_cls=True)

imfile = 'test.jpg'
result = ocr.ocr(imfile, cls=True)

image = Image.open(imfile).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='PaddleOCR/doc/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.show()
