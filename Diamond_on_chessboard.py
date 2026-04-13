import numpy as np
import cv2 as cv


video_file = 'B:\\cv\\only_board.mov'
K = np.array([[1097.32511, 0, 593.988134],
              [0, 1086.99723, 265.455875],
              [0, 0, 1]])
dist_coeff = np.array([-0.81089462, 1.5163688, 0.02975743, 0.01103372, -3.78697131])

board_pattern = (13, 9)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

video = cv.VideoCapture(video_file)
assert video.isOpened(), '비디오 파일을 읽을 수 없습니다.'


scale = board_cellsize * 1.5
pts_diamond = np.array([
    [0, 0, -1],  
    [0, 0, 1],   
    [1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0] 
]) * scale


edges = [
    (0, 2), (0, 3), (0, 4), (0, 5), # Top to middle
    (1, 2), (1, 3), (1, 4), (1, 5), # Bottom to middle
    (2, 3), (3, 4), (4, 5), (5, 2)  # Middle ring
]

obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])
frame_count = 0

while True:
    valid, img = video.read()
    if not valid: break

    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)

        angle = frame_count * 0.05
        c, s = np.cos(angle), np.sin(angle)
        R_anim = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        

        center_offset = board_cellsize * np.array([6, 4, -2])
        rotated_pts = (pts_diamond @ R_anim.T) + center_offset


        img_pts, _ = cv.projectPoints(rotated_pts, rvec, tvec, K, dist_coeff)
        img_pts = np.int32(img_pts).reshape(-1, 2)


        for i, j in edges:
            cv.line(img, tuple(img_pts[i]), tuple(img_pts[j]), (255, 255, 0), 2)


        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        cv.putText(img, f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]', (10, 25), 
                    cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    cv.imshow('HW4: Spinning Diamond (Kim Chul-hyeon)', img)
    frame_count += 1
    key = cv.waitKey(10)
    if key == ord(' '): cv.waitKey()
    if key == 27: break

video.release()
cv.destroyAllWindows()