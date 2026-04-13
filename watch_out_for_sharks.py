import numpy as np
import cv2 as cv

video_file = 'B:\\cv\\only_board.mov'
shark_file = 'B:\cv\sha.mp4'  

K = np.array([[1097.32511, 0, 593.988134],
              [0, 1086.99723, 265.455875],
              [0, 0, 1]])
dist_coeff = np.array([-0.81089462, 1.5163688, 0.02975743, 0.01103372, -3.78697131])

board_pattern = (13, 9)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK


video = cv.VideoCapture(video_file)
shark_video = cv.VideoCapture(shark_file)


sw = int(shark_video.get(cv.CAP_PROP_FRAME_WIDTH))
sh = int(shark_video.get(cv.CAP_PROP_FRAME_HEIGHT))
shark_pts_2d = np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]])


shark_pts_3d = board_cellsize * np.array([
    [2, 0, -3], [10, 0, -3], [10, 8, -3], [2, 8, -3]
], dtype=np.float32)

obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

while True:
    valid, img = video.read()
    if not valid: break
    
    ret_s, shark_frame = shark_video.read()
    
    if not ret_s:
        shark_video.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret_s, shark_frame = shark_video.read()

    if shark_frame is None:
        continue

    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)
        
        dst_pts, _ = cv.projectPoints(shark_pts_3d, rvec, tvec, K, dist_coeff)
        dst_pts = dst_pts.reshape(-1, 2).astype(np.float32)

        M = cv.getPerspectiveTransform(shark_pts_2d, dst_pts)
        
        warped_shark = cv.warpPerspective(shark_frame, M, (img.shape[1], img.shape[0]))
        
        #크로마키 제거
        hsv = cv.cvtColor(warped_shark, cv.COLOR_BGR2HSV)
  
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv.inRange(hsv, lower_green, upper_green)
        
        black_mask = cv.inRange(warped_shark, (0,0,0), (5,5,5))
        shark_mask = cv.bitwise_not(cv.bitwise_or(mask, black_mask))
        

        img_bg = cv.bitwise_and(img, img, mask=cv.bitwise_not(shark_mask))
        img_fg = cv.bitwise_and(warped_shark, warped_shark, mask=shark_mask)
        img = cv.add(img_bg, img_fg)

    cv.imshow('watch_out_for_sharks', img)
    if cv.waitKey(10) == 27: break

video.release()
shark_video.release()
cv.destroyAllWindows()