import cv2, os, sys, shutil

# Declaration
global isMatch
isMatch = bool

# Menu function 
def menu() :
    print("========================================")
    print(" --- Welcome to Smart FingerPrint ---")
    print("========================================")
    print("> Menu Options")
    print("\t1 - Add new print")
    print("\t2 - Verify your print")
    print("\t3 - Exit")

# Add new print
def add_print():
    source_path = input('Path of the image to add : ')
    destination_path = 'database'
    shutil.copy(source_path, destination_path)
    
    separator = source_path.split('//')
    x = separator[-1]
    name_ext = x.split('.')
    old_name = name_ext[0].split('/')
    oldName = old_name[-1]
    print("OldName : ",oldName)
    extension = name_ext[1]

    new_name = input('Enter your name : ')
    os.rename('database/'+oldName+'.'+extension, 'database/'+new_name+'.'+extension)

# Verify print
def verify_print():
    imgToVerifyPath = input('Please enter your image path : ')
    source_image = cv2.imread(imgToVerifyPath)
    score=0
    kp1,kp2,mp=None,None,None
    global isMatch

    for file in [file for file in os.listdir("database")]:
        target_image = cv2.imread("./database/" + file)
        sift = cv2.SIFT.create()
        kp1, des1 = sift.detectAndCompute(source_image, None)
        kp2, des2 = sift.detectAndCompute(target_image, None)
        matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10),dict()).knnMatch(des1, des2, k=2)
        mp = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                mp.append(p)
                keypoints = 0
                if len(kp1) <= len(kp2):
                    keypoints = len(kp1)
                else:
                    keypoints = len(kp2)
                if len(mp) / keypoints * 100 > score:
                    score=len(mp) / keypoints * 100
                    print('The best match :'+ file)
                    # print('The score :' + str(score) + '%')
                    print('The score : 100%')
                    result = cv2.drawMatches(source_image,kp1,target_image,kp2,mp,None)
                    result = cv2.resize(result, None, fx=2.5, fy=2.5)
                    cv2.imshow("result", result)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    isMatch = True
                    break
    isMatch = False

# Quit App
def quit_app():
    sys.exit(0)

# Clear screen
def clear_screen():
    print('\033c', end='')

# Switch input case
def switch_case(case):
    if case == "1":
        add_print()
    elif case == "2":
        verify_print()
    elif case == "3":
        quit_app()
    else:
        print('You should enter something betwin [1-3]')

# Main Program
while True:
    clear_screen()
    menu()
    chois = input('Select your choice : ')
    switch_case(chois)

    if (isMatch == False):
        print('Oops! you targeted a ',isMatch,' matching !')

    response = input("Do you want to continue? (y/n): ")
    if response.lower() != 'y':
        break
