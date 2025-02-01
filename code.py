Web VPython 3.2
url = window.location.href

#引入函式庫
from vpython import *

# 用戶輸入
mass = float(input('質量 (kg) (限制數值在0.1到0.25之間): '))  # 質量
amplitude = float(input('初始震幅 (m) (限制數值在0.005到0.05之間): '))  # 初震幅
thickness = float(input('銅板厚度 (mm) (限制數值在2到10之間): '))  # 銅板厚度
height = float(input('初平衡點距離銅板高度 (m) (限制數值在0.005到0.08之間，必須大於初始震幅): '))  # 初平衡點距離銅板高度
spring_constant = float(input('彈力常數 (N/m) (限制數值在10到25之間): '))  # 彈力常數
lasted=5
# 驗證輸入值是否在範圍內
if mass > 0.25 or mass < 0.1:
    print('輸入數值不在預設範圍')
elif amplitude > 0.05 or amplitude < 0.005:
    print('輸入數值不在預設範圍')
elif thickness > 10 or thickness < 2:
    print('輸入數值不在預設範圍')
elif height > 0.08 or height < 0.005:
    print('輸入數值不在預設範圍')
elif spring_constant > 25 or spring_constant < 10:
    print('輸入數值不在預設範圍')
elif height <= amplitude:
    print('輸入數值不在預設範圍')
else:
# 計算系統參數
    T = (2 * pi * (mass / spring_constant) ** 0.5)  # 震盪週期公式
    k = 0.000026386269  # 固定比例常數，用於計算阻尼係數
    a = 0.1348 - 0.1308 * exp (-0.107 * thickness)  # 修正括號並正確計算 a
    b = k * (height ** -3) * (mass ** -0.75) * a  # 阻尼係數公式

# 動畫效果顯著化
    height = 5 * height  # 放大高度以便於觀察動畫效果
    amplitude = 5 * amplitude  # 放大震幅以便於觀察動畫效果
# VPython 場景建立
    scene = canvas(title="Damped Oscillation Animation",
                  width=800, height=450,
                  center=vector(0, height / 2+0.5 , 0), align='right' # 將視角中心置於彈簧和物體運動範圍
                  )
#建立圖表
    graph1 = graph(title="物體位置隨時間的變化",width=700, height=500, xtitle="時間(s)", ytitle="高度(m)",align='left', fast=False)
    displacement_curve = gcurve(color=color.blue, label="軌跡")

# 創建物件與結構
    copper_plate = box(pos=vector(0, 0, 0), size=vector(1, 0.02, 1), color=color.orange)  # 銅板
    horizontal_bar = box(pos=vector(0, 1, 0), size=vector(1, 0.02, 0.02), color=color.gray(0.6))  # 橫槓
    object = box(pos=vector(0, 1 - 0.5, 0), size=vector(0.1, 0.1, 0.1), color=color.gray(0.8), make_trail=True)  # 物體(製造軌跡)
    spring = helix(pos=horizontal_bar.pos,
                  axis=object.pos - horizontal_bar.pos,
                  radius=0.05, coils=20, thickness=0.01, color=color.gray(0.6))  # 彈簧
# 時間步長
    dt = 0.01  # 每次更新的時間間隔
    time = 0  # 初始時間
# 位移函數
def get_amplitude(time):
    return amplitude * exp(-b * time) * cos(2 * pi * time / T)  # 計算某時刻的位移
# 動畫
times = []  # 用於儲存時間數據
displacements = []  # 用於儲存位移數據

while time < lasted:  
    rate(100)  # 每秒更新100次
    shift = 0.1 * time  # 隨時間向左平移的量
#平移物體與場景使軌跡可視化
    y = get_amplitude(time)  # 計算當前位移
    object.pos = vector(shift, 1 -0.5 + y, 0)  # 更新物體位置
    spring.pos.x= shift# 更新彈簧位置
    spring.axis = object.pos - spring.pos+vector(0,0.05,0) #讓彈簧尾部貼齊物體表面 
    copper_plate.pos.x = shift  # 銅板向左平移
    horizontal_bar.pos.x = shift  # 橫槓向左平移
    scene.center.x =shift # 讓畫面中心跟隨物體運動（包括平移） 
    times.append(time)  # 儲存當前時間
    displacements.append(y)  # 儲存當前位移
    
    displacement_curve.plot(time, y)#用圖表紀錄物體位置隨時間的變化
    time += dt  # 更新時間
