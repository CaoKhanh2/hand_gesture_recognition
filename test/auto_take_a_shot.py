import cv2
import os
import time


time.sleep(2)
cap = cv2.VideoCapture(0)

# Biến đếm, để chỉ lưu dữ liệu sau khoảng 60 frame, tránh lúc đầu chưa kịp cầm tiền lên
i=0
end =100
label = "new"

while(True):
    # Capture frame-by-frameq
    #
    i+=1
    ret, frame = cap.read()

    if not ret or frame is None:
        break

    frame = cv2.resize(frame,(224,224))
    frame = frame.reshape((224, 224, 3))

    #Hiển thị
    if ret == True:
        cv2.imshow('frame',frame)

    # # Lưu dữ liệu
    if 0 <= i <= end:
        # Tạo thư mục nếu chưa có
        if not os.path.exists('./data/train3/' + str(label)):
            os.mkdir('./data/train3/' + str(label))
            
        cv2.imwrite('./data/train3/'+str(label)+'/Image' + str(i) + ".jpg",frame)
    else:
        cap.release()
        cv2.destroyAllWindows()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
