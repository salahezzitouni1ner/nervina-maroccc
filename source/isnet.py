import cv2, numpy as np, sys
from PIL import Image
NET=None
def mask(img):
    global NET
    if NET is None: NET=cv2.dnn.readNetFromONNX('/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad/models/isnet.onnx')
    a=np.asarray(img.convert('RGB').resize((1024,1024),Image.BILINEAR)).astype(np.float32)/255.0
    a=(a-0.5)/1.0
    blob=a.transpose(2,0,1)[None]
    NET.setInput(blob)
    out=NET.forward()
    m=out[0,0]
    m=(m-m.min())/(m.max()-m.min()+1e-8)
    return Image.fromarray((m*255).astype('uint8')).resize(img.size,Image.BILINEAR)
if __name__=='__main__':
    im=Image.open(sys.argv[1]); m=mask(im)
    o=im.convert('RGBA'); o.putalpha(m); o.save(sys.argv[2])
