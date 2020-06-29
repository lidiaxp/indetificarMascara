import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
mouthCascade = cv2.CascadeClassifier('Mouth.xml')
noseCascade = cv2.CascadeClassifier('Nariz.xml')

# image = cv2.imread("this.jpg")



def generate(image, com, sem):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tt = image.shape[:2][1]/2
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    nose = noseCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    mouths = mouthCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    try:
        f, m, e, n = False, False, False, False
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if len(faces) > 0:
            cv2.rectangle(image, (faces[0][0], faces[0][1]), (faces[0][0]+faces[0][2], faces[0][1]+faces[0][3]), (255, 0, 0), 2)
            f = True
        else:
            f = False

        for (x, y, w, h) in eyes:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            e = True
    
        if len(nose) > 0:
            for (x, y, w, h) in nose:
                if y+h < faces[0][1]+faces[0][3] and y > faces[0][1] and x > faces[0][0] and x+w < faces[0][0]+faces[0][2] and y+h > eyes[0][1]+eyes[0][3] and eyes[0][3] > h:
                    if eyes[0][1]+eyes[0][3]+25 > y:
                        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        n = True

        
        # for (x, y, w, h) in mouths:
        #     if y+h < faces[0][1]+faces[0][3] and y > faces[0][1] and x > faces[0][0] and x+w < faces[0][0]+faces[0][2]:
        #         if y > eyes[0][1]+eyes[0][3] and nose[0][1]+nose[0][3]+40 > y:
        #             if x < tt and x+w > tt: 
        #                 cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 255), 2)

        if f and e and n:
            sem += 1
            com = 0
        else:
            com += 1
            sem = 0
        
        if com > 6:
            cv2.putText(image, "Com mascara", (500,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        
        if sem > 6:
            cv2.putText(image, "Sem mascara", (500,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

        f, e, n = False, False, False

    except:
        pass
    return com, sem


def recognize(mouths, eyes, image):
    try:
        count = 0
        for i in range(len(mouths)):
            a, b, c, d = mouths[i][0], mouths[i][1], mouths[i][2], mouths[i][3]
            ea1, eb1, ec1, ed1 = eyes[0][0], eyes[0][1], eyes[0][2], eyes[0][3]

            if len(eyes) > 1:
                ea2, eb2, ec2, ed2 = eyes[1][0], eyes[1][1], eyes[1][2], eyes[1][3]
                value2 = c < eb2+ed2
                tt = None
            else:
                tt = 425
                ea2 = ea1
                ec2 = ec1
                value2 = True

            if b+d > eb1+ed1 and value2:
                # cv2.rectangle(image, (a, b), (a+c, b+d), (255, 0, 0), 2)
                if tt != None:
                    if ea1 > tt:
                        if a+c < max(ea1+ec1, ea2+ec2)+40:
                            # print("tem boca 1")
                            count = 1
                            break
                    else:
                        if a > min(ea1, ea2)-40:
                            # print("tem boca 2")
                            count = 1
                            break
                else:
                    if a < min(ea1+ec1, ea2+ec2)-40 or a+c < max(ea1, ea2)+40:
                        # print("tem boca 3")
                        count = 1
                        break

        if count == 1:
            print("pessoa n ta usando mascara")
        else:
            print("pessoa esta usando mascara")
    except:
        print("sem resposta")



# image = cv2.VideoCapture(-1)
# while(True):
#     count = 0
#     ret, frame = image.read()

#     m, e = generate(frame)
#     recognize(count, m, e)
    
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


video_capture = cv2.VideoCapture("ilana.mp4")
com, sem = 0, 0
out = cv2.VideoWriter('toiCovidBuster.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280,720))

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    com, sem = generate(frame, com, sem)
    out.write(frame)
    # recognize(m, e, frame)
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
out.release()
cv2.destroyAllWindows() 


# cv2.imshow("Titulo da imagem", image)
# cv2.waitKey(0)
