# AR_object_indicator
 Use OpenCV to display AR objects on a pre-captured image.

# 🦈 & ◆ AR Visualization: Shark & Diamond

본 프로젝트는 카메라 캘리브레이션 데이터와 체스판 패턴을 활용하여 카메라의 3차원 자세를 추정하고, 이를 기반으로 동적인 AR 물체를 영상에 합성하는 openCV 프로젝트입니다.

**<아무것도 없었을 때 보드 이미지>**

<img width="900" height="459" alt="image" src="https://github.com/user-attachments/assets/84fe53af-4962-4612-bb77-636b928d6a56" />
---

##  주요 기능

본 저장소는 두 가지 서로 다른 AR 구현 방식을 포함하고 있습니다.

### 1. Watch Out for Sharks! (`watch_out_for_sharks.py`)
**크로마키 합성**: 초록색 배경의 상어 비디오 소스를 실시간으로 마스킹 처리하여 배경을 제거합니다.

**공간감 구현**: 상어 영상을 체스판 위 공중에 띄워 실제 공간에서 헤엄치는 듯한 효과를 줍니다.

**투영 변환**: `solvePnP`로 구한 자세 정보를 바탕으로 `warpPerspective`를 적용하여 카메라 움직임에 따라 상어의 원근감이 실시간으로 변화합니다.

**<상어를 넣은 영상 이미지>**

<img width="1596" height="938" alt="스크린샷 2026-04-14 025732" src="https://github.com/user-attachments/assets/c8668e2b-d40e-4696-97b3-4904f9045714" />

**<상어를 넣은 영상>**


https://github.com/user-attachments/assets/8c54c14b-9f34-447c-9594-949f5c006cc4





### 2. Spinning Diamond (`Diamond_on_chessboard.py`)
**3D 모델링**: 다이아몬드형태의 3D 정점과 에지를 직접 정의하여 시각화합니다.

**실시간 애니메이션**: 프레임 카운트와 삼각함수를 활용해 다이아몬드가 스스로 회전하는 애니메이션 효과를 추가했습니다.

**와이어프레임 렌더링**: `projectPoints`를 통해 3D 좌표를 2D 이미지 평면으로 정합하여 자연스러운 입체감을 제공합니다.


**<다이아몬드를 넣은 영상 이미지>**

<img width="1604" height="937" alt="스크린샷 2026-04-14 031904" src="https://github.com/user-attachments/assets/517b072f-e4ce-428d-b790-c24729c55725" />

**<다이아몬드를 넣은 영상>**

https://github.com/user-attachments/assets/91ed37d3-b716-4bc1-96f1-58aeb8c49427

---

##  실행 환경 및 방법

### 요구 사항
* Python 3.10.0
* OpenCV (`opencv-python`)
* NumPy

### 실행 방법
1. 캘리브레이션에 사용된 보드 영상(`only_board.mov`)과 상어 소스 영상(`sha.mp4`)이 `B:\cv\` 경로 혹은 코드 내 지정된 경로에 있는지 확인합니다.
2. 다음 명령어를 입력하여 프로그램을 실행합니다.
```bash
python watch_out_for_sharks.py
# 또는
python Diamond_on_chessboard.py
