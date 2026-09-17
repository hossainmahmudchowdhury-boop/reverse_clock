# Revese_clock

I have designed Reverse Clock which is a custom-built clock based on the Raspberry Pi Zero 2 W and a 1.54-inch 240×240 ST7789 TFT LCD.
## CAD Design

### Body 1
![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/picrvc1.png)
### Body 2
![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/picrvc2.png)
### Whole Body
![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/picrvc3.png)

## Custom Firmware

When I will get sleep , It will notify me not to go bed instead of completing my regular task . As rp 2w is an AI starter microcomputer I choosed this . 
How to deploy YOLOV5 in rp 2w is mentioned below.


![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/Screenshot%202026-09-16%20131902.png)

At first I have to make the environment.

    pip install ultralytics

``` # Update system first
  sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv libatlas-base-dev libopenblas-dev libjpeg-dev

# Create virtual environment
python3 -m venv ~/reverse_clock
source ~/reverse_clock/bin/activate

# Install PyTorch first (CPU version for ARM)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Then the rest
pip install -r requirements.txt
```



You have to train your drowsyness dataset . In this case I take the data from 

     https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd

It will take about 4hours+ in cpu but if you use a GPU or other high functional processor it won't take much time .

#### Install app.py code

```

from ultralytics import YOLO

model = YOLO("runs/classify/train/weights/best.pt")

print("Model loaded!")
print("Classes:", model.names)
print("Starting webcam...")

model.predict(
    source=0,
    show=True,
    conf=0.4
)
```



Firstly I identify myself
![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/Screenshot%202026-09-17%20005315.png)

Secondly, I tried the Drowsiness feature
![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/Screenshot%202026-09-18%20005146.png)
Then try the nondrowsiness feature
![image alt](https://github.com/hossainmahmudchowdhury-boop/reverse_clock/blob/main/Images/Screenshot%202026-09-18%20005230.png)


## BOM

| Item                                      | Quantity | Price     | Link |
| ----------------------------------------- | -------- | --------- | ---- |
| Raspberry Pi Zero 2 W                     | 1        | $32.65    | [Link](https://ali.onl/2yvu) |
| 5MP RPi Zero Camera + 15 cm FFC           | 1        | $9.71     | [Link](https://alishort.com/8dFxK) |
| 1.54inch LCD Module 240x240 (ST7789)      | 1        | $11.72      | [Link](https://s.click.aliexpress.com/e/_Dmf...) |
| TP4056 Charging Module (with protection)  | 1        | $5.61| [Link](https://ali.onl/2yvm) |
| Rechargeable Battery (3.7V LiPo / 18650)  | 1        | $6.39     | [Link]( https://s.click.aliexpress.com/e/_DdI...) |
| Mini Breadboard                           | 1        | $0.49      | [Link](https://s.click.aliexpress.com/e/_Dmn...) |
| Jumper Wires (Male-Female pack)         | 1        | $4.69      | [Link](https://ali.onl/2yvn) |
| MicroSD Card (16GB)         | 1        | $4.09      | [Link](https://ali.onl/2yvo) |
| 40 pin GPIO Header                        | 1        | $2.73        | [Link](https://ali.onl/2yvp) |
| 3.7V to 5V Boost Converter      | 1        | $1.09      | [Link](https://ali.onl/2yvq) |
| Power Switch                              | 5        | $1     | [Link](https://ali.onl/2yvr) |
|Top Case                                   |1        |                 |Printing Legion|
Base  Case                                   |1        |                 |Printing Legion|
